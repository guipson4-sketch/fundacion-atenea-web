// Avisos de Mercado Pago (webhook). Cuando un pago se aprueba:
//  · se guarda en la tabla "donaciones" (una sola vez por pago),
//  · se avisa a administracion@ y se envía la constancia a quien donó.
// Variables: MP_ACCESS_TOKEN (obligatoria), MP_WEBHOOK_SECRET (opcional: firma de Mercado Pago).
import { json, guardar } from "../../cf/lib.js";
import { buzon, enviar, marco, filas, boton, esc, esCorreo, registrarEnvio, DOMINIO } from "../../cf/mail.js";

const soles = n => "S/ " + Number(n || 0).toLocaleString("es-PE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

async function firmaValida(request, env, id) {
  if (!env.MP_WEBHOOK_SECRET) return true;                       // sin secreto, se confía en la consulta directa a la API
  const h = request.headers.get("x-signature") || "";
  const ts = (h.match(/ts=([^,]+)/) || [])[1], v1 = (h.match(/v1=([^,]+)/) || [])[1];
  if (!ts || !v1) return false;
  const manifest = `id:${String(id).toLowerCase()};request-id:${request.headers.get("x-request-id") || ""};ts:${ts};`;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.MP_WEBHOOK_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = [...new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(manifest)))].map(b => b.toString(16).padStart(2, "0")).join("");
  return mac === v1;
}

export async function onRequest({ request, env, waitUntil }) {
  const url = new URL(request.url);
  let id = url.searchParams.get("data.id") || url.searchParams.get("id");
  let tipo = url.searchParams.get("type") || url.searchParams.get("topic");
  if (request.method === "POST") {
    const b = await request.json().catch(() => ({}));
    id = b?.data?.id || id; tipo = b?.type || b?.topic || tipo;
  }
  if (tipo !== "payment" || !id) return new Response("ok");     // otros avisos no nos interesan
  if (!env.MP_ACCESS_TOKEN || !env.DB) return json(503, { error: "No configurado" });
  if (!(await firmaValida(request, env, id))) return json(401, { error: "Firma inválida" });

  // Se consulta el pago directamente a Mercado Pago: así nadie puede inventar una donación.
  const r = await fetch(`https://api.mercadopago.com/v1/payments/${encodeURIComponent(id)}`, { headers: { authorization: `Bearer ${env.MP_ACCESS_TOKEN}` } }).catch(() => null);
  if (!r || !r.ok) return json(502, { error: "No se pudo consultar el pago" });    // Mercado Pago reintenta
  const p = await r.json();
  if (!String(p.external_reference || "").startsWith("don-")) return new Response("ok");

  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS donaciones (
    pago_id TEXT PRIMARY KEY, referencia TEXT, estado TEXT NOT NULL, monto REAL, nombre TEXT, correo TEXT,
    medio TEXT, notificado INTEGER NOT NULL DEFAULT 0, creado TEXT NOT NULL DEFAULT (datetime('now')), actualizado TEXT)`).run();
  const nombre = (p.metadata?.nombre || [p.payer?.first_name, p.payer?.last_name].filter(Boolean).join(" ") || "").slice(0, 80);
  const correo = (p.payer?.email || "").slice(0, 120);
  await env.DB.prepare(`INSERT INTO donaciones (pago_id, referencia, estado, monto, nombre, correo, medio, actualizado)
    VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
    ON CONFLICT(pago_id) DO UPDATE SET estado = excluded.estado, actualizado = datetime('now')`)
    .bind(String(p.id), p.external_reference, p.status, p.transaction_amount, nombre, correo, p.payment_method_id || "").run();

  if (p.status === "approved") {
    // Solo el primer aviso aprobado envía correos (Mercado Pago puede avisar varias veces).
    const marca = await env.DB.prepare("UPDATE donaciones SET notificado = 1 WHERE pago_id = ? AND notificado = 0").bind(String(p.id)).run();
    if (marca?.meta?.changes > 0) {
      const tarea = avisar(env, p, nombre, correo, request).catch(e => console.error("avisar", e));
      if (waitUntil) waitUntil(tarea); else await tarea;
    }
  }
  return new Response("ok");
}

async function avisar(env, p, nombre, correo, request) {
  await guardar(env, "donacion", { monto: p.transaction_amount, nombre, correo, pago: p.id, medio: p.payment_method_id }, request).catch(() => {});
  const datos = { Monto: soles(p.transaction_amount), Donante: nombre || "(sin nombre)", Correo: correo || "(sin correo)", "N.º de operación": String(p.id), Medio: p.payment_method_id || "", Estado: "Aprobado" };
  const a = await enviar(env, {
    to: buzon(env, "administracion"), replyTo: esCorreo(correo) ? correo : undefined,
    subject: `[Donación] ${soles(p.transaction_amount)} de ${nombre || correo || "donante"}`,
    html: marco("Nueva donación aprobada", filas(datos) + `<p style="margin-top:16px">${boton(`https://${DOMINIO}/admin?f=donacion`, "Ver en el panel")}${boton("https://www.mercadopago.com.pe/activities", "Abrir Mercado Pago")}</p>`),
    text: `Donación aprobada: ${soles(p.transaction_amount)} · ${nombre} · ${correo} · operación ${p.id}`,
  });
  await registrarEnvio(env, null, buzon(env, "administracion"), a);
  if (esCorreo(correo)) {
    const fecha = new Date().toLocaleDateString("es-PE", { timeZone: "America/Lima", dateStyle: "long" });
    const b = await enviar(env, {
      to: correo, replyTo: buzon(env, "administracion"),
      subject: "Gracias por tu donación · Fundación Atenea",
      html: marco("¡Gracias por sumar tu color!", `<p>Hola ${esc(nombre || "")}, recibimos tu donación de <strong>${soles(p.transaction_amount)}</strong> el ${esc(fecha)}. Se destinará a los programas de la fundación.</p>
        ${filas({ "N.º de operación": String(p.id), Monto: soles(p.transaction_amount), Fecha: fecha })}
        <p style="font-size:13px;color:#6E5566;margin-top:14px">Esta constancia confirma tu aporte; no es un comprobante tributario. Si necesitas un documento para fines tributarios, responde este correo.</p>`),
      text: `Gracias por tu donación de ${soles(p.transaction_amount)}. N.º de operación ${p.id}.`,
    });
    await registrarEnvio(env, null, correo, b);
  }
}

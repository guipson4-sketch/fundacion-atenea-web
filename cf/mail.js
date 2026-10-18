// Envío de correos con Resend (https://resend.com).
// Variables: RESEND_API_KEY (secreta), MAIL_FROM (opcional), MAIL_<BUZON> para cambiar un destino.
// Si falta RESEND_API_KEY el sitio sigue funcionando: los mensajes quedan en el panel /admin.

export const DOMINIO = "ateneapiuraperu.org";
export const BUZONES = ["contacto", "ayuda", "programas", "voluntariado", "alianzas", "administracion", "gerencia", "privacidad"];

// Devuelve el correo de un buzón (por ejemplo "ayuda" → ayuda@ateneapiuraperu.org).
export const buzon = (env, nombre) => env["MAIL_" + nombre.toUpperCase()] || `${nombre}@${DOMINIO}`;

export const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export const esCorreo = s => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(s || "").trim());

// Celular peruano (9 dígitos que empiezan en 9) → enlace de WhatsApp. Si no lo es, devuelve null.
export function enlaceWhatsApp(texto) {
  const d = String(texto || "").replace(/\D/g, "");
  const n = d.length === 11 && d.startsWith("51") ? d.slice(2) : d;
  return /^9\d{8}$/.test(n) ? `https://wa.me/51${n}` : null;
}

export async function enviar(env, { to, cc, replyTo, subject, html, text }) {
  if (!env.RESEND_API_KEY) { console.warn("RESEND_API_KEY no configurada: no se envía correo."); return { ok: false, error: "sin-clave" }; }
  const from = env.MAIL_FROM || `Fundación Atenea <contacto@${DOMINIO}>`;
  const cuerpo = { from, to: [].concat(to), subject, html, text };
  if (cc) cuerpo.cc = [].concat(cc);
  if (replyTo) cuerpo.reply_to = replyTo;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify(cuerpo),
  }).catch(e => ({ ok: false, status: 0, text: async () => String(e) }));
  if (!r.ok) {
    const detalle = (await r.text().catch(() => "")).slice(0, 300);
    console.error("Resend", r.status, detalle);
    return { ok: false, error: `${r.status} ${detalle}` };
  }
  return { ok: true };
}

// Marco común de los correos (colores del logo).
export function marco(titulo, contenido, pie = "") {
  return `<!doctype html><html lang="es"><body style="margin:0;background:#FBF7F3;font-family:Arial,Helvetica,sans-serif;color:#2A0F22">
<div style="max-width:600px;margin:0 auto;padding:24px 16px">
<div style="height:6px;background:linear-gradient(90deg,#8A2BB0,#C81E73,#EE827C,#F6E08A,#A3CDF5);border-radius:6px 6px 0 0"></div>
<div style="background:#fff;padding:28px 26px;border-radius:0 0 12px 12px">
<h1 style="margin:0 0 16px;font-size:21px;color:#3E0D2C">${esc(titulo)}</h1>${contenido}
<p style="margin:26px 0 0;font-size:12px;color:#6E5566">Fundación Atenea · Juntos por un mejor mañana · Jr. Circunvalación 1384, Piura, Perú · ${DOMINIO}${pie}</p>
</div></div></body></html>`;
}

export const filas = (obj, etiquetas = {}) => `<table style="width:100%;border-collapse:collapse;font-size:14px">` +
  Object.entries(obj).filter(([k, v]) => String(v ?? "").trim() !== "" && k !== "autorizo").map(([k, v]) =>
    `<tr><td style="padding:6px 10px 6px 0;vertical-align:top;color:#6E5566;white-space:nowrap">${esc(etiquetas[k] || k)}</td><td style="padding:6px 0;border-bottom:1px solid #eee">${esc(v).replace(/\n/g, "<br>")}</td></tr>`).join("") + `</table>`;

export const boton = (href, texto) => `<a href="${esc(href)}" style="display:inline-block;margin:6px 8px 0 0;background:#C81E73;color:#fff;text-decoration:none;padding:10px 18px;border-radius:99px;font-size:14px">${esc(texto)}</a>`;

// Deja constancia del envío (para ver en /admin si algún correo falló).
export async function registrarEnvio(env, mensajeId, destino, resultado) {
  if (!env.DB) return;
  try {
    await env.DB.prepare(`CREATE TABLE IF NOT EXISTS envios (
      id INTEGER PRIMARY KEY AUTOINCREMENT, mensaje_id INTEGER, destino TEXT, ok INTEGER NOT NULL, error TEXT,
      creado TEXT NOT NULL DEFAULT (datetime('now')))`).run();
    await env.DB.prepare("INSERT INTO envios (mensaje_id, destino, ok, error) VALUES (?, ?, ?, ?)")
      .bind(mensajeId ?? null, destino, resultado.ok ? 1 : 0, resultado.ok ? null : String(resultado.error || "").slice(0, 300)).run();
  } catch (e) { console.error("D1 envios", e); }
}

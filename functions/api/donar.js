// Donaciones con Mercado Pago (Checkout Pro). Token en la variable secreta MP_ACCESS_TOKEN.
import { json, origenPermitido, limitado, guardar } from "../../cf/lib.js";

export async function onRequestPost({ request, env }) {
  if (!origenPermitido(request, env)) return json(403, { error: "Origen no permitido" });
  if (limitado(request, "donar", 10)) return json(429, { error: "Demasiadas solicitudes. Espera un minuto." });
  if (!env.MP_ACCESS_TOKEN) return json(503, { error: "Las donaciones con tarjeta se activarán muy pronto. Mientras tanto puedes donar por Yape, Plin o transferencia." });

  let b; try { b = await request.json(); } catch { return json(400, { error: "Solicitud inválida" }); }
  const monto = Math.round(Number(b?.monto) * 100) / 100;
  if (!Number.isFinite(monto) || monto < 5 || monto > 20000) return json(400, { error: "Elige un monto entre S/ 5 y S/ 20 000." });
  const email = typeof b?.email === "string" && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(b.email) ? b.email.slice(0, 120) : undefined;
  const nombre = typeof b?.nombre === "string" ? b.nombre.trim().slice(0, 80) : "";
  const site = new URL(request.url).origin;

  const res = await fetch("https://api.mercadopago.com/checkout/preferences", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${env.MP_ACCESS_TOKEN}` },
    body: JSON.stringify({
      items: [{ id: "donacion", title: "Donación · Fundación Atenea", quantity: 1, currency_id: "PEN", unit_price: monto }],
      payer: email ? { email, name: nombre || undefined } : undefined,
      back_urls: { success: `${site}/gracias`, pending: `${site}/gracias?estado=pendiente`, failure: `${site}/involucrate#donar` },
      auto_return: "approved", statement_descriptor: "FUND ATENEA", notification_url: `${site}/api/mp-webhook`,
      external_reference: `don-${Date.now()}`, metadata: { tipo: "donacion", nombre },
    }),
  }).catch(() => null);
  if (!res || !res.ok) { if (res) console.error("MercadoPago", res.status); return json(502, { error: "No pudimos conectar con la pasarela. Intenta de nuevo o dona por Yape." }); }
  const pref = await res.json();
  await guardar(env, "donacion-iniciada", { monto, nombre, email }, request).catch(() => {});
  return json(200, { url: pref.init_point });
}

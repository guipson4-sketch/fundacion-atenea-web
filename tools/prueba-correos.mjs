// Prueba local (sin internet) del flujo de correos y del webhook de pagos: node tools/prueba-correos.mjs
import { onRequestPost as form } from "../functions/api/form.js";
import { onRequest as webhook } from "../functions/api/mp-webhook.js";

const enviados = []; let id = 0; const donaciones = new Map(); let sql = [];
globalThis.fetch = async (url, o = {}) => {
  if (String(url).includes("resend.com")) { enviados.push(JSON.parse(o.body)); return new Response("{}", { status: 200 }); }
  if (String(url).includes("api.mercadopago.com/v1/payments"))
    return new Response(JSON.stringify({ id: 777, status: "approved", transaction_amount: 60, external_reference: "don-1", payment_method_id: "yape", payer: { email: "ana@correo.com" }, metadata: { nombre: "Ana" } }), { status: 200 });
  throw new Error("fetch inesperado " + url);
};
const DB = { prepare(q) { sql.push(q); const st = { args: [], bind(...a) { st.args = a; return st; },
  async run() { if (/INSERT INTO mensajes/.test(q)) return { meta: { last_row_id: ++id } };
    if (/INSERT INTO donaciones/.test(q)) { donaciones.set(st.args[0], { ...(donaciones.get(st.args[0]) || { notificado: 0 }) }); return { meta: {} }; }
    if (/UPDATE donaciones SET notificado/.test(q)) { const d = donaciones.get(st.args[0]); if (d && !d.notificado) { d.notificado = 1; return { meta: { changes: 1 } }; } return { meta: { changes: 0 } }; }
    return { meta: {} }; }, async all() { return { results: [] }; } }; return st; } };
const env = { DB, RESEND_API_KEY: "test", MP_ACCESS_TOKEN: "test" };
const pend = []; const waitUntil = p => pend.push(p);
const enviarForm = async (campos) => {
  const fd = new FormData(); for (const [k, v] of Object.entries(campos)) fd.append(k, v);
  const r = await form({ request: new Request("https://ateneapiuraperu.org/api/form", { method: "POST", body: fd }), env, waitUntil });
  await Promise.all(pend.splice(0)); return r.json();
};
const ok = (c, m) => { if (!c) { console.error("FALLA:", m); process.exitCode = 1; } else console.log("ok  ", m); };

let r = await enviarForm({ "form-name": "contacto", motivo: "Necesito ayuda", nombre: "Rosa", contacto: "rosa@correo.com", mensaje: "Hola", autorizo: "si" });
ok(r.ok && enviados.length === 2, "contacto: 2 correos (equipo + acuse)");
ok(enviados[0].to[0] === "ayuda@ateneapiuraperu.org" && enviados[0].reply_to === "rosa@correo.com", "contacto 'Necesito ayuda' va a ayuda@ y responde a la persona");
ok(!enviados[1].html.includes("Hola</"), "el acuse no repite el mensaje");

enviados.length = 0;
r = await enviarForm({ "form-name": "contacto", motivo: "Voluntariado", nombre: "Luis", contacto: "987654321", mensaje: "Quiero ayudar", autorizo: "si" });
ok(enviados.length === 1 && enviados[0].to[0] === "voluntariado@ateneapiuraperu.org" && enviados[0].html.includes("wa.me/51987654321"), "teléfono: 1 correo con botón de WhatsApp");

enviados.length = 0;
r = await enviarForm({ "form-name": "reclamaciones", nombre: "Marta", documento: "12345678", telefono: "999", domicilio: "Piura", correo: "marta@correo.com", tipo: "Reclamo", descripcion: "Demora", pedido: "Respuesta", autorizo: "si" });
ok(/^LR-\d{4}-\d{5}$/.test(r.codigo), "reclamo: devuelve código " + r.codigo);
ok(enviados.length === 2 && enviados[0].to[0] === "privacidad@ateneapiuraperu.org" && enviados[0].cc[0] === "gerencia@ateneapiuraperu.org", "reclamo: privacidad@ con copia a gerencia@");
ok(enviados[1].to[0] === "marta@correo.com" && enviados[1].html.includes(r.codigo) && enviados[1].html.includes("INDECOPI"), "reclamo: copia al consumidor con código e INDECOPI");

enviados.length = 0;
const hook = () => webhook({ request: new Request("https://ateneapiuraperu.org/api/mp-webhook", { method: "POST", body: JSON.stringify({ type: "payment", data: { id: "777" } }) }), env, waitUntil });
await hook(); await Promise.all(pend.splice(0));
ok(enviados.length === 2 && enviados[0].to[0] === "administracion@ateneapiuraperu.org" && enviados[1].to[0] === "ana@correo.com", "donación aprobada: aviso a administracion@ y constancia al donante");
await hook(); await Promise.all(pend.splice(0));
ok(enviados.length === 2, "aviso repetido de Mercado Pago no duplica correos");

enviados.length = 0; env.RESEND_API_KEY = "";
r = await enviarForm({ "form-name": "boletin", nombre: "Eva", correo: "eva@correo.com" });
ok(r.ok && enviados.length === 0, "sin RESEND_API_KEY el formulario igual responde bien");

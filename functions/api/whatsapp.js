// Respuestas automáticas de WhatsApp (Cloud API de Meta): palabra clave → texto.
// Variables en Cloudflare: WA_TOKEN (token permanente), WA_PHONE_ID, WA_VERIFY_TOKEN, WA_APP_SECRET.
// Sin WA_APP_SECRET el endpoint rechaza todo: así nadie puede hacer que el bot escriba a terceros.
import { json, excedeLimite, igualSeguro } from "../../cf/lib.js";

const WEB = "https://ateneapiuraperu.org";
const TEL = "907 841 529";

const RESP = {
  menu: `Hola, gracias por escribir a Fundación Atenea Piura Perú. Responde con una palabra:\n\n• *información*: quiénes somos y qué hacemos\n• *ayuda*: necesito orientación\n• *donar*: quiero apoyar\n• *voluntariado*: quiero sumarme\n• *alianzas*: quiero aliarme con la fundación\n• *horario*: horario y dirección\n\nO cuéntanos tu consulta y una persona del equipo te responderá.`,
  informacion: `Fundación Atenea Piura Perú es una fundación sin fines de lucro en Piura. Trabajamos con programas de orientación, salud, niñez, mujeres y varones.\n\nConoce nuestros programas: ${WEB}/programas\nEstamos en Jr. Circunvalación N.° 1384, Piura.\n\nSi quieres que te orientemos, escribe *ayuda*.`,
  ayuda: `Gracias por escribirnos. Para orientarte necesitamos solo tu nombre y qué necesitas. Una persona del equipo te responderá en horario de atención.\n\nSi estás en peligro ahora, llama a la Línea 100 (gratuita, 24 horas) o a la Policía al 105.`,
  donar: `Gracias por querer apoyar a Fundación Atenea. Aquí ves cómo donar: ${WEB}/guia-como-donar-en-piura\n\nTambién puedes donar alimentos, útiles o tu tiempo. Escríbenos qué te gustaría aportar y te indicamos cómo coordinar.`,
  voluntariado: `¡Gracias por querer ser voluntaria/o de Fundación Atenea! Cuéntanos tu nombre, tu disponibilidad y en qué te gustaría ayudar. Más información: ${WEB}/involucrate`,
  alianzas: `Gracias por tu interés en aliarte con Fundación Atenea. Cuéntanos quién eres, tu organización y qué propones. Te responderá el equipo de alianzas. También puedes escribir a contacto@ateneapiuraperu.org.`,
  horario: `Atendemos de lunes a viernes, de 9:00 a 18:00, en Jr. Circunvalación N.° 1384, Piura. WhatsApp ${TEL}. Más datos: ${WEB}/contacto`,
};

// Palabras (sin tildes, en minúscula) → respuesta.
const CLAVES = [
  [/\b(donar|donacion|donaciones|apoyar|aportar|yape|cuenta)\b/, "donar"],
  [/\b(voluntari[ao]s?|voluntariado)\b/, "voluntariado"],
  [/\b(alianza|alianzas|convenio|auspicio|patrocinio)\b/, "alianzas"],
  [/\b(ayuda|orientacion|necesito|asesoria)\b/, "ayuda"],
  [/\b(horario|horarios|direccion|ubicacion|donde)\b/, "horario"],
  [/\b(informacion|info|quienes|programas)\b/, "informacion"],
];

export const normalizar = t => String(t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ\s]/g, " ");

export function elegir(texto) {
  const n = normalizar(texto);
  for (const [re, k] of CLAVES) if (re.test(n)) return k;
  return null;
}

async function firmaValida(env, request, cuerpo) {
  if (!env.WA_APP_SECRET) return false;
  const dado = (request.headers.get("x-hub-signature-256") || "").replace("sha256=", "");
  const clave = await crypto.subtle.importKey("raw", new TextEncoder().encode(env.WA_APP_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", clave, new TextEncoder().encode(cuerpo)));
  const esperado = [...mac].map(b => b.toString(16).padStart(2, "0")).join("");
  return igualSeguro(dado, esperado);
}

async function responder(env, a, texto) {
  const r = await fetch(`https://graph.facebook.com/v21.0/${env.WA_PHONE_ID}/messages`, {
    method: "POST",
    headers: { authorization: `Bearer ${env.WA_TOKEN}`, "content-type": "application/json" },
    body: JSON.stringify({ messaging_product: "whatsapp", to: a, type: "text", text: { body: texto, preview_url: false } }),
  }).catch(e => ({ ok: false, status: 0, text: async () => String(e) }));
  if (!r.ok) console.error("WhatsApp", r.status, (await r.text().catch(() => "")).slice(0, 300));
}

// Verificación del webhook que pide Meta al configurarlo.
export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  if (env.WA_VERIFY_TOKEN && u.searchParams.get("hub.mode") === "subscribe" && u.searchParams.get("hub.verify_token") === env.WA_VERIFY_TOKEN)
    return new Response(u.searchParams.get("hub.challenge") || "", { status: 200 });
  return new Response("Prohibido", { status: 403 });
}

export async function onRequestPost({ request, env, waitUntil }) {
  const cuerpo = await request.text();
  if (!(await firmaValida(env, request, cuerpo))) return json(403, { error: "Firma inválida" });
  let datos; try { datos = JSON.parse(cuerpo); } catch { return json(400, { error: "JSON inválido" }); }
  const tareas = [];
  for (const e of datos.entry || []) for (const c of e.changes || []) {
    for (const m of c.value?.messages || []) {
      const de = String(m.from || "");
      if (!/^\d{8,15}$/.test(de)) continue;
      const texto = m.type === "text" ? m.text?.body : m.type === "button" ? m.button?.text : m.type === "interactive" ? (m.interactive?.button_reply?.title || m.interactive?.list_reply?.title) : null;
      tareas.push((async () => {
        if (await excedeLimite(env, "wa-resp", de, 6, 3600)) return;      // máximo 6 respuestas por hora a una misma persona
        let k = texto ? elegir(texto) : null;
        if (!k) { if (await excedeLimite(env, "wa-menu", de, 1, 43200)) return; k = "menu"; }   // el menú, una vez cada 12 h
        await responder(env, de, RESP[k]);
      })().catch(e => console.error("wa", e)));
    }
  }
  const todo = Promise.all(tareas);
  if (waitUntil) waitUntil(todo); else await todo;
  return json(200, { ok: true });
}

// Asistente de soporte de la Fundación Atenea.
// La clave de Gemini vive solo aquí (variable de entorno GEMINI_API_KEY), nunca en el navegador.
import { KNOWLEDGE } from "./knowledge.mjs";

const MODEL = process.env.GEMINI_MODEL || "gemini-3.5-flash-lite";
const MAX_TURNS = 10;          // turnos de historial que se envían
const MAX_CHARS = 800;         // largo máximo de cada mensaje del usuario
const PER_MINUTE = 6;          // límite por IP (mejor esfuerzo, por instancia)
const hits = new Map();

const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});

function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter(t => now - t < 60_000);
  list.push(now); hits.set(ip, list);
  return list.length > PER_MINUTE;
}

export default async (req, context) => {
  if (req.method !== "POST") return json(405, { error: "Método no permitido" });

  // Por defecto solo se acepta el dominio del propio sitio; ALLOWED_ORIGINS añade otros (p. ej. el dominio propio).
  const allowed = (process.env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
  for (const u of [context?.site?.url, process.env.URL, process.env.DEPLOY_PRIME_URL]) {
    try { if (u) allowed.push(new URL(u).origin.replace("http://", "https://")); } catch {}
  }
  const origin = req.headers.get("origin") || "";
  if (allowed.length && origin && !allowed.includes(origin)) return json(403, { error: "Origen no permitido" });

  const ip = context?.ip || req.headers.get("x-nf-client-connection-ip") || "anon";
  if (limited(ip)) return json(429, { error: "Demasiados mensajes seguidos. Espera un minuto, por favor." });

  const key = process.env.GEMINI_API_KEY;
  if (!key) return json(500, { error: "El asistente no está configurado todavía." });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "Solicitud inválida" }); }
  const history = Array.isArray(body?.messages) ? body.messages : [];
  const contents = history.slice(-MAX_TURNS)
    .filter(m => m && (m.role === "user" || m.role === "model") && typeof m.text === "string" && m.text.trim())
    .map(m => ({ role: m.role, parts: [{ text: m.text.slice(0, MAX_CHARS) }] }));
  if (!contents.length || contents.at(-1).role !== "user") return json(400, { error: "Falta el mensaje" });

  // Con la clave propia de Google se llama directo a Gemini (plan gratuito de Google).
  // Sin ella, Netlify AI Gateway inyecta GEMINI_API_KEY y GOOGLE_GEMINI_BASE_URL (usa créditos de Netlify).
  const base = process.env.GOOGLE_GEMINI_BASE_URL || "https://generativelanguage.googleapis.com";
  const res = await fetch(`${base}/v1beta/models/${MODEL}:generateContent`, {
    method: "POST",
    headers: { "content-type": "application/json", "x-goog-api-key": key },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: KNOWLEDGE }] },
      contents,
      generationConfig: { temperature: 0.3, maxOutputTokens: 500 },
    }),
  }).catch(() => null);

  if (!res) return json(502, { error: "No pudimos conectar con el asistente." });
  if (res.status === 429) return json(429, { error: "El asistente alcanzó su límite por ahora. Escríbenos por WhatsApp y te respondemos." });
  if (!res.ok) { console.error("Gemini", res.status, (await res.text()).slice(0, 300)); }
  if (!res.ok) return json(502, { error: "El asistente no está disponible en este momento." });

  const data = await res.json();
  const text = data?.candidates?.[0]?.content?.parts?.map(p => p.text || "").join("").trim();
  if (!text) return json(200, { reply: "No puedo responder eso. Escríbenos por WhatsApp al +51 900 000 000 y una persona del equipo te ayudará." });
  return json(200, { reply: text });
};

// Asistente de soporte (Gemini). La clave vive en la variable secreta GEMINI_API_KEY.
import { KNOWLEDGE } from "../../cf/knowledge.js";
import { json, origenPermitido, limitado } from "../../cf/lib.js";

export async function onRequestPost({ request, env }) {
  if (!origenPermitido(request, env)) return json(403, { error: "Origen no permitido" });
  if (limitado(request, "chat", 6)) return json(429, { error: "Demasiados mensajes seguidos. Espera un minuto, por favor." });
  if (!env.GEMINI_API_KEY) return json(500, { error: "El asistente no está configurado todavía." });

  let body; try { body = await request.json(); } catch { return json(400, { error: "Solicitud inválida" }); }
  const contents = (Array.isArray(body?.messages) ? body.messages : []).slice(-10)
    .filter(m => m && (m.role === "user" || m.role === "model") && typeof m.text === "string" && m.text.trim())
    .map(m => ({ role: m.role, parts: [{ text: m.text.slice(0, 800) }] }));
  if (!contents.length || contents.at(-1).role !== "user") return json(400, { error: "Falta el mensaje" });

  const model = env.GEMINI_MODEL || "gemini-3.5-flash-lite";
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
    method: "POST",
    headers: { "content-type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: KNOWLEDGE }] }, contents,
      generationConfig: { temperature: 0.3, maxOutputTokens: 500 },
    }),
  }).catch(() => null);

  if (!res) return json(502, { error: "No pudimos conectar con el asistente." });
  if (res.status === 429) return json(429, { error: "El asistente alcanzó su límite por ahora. Escríbenos por WhatsApp y te respondemos." });
  if (!res.ok) { console.error("Gemini", res.status, (await res.text()).slice(0, 300)); return json(502, { error: "El asistente no está disponible en este momento." }); }
  const data = await res.json();
  const text = data?.candidates?.[0]?.content?.parts?.map(p => p.text || "").join("").trim();
  return json(200, { reply: text || "No puedo responder eso. Escríbenos por WhatsApp y una persona del equipo te ayudará." });
}

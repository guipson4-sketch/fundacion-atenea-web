// Utilidades compartidas por las funciones de Cloudflare Pages.
export const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});

// Solo se aceptan peticiones desde el propio sitio (y los orígenes de ALLOWED_ORIGINS).
export function origenPermitido(request, env) {
  const origin = request.headers.get("origin");
  if (!origin) return true;
  const ok = (env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
  ok.push(new URL(request.url).origin);
  return ok.includes(origin);
}

// Límite por IP (mejor esfuerzo, en memoria de cada instancia).
const hits = new Map();
export function limitado(request, clave, max, ventanaMs = 60_000) {
  const ip = request.headers.get("cf-connecting-ip") || "anon";
  const k = clave + ":" + ip, now = Date.now();
  const list = (hits.get(k) || []).filter(t => now - t < ventanaMs);
  list.push(now); hits.set(k, list);
  return list.length > max;
}

export async function ipHash(request) {
  const data = new TextEncoder().encode((request.headers.get("cf-connecting-ip") || "") + "|atenea");
  return [...new Uint8Array(await crypto.subtle.digest("SHA-256", data))].map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function guardar(env, formulario, datos, request) {
  if (!env.DB) return false;
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, formulario TEXT NOT NULL, datos TEXT NOT NULL,
    ip_hash TEXT NOT NULL, creado TEXT NOT NULL DEFAULT (datetime('now')))`).run();
  const r = await env.DB.prepare("INSERT INTO mensajes (formulario, datos, ip_hash) VALUES (?, ?, ?)")
    .bind(formulario, JSON.stringify(datos), await ipHash(request)).run();
  return r?.meta?.last_row_id || true;     // id del mensaje (o true si D1 no lo informa)
}

// Utilidades compartidas por las funciones de Cloudflare Pages.
export const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});

// Solo se aceptan peticiones hechas desde el propio sitio (y los orígenes de ALLOWED_ORIGINS).
// Los navegadores siempre envían la cabecera Origin en un POST; si falta, la petición no viene de una página nuestra.
export function origenPermitido(request, env) {
  const origin = request.headers.get("origin");
  if (!origin) return false;
  const ok = (env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
  ok.push(new URL(request.url).origin);
  return ok.includes(origin);
}

// Límite por IP en memoria de cada instancia: primer filtro, barato (no toca la base de datos).
const hits = new Map();
export function limitado(request, clave, max, ventanaMs = 60_000) {
  const ip = request.headers.get("cf-connecting-ip") || "anon";
  const k = clave + ":" + ip, now = Date.now();
  const list = (hits.get(k) || []).filter(t => now - t < ventanaMs);
  list.push(now); hits.set(k, list);
  if (hits.size > 5000) for (const [kk, v] of hits) if (!v.some(t => now - t < ventanaMs)) hits.delete(kk);
  return list.length > max;
}

// Límite compartido entre todas las instancias (tabla "limites" en D1).
// Cuenta los intentos de `id` bajo `clave` en la ventana. Los intentos rechazados no escriben nada,
// así una inundación de peticiones no llena la base de datos. Si D1 falla, se deja pasar (el filtro en memoria sigue activo).
const tablasListas = new WeakMap();   // una comprobación de tabla por cada binding de D1
export async function excedeLimite(env, clave, id, max, ventanaSeg) {
  if (!env.DB) return false;
  try {
    if (!tablasListas.has(env.DB)) tablasListas.set(env.DB, env.DB.batch([
      env.DB.prepare("CREATE TABLE IF NOT EXISTS limites (clave TEXT NOT NULL, id TEXT NOT NULL, t INTEGER NOT NULL)"),
      env.DB.prepare("CREATE INDEX IF NOT EXISTS limites_idx ON limites (clave, id, t)"),
    ]));
    await tablasListas.get(env.DB);
    const ahora = Math.floor(Date.now() / 1000);
    const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM limites WHERE clave = ? AND id = ? AND t > ?").bind(clave, id, ahora - ventanaSeg).first();
    if ((r?.n ?? 0) >= max) return true;
    await env.DB.prepare("INSERT INTO limites (clave, id, t) VALUES (?, ?, ?)").bind(clave, id, ahora).run();
    if (Math.random() < 0.02) await env.DB.prepare("DELETE FROM limites WHERE t < ?").bind(ahora - 2 * 86400).run();
    return false;
  } catch (e) { tablasListas.delete(env.DB); console.error("limites", e); return false; }
}

// Para bloqueos por intentos fallidos (panel /admin): cuenta y anota aparte, sin contar los accesos correctos.
export async function contarEventos(env, clave, id, ventanaSeg) {
  if (!env.DB) return 0;
  try {
    await env.DB.prepare("CREATE TABLE IF NOT EXISTS limites (clave TEXT NOT NULL, id TEXT NOT NULL, t INTEGER NOT NULL)").run();
    const r = await env.DB.prepare("SELECT COUNT(*) AS n FROM limites WHERE clave = ? AND id = ? AND t > ?").bind(clave, id, Math.floor(Date.now() / 1000) - ventanaSeg).first();
    return r?.n ?? 0;
  } catch (e) { console.error("limites", e); return 0; }
}
export async function anotarEvento(env, clave, id) {
  if (!env.DB) return;
  try { await env.DB.prepare("INSERT INTO limites (clave, id, t) VALUES (?, ?, ?)").bind(clave, id, Math.floor(Date.now() / 1000)).run(); }
  catch (e) { console.error("limites", e); }
}

// Cloudflare Turnstile (captcha gratuito). Solo se exige si existe la variable secreta TURNSTILE_SECRET.
export async function turnstileOk(env, token, request) {
  if (!env.TURNSTILE_SECRET) return true;
  if (typeof token !== "string" || !token || token.length > 2048) return false;
  const cuerpo = new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token });
  const ip = request.headers.get("cf-connecting-ip"); if (ip) cuerpo.set("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: cuerpo }).catch(() => null);
  if (!r || !r.ok) return false;
  return (await r.json().catch(() => ({}))).success === true;
}

// Comparación en tiempo constante (evita adivinar contraseñas midiendo tiempos).
export async function igualSeguro(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([a, b].map(v => crypto.subtle.digest("SHA-256", enc.encode(String(v)))));
  const p = new Uint8Array(x), q = new Uint8Array(y); let d = 0;
  for (let i = 0; i < p.length; i++) d |= p[i] ^ q[i];
  return d === 0;
}

// La IP no se guarda: solo un hash. Con la variable secreta IP_SALT el hash no se puede revertir probando direcciones.
export async function ipHash(request, env) {
  const sal = env?.IP_SALT || "atenea";
  const data = new TextEncoder().encode((request.headers.get("cf-connecting-ip") || "") + "|" + sal);
  return [...new Uint8Array(await crypto.subtle.digest("SHA-256", data))].map(b => b.toString(16).padStart(2, "0")).join("");
}

export async function guardar(env, formulario, datos, request) {
  if (!env.DB) return false;
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, formulario TEXT NOT NULL, datos TEXT NOT NULL,
    ip_hash TEXT NOT NULL, creado TEXT NOT NULL DEFAULT (datetime('now')))`).run();
  const r = await env.DB.prepare("INSERT INTO mensajes (formulario, datos, ip_hash) VALUES (?, ?, ?)")
    .bind(formulario, JSON.stringify(datos), await ipHash(request, env)).run();
  return r?.meta?.last_row_id || true;     // id del mensaje (o true si D1 no lo informa)
}

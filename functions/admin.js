// Panel privado de mensajes: /admin  (usuario: atenea · contraseña: variable secreta ADMIN_PASSWORD)
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function igual(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([a, b].map(v => crypto.subtle.digest("SHA-256", enc.encode(v))));
  const p = new Uint8Array(x), q = new Uint8Array(y); let d = 0;
  for (let i = 0; i < p.length; i++) d |= p[i] ^ q[i];
  return d === 0;
}

// "1" = enviado, "0" = falló (group_concat de los envíos de ese mensaje)
const correoEstado = c => c == null ? "—" : String(c).split(",").includes("0")
  ? '<strong style="color:#B3261E">Falló</strong>' : '<span style="color:#1F7A4D">Enviado</span>';

export async function onRequestGet({ request, env }) {
  const pedir = () => new Response("Acceso restringido", { status: 401, headers: { "www-authenticate": 'Basic realm="Fundacion Atenea", charset="UTF-8"' } });
  if (!env.ADMIN_PASSWORD) return new Response("Panel no configurado: falta ADMIN_PASSWORD.", { status: 503 });
  const auth = request.headers.get("authorization") || "";
  if (!auth.startsWith("Basic ")) return pedir();
  let user = "", pass = "";
  // El navegador envía usuario:contraseña en UTF-8 dentro de Base64; se decodifica como UTF-8 (para ñ, tildes, símbolos).
  try {
    const bytes = Uint8Array.from(atob(auth.slice(6)), c => c.charCodeAt(0));
    [user, pass] = new TextDecoder().decode(bytes).split(/:(.*)/s);
  } catch { return pedir(); }
  // Se ignoran espacios al inicio/fin (típicos al copiar y pegar) y mayúsculas en el usuario.
  if (user.trim().toLowerCase() !== "atenea" || !(await igual((pass || "").trim(), env.ADMIN_PASSWORD.trim()))) return pedir();

  const filtro = new URL(request.url).searchParams.get("f") || "";
  let filas = [];
  if (env.DB) {
    try {
      await env.DB.prepare(`CREATE TABLE IF NOT EXISTS envios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, mensaje_id INTEGER, destino TEXT, ok INTEGER NOT NULL, error TEXT,
        creado TEXT NOT NULL DEFAULT (datetime('now')))`).run();
      const q = filtro
        ? env.DB.prepare("SELECT m.*, (SELECT group_concat(ok) FROM envios e WHERE e.mensaje_id = m.id) AS correos FROM mensajes m WHERE formulario = ? ORDER BY id DESC LIMIT 300").bind(filtro)
        : env.DB.prepare("SELECT m.*, (SELECT group_concat(ok) FROM envios e WHERE e.mensaje_id = m.id) AS correos FROM mensajes m ORDER BY id DESC LIMIT 300");
      filas = (await q.all()).results || [];
    } catch { filas = []; }
  }
  const rows = filas.map(r => {
    const d = (() => { try { return JSON.parse(r.datos); } catch { return {}; } })();
    return `<tr><td>${r.id}</td><td>${esc(r.creado)} UTC</td><td>${esc(r.formulario)}</td><td><dl>${Object.entries(d).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v).replace(/\n/g, "<br>")}</dd>`).join("")}</dl></td><td>${correoEstado(r.correos)}</td></tr>`;
  }).join("") || `<tr><td colspan="5">Aún no hay mensajes${env.DB ? "" : " (falta conectar la base de datos D1 con el nombre DB)"}.</td></tr>`;

  return new Response(`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Mensajes · Fundación Atenea</title><style>body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#FBF7F3;color:#2A0F22}main{max-width:1100px;margin:0 auto;padding:32px 20px}
h1{color:#3E0D2C}a{color:#D6287F}table{width:100%;border-collapse:collapse;background:#fff}td,th{padding:10px;border-bottom:1px solid #eee;vertical-align:top;text-align:left}
th{background:#3E0D2C;color:#fff}dl{margin:0}dt{font-weight:600;font-size:12px;text-transform:uppercase;color:#6E5566}dd{margin:0 0 6px}</style></head><body><main>
<h1>Mensajes recibidos</h1><p><a href="?">Todos</a> · <a href="?f=contacto">Contacto</a> · <a href="?f=boletin">Boletín</a> · <a href="?f=reclamaciones">Reclamaciones</a> · <a href="?f=donacion">Donaciones aprobadas</a> · <a href="?f=donacion-iniciada">Donaciones iniciadas</a></p>
<table><tr><th>#</th><th>Fecha</th><th>Formulario</th><th>Datos</th><th>Correo</th></tr>${rows}</table></main></body></html>`,
    { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
}

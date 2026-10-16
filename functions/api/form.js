// Formularios del sitio: se guardan en la base de datos D1 (binding DB).
import { json, origenPermitido, limitado, guardar } from "../../cf/lib.js";

const CAMPOS = {
  contacto: ["motivo", "nombre", "contacto", "mensaje", "autorizo"],
  boletin: ["nombre", "correo"],
  reclamaciones: ["nombre", "documento", "telefono", "domicilio", "correo", "tipo", "descripcion", "pedido", "autorizo"],
};

export async function onRequestPost({ request, env }) {
  if (!origenPermitido(request, env)) return json(403, { error: "Origen no permitido" });
  if (limitado(request, "form", 5)) return json(429, { error: "Demasiados envíos seguidos. Espera un minuto." });
  const fd = await request.formData().catch(() => null);
  if (!fd) return json(400, { error: "Solicitud inválida" });
  const f = fd.get("form-name");
  if (!CAMPOS[f]) return json(400, { error: "Formulario desconocido" });
  if (fd.get("bot-field")) return json(200, { ok: true });          // trampa antispam
  const datos = {};
  for (const k of CAMPOS[f]) datos[k] = String(fd.get(k) ?? "").trim().slice(0, 4000);
  if (CAMPOS[f].includes("autorizo") && !datos.autorizo) return json(400, { error: "Debes autorizar el uso de tus datos." });
  try {
    if (!(await guardar(env, f, datos, request))) return json(500, { error: "No pudimos registrar tu mensaje. Escríbenos por WhatsApp." });
  } catch (e) { console.error("D1", e); return json(500, { error: "No pudimos registrar tu mensaje. Escríbenos por WhatsApp." }); }
  return json(200, { ok: true });
}

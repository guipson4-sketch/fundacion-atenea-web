// Formularios del sitio: se guardan en la base de datos D1 (binding DB).
import { json, origenPermitido, limitado, guardar } from "../../cf/lib.js";
import { notificar } from "../../cf/notificar.js";

const CAMPOS = {
  contacto: ["motivo", "nombre", "contacto", "mensaje", "autorizo"],
  boletin: ["nombre", "correo"],
  reclamaciones: ["nombre", "documento", "telefono", "domicilio", "correo", "tipo", "descripcion", "pedido", "autorizo"],
};

export async function onRequestPost({ request, env, waitUntil }) {
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
  let id;
  try {
    id = await guardar(env, f, datos, request);
    if (!id) return json(500, { error: "No pudimos registrar tu mensaje. Escríbenos por WhatsApp." });
  } catch (e) { console.error("D1", e); return json(500, { error: "No pudimos registrar tu mensaje. Escríbenos por WhatsApp." }); }
  // Hoja de reclamación: el código sale del número del mensaje (LR-2026-00012).
  const codigo = f === "reclamaciones" ? `LR-${new Date().getFullYear()}-${String(id).padStart(5, "0")}` : undefined;
  // El correo se envía después de responder, para que la persona no espere.
  const aviso = notificar(env, f, datos, id, codigo).catch(e => console.error("notificar", e));
  if (waitUntil) waitUntil(aviso); else await aviso;
  return json(200, { ok: true, codigo });
}

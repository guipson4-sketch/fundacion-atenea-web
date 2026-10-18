// Qué correo se envía, y a qué buzón, cuando alguien usa un formulario del sitio.
import { buzon, enviar, marco, filas, boton, esc, esCorreo, enlaceWhatsApp, registrarEnvio, DOMINIO } from "./mail.js";

const ADMIN = `https://${DOMINIO}/admin`;

// Motivo del formulario de contacto → buzón que debe atenderlo.
const RUTA_MOTIVO = {
  "Necesito ayuda": "ayuda",
  "Quiero donar": "administracion",
  "Voluntariado": "voluntariado",
  "Alianza o consultoría": "alianzas",
  "Prensa": "contacto",
};

const ETIQUETAS = {
  motivo: "Motivo", nombre: "Nombre", contacto: "Teléfono o correo", mensaje: "Mensaje", correo: "Correo",
  documento: "Documento", telefono: "Teléfono", domicilio: "Domicilio", tipo: "Tipo", descripcion: "Detalle", pedido: "Pedido del consumidor",
};

async function mandar(env, id, opciones) {
  const r = await enviar(env, opciones);
  await registrarEnvio(env, id, [].concat(opciones.to).join(", "), r);
  return r;
}

export async function notificar(env, formulario, datos, id, codigo) {
  if (formulario === "contacto") return contacto(env, datos, id);
  if (formulario === "boletin") return boletin(env, datos, id);
  if (formulario === "reclamaciones") return reclamo(env, datos, id, codigo);
}

async function contacto(env, d, id) {
  const clave = RUTA_MOTIVO[d.motivo] || "contacto";
  const destino = buzon(env, clave);
  const respuesta = esCorreo(d.contacto) ? d.contacto.trim() : null;
  const wa = enlaceWhatsApp(d.contacto);
  const botones = (respuesta ? boton(`mailto:${respuesta}?subject=${encodeURIComponent("Re: " + (d.motivo || "Tu mensaje a Fundación Atenea"))}`, "Responder por correo") : "")
    + (wa ? boton(wa, "Responder por WhatsApp") : "") + boton(ADMIN, "Ver en el panel");
  const aviso = respuesta ? "Puedes responder directamente a este correo: tu respuesta llegará a la persona." : "La persona dejó un teléfono o un dato que no es un correo: usa los botones para contactarla.";
  await mandar(env, id, {
    to: destino, replyTo: respuesta || undefined,
    subject: `[${d.motivo || "Contacto"}] ${d.nombre || "Mensaje nuevo"} · mensaje #${id}`,
    html: marco(`Nuevo mensaje · ${d.motivo || "Contacto"}`, `<p style="margin:0 0 14px;font-size:14px">${aviso}</p>${filas(d, ETIQUETAS)}<p style="margin-top:16px">${botones}</p>`),
    text: `${d.motivo}\n${d.nombre}\n${d.contacto}\n\n${d.mensaje}\n\nPanel: ${ADMIN}`,
  });
  // Acuse de recibo a la persona, sin repetir su mensaje (puede tener datos sensibles).
  if (respuesta) {
    const urgente = d.motivo === "Necesito ayuda"
      ? `<p style="font-size:14px"><strong>Si estás en peligro ahora</strong>, llama a la Línea 100 (gratuita, 24 horas) o a la Policía al 105.</p>` : "";
    await mandar(env, id, {
      to: respuesta, replyTo: destino,
      subject: "Recibimos tu mensaje · Fundación Atenea",
      html: marco("Recibimos tu mensaje", `<p>Hola ${esc(d.nombre || "")}, gracias por escribirnos. Una persona de nuestro equipo te responderá en un plazo de 48 horas hábiles, por este mismo medio.</p>${urgente}<p style="font-size:13px;color:#6E5566">Tu mensaje se guarda con reserva y solo lo ve el equipo que atiende tu consulta (Ley N.º 29733).</p>`),
      text: `Hola ${d.nombre || ""}, recibimos tu mensaje. Te responderemos en 48 horas hábiles. Si estás en peligro, llama a la Línea 100 o a la Policía al 105.`,
    });
  }
}

async function boletin(env, d, id) {
  await mandar(env, id, {
    to: buzon(env, "contacto"), replyTo: esCorreo(d.correo) ? d.correo : undefined,
    subject: `[Boletín] Nueva suscripción · ${d.correo || d.nombre || ""}`,
    html: marco("Nueva suscripción al boletín", filas(d, ETIQUETAS) + `<p>${boton(ADMIN, "Ver en el panel")}</p>`),
    text: `Suscripción al boletín: ${d.nombre} <${d.correo}>`,
  });
  if (esCorreo(d.correo)) await mandar(env, id, {
    to: d.correo, replyTo: buzon(env, "contacto"),
    subject: "Te suscribiste al boletín de Fundación Atenea",
    html: marco("¡Gracias por sumarte!", `<p>Hola ${esc(d.nombre || "")}, te enviaremos una vez al mes historias, avances y formas de ayudar. Si no fuiste tú, responde este correo y te damos de baja.</p>`),
    text: "Gracias por suscribirte al boletín de Fundación Atenea. Si no fuiste tú, responde este correo.",
  });
}

async function reclamo(env, d, id, codigo) {
  const fecha = new Date().toLocaleString("es-PE", { timeZone: "America/Lima", dateStyle: "long", timeStyle: "short" });
  const ruc = env.FUND_RUC ? `<br>RUC ${esc(env.FUND_RUC)}` : "";
  const plazo = esc(env.RECLAMO_PLAZO || "el plazo que establece la ley");
  const hoja = `<p style="margin:0 0 4px;font-size:13px;color:#6E5566">Hoja de reclamación N.º <strong>${esc(codigo)}</strong> · ${esc(fecha)} (hora de Lima)</p>`
    + `<p style="font-size:13px;margin:0 0 12px">Proveedor: Fundación Atenea · Jr. Circunvalación 1384, Piura${ruc}</p>`
    + filas(d, ETIQUETAS);
  // 1) Al equipo: privacidad@ con copia a gerencia@
  await mandar(env, id, {
    to: buzon(env, "privacidad"), cc: buzon(env, "gerencia"), replyTo: esCorreo(d.correo) ? d.correo : undefined,
    subject: `[Libro de Reclamaciones] ${codigo} · ${d.tipo || "Reclamo"} de ${d.nombre || ""}`,
    html: marco(`Nuevo ${esc(d.tipo || "reclamo")} · ${codigo}`, `<p style="margin:0 0 14px;font-size:14px">Hay que responder a la persona dentro de ${plazo}. Puedes responder a este correo: llegará a ella.</p>${hoja}<p style="margin-top:16px">${boton(ADMIN, "Ver en el panel")}</p>`),
    text: `${codigo}\n${d.tipo}\n${d.nombre} ${d.documento}\n${d.correo} ${d.telefono}\n\n${d.descripcion}\n\nPedido: ${d.pedido}\n\nPanel: ${ADMIN}`,
  });
  // 2) Copia al consumidor (constancia de que su reclamo fue recibido)
  if (esCorreo(d.correo)) await mandar(env, id, {
    to: d.correo.trim(), replyTo: buzon(env, "privacidad"),
    subject: `Constancia de tu ${String(d.tipo || "reclamo").toLowerCase()} · ${codigo}`,
    html: marco("Recibimos tu reclamación", `<p>Hola ${esc(d.nombre || "")}, esta es la copia de tu hoja de reclamación. Te responderemos por este medio dentro de ${plazo}.</p>${hoja}<p style="font-size:12px;color:#6E5566;margin-top:14px">La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el INDECOPI.</p>`),
    text: `Constancia ${codigo}. Recibimos tu ${d.tipo || "reclamo"}. Te responderemos por correo.`,
  });
}

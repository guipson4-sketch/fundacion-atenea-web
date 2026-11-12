"""Guías prácticas de la Fundación Atenea (contenido para búsquedas reales en Piura).

Cada guía genera su propia página (guia-*.html) con Article + FAQPage + BreadcrumbList.
Revisar y actualizar la fecha `updated` cuando cambie una norma, un teléfono o un procedimiento.
"""

UPDATED = "2026-11-12"

EMERGENCIA = ('<p class="callout"><strong>¿Estás en peligro ahora?</strong> Llama a la Policía al <strong>105</strong> '
              'o a la <strong>Línea 100</strong> (gratuita, las 24 horas, atiende a mujeres y varones).</p>')

GUIDES = [
 {
  "file": "guia-asesoria-legal-gratuita-piura.html",
  "tag": "Legal",
  "title": "Asesoría legal gratuita en Piura: dónde pedirla | Atenea",
  "short": "Asesoría legal gratuita en Piura: dónde pedirla y cómo prepararte",
  "desc": "Asesoría legal gratuita en Piura: Fono ALEGRA 1884, Defensa Pública, CEM, DEMUNA y consultorios jurídicos. Qué llevar y cómo prepararte.",
  "h1": 'Asesoría legal gratuita <span class="ital mag">en Piura.</span>',
  "lead": "Si no puedes pagar un abogado, en Piura tienes varias puertas gratuitas. Te contamos cuál elegir según tu caso y cómo llegar preparada o preparado.",
  "related": ["programa-orientacion.html", "programa-mujeres.html"],
  "sections": [
   ("Primero: orientación por teléfono",
    "<p>Si no sabes por dónde empezar, llama al <strong>Fono ALEGRA 1884</strong> del Ministerio de Justicia y Derechos Humanos. Es gratuito y te orientan sobre tu caso y sobre la sede de atención más cercana.</p>"),
   ("Defensa Pública: un abogado gratuito",
    "<p>La <strong>Defensa Pública</strong> del Ministerio de Justicia brinda abogados gratuitos a personas que no pueden pagar uno. Atiende, entre otros, casos de <strong>familia</strong> (alimentos, tenencia, régimen de visitas), <strong>violencia</strong> y casos <strong>penales</strong>. Evalúan tu situación económica en la primera atención.</p>"
    "<ul class=\"list\"><li>Pregunta en el 1884 por la sede de Defensa Pública o ALEGRA más cercana en la región Piura.</li><li>Si eres víctima de violencia, también te representan gratuitamente.</li></ul>"),
   ("Si hay violencia: Centro Emergencia Mujer",
    "<p>Los <strong>Centros Emergencia Mujer (CEM)</strong> del MIMP dan atención legal, psicológica y social gratuita a víctimas de violencia, también a varones. Te acompañan en la denuncia y en el pedido de medidas de protección.</p>"),
   ("Si se trata de niñas, niños o adolescentes: DEMUNA",
    "<p>La <strong>DEMUNA</strong> de tu municipalidad atiende casos de niñas, niños y adolescentes y puede llevar a cabo <strong>conciliaciones</strong> sobre alimentos, tenencia y visitas. El acta de conciliación tiene valor legal y puede exigirse ante un juez si no se cumple.</p>"),
   ("Consultorios jurídicos de universidades",
    "<p>Varias facultades de Derecho de Piura tienen consultorios jurídicos gratuitos o de bajo costo, atendidos por estudiantes bajo la supervisión de abogados. Pregunta directamente en la facultad por sus horarios.</p>"),
   ("Cómo prepararte para la consulta",
    "<ul class=\"list amber\"><li>Lleva tu DNI y, si los tienes, los documentos del caso (partidas, contratos, notificaciones, recibos).</li><li>Escribe en una hoja qué pasó, con fechas, en orden.</li><li>Anota tus preguntas antes de ir.</li><li>Pide que te expliquen los siguientes pasos y los plazos.</li></ul>"),
   ("La orientación de la Fundación Atenea",
    "<p>En la Fundación Atenea te escuchamos gratis y con reserva, te ayudamos a ordenar tu caso y te derivamos al servicio que corresponde. <a href=\"programa-orientacion.html\">Conoce nuestro programa de orientación gratuita</a> o <a href=\"contacto.html\">escríbenos</a>.</p>"),
  ],
  "faqs": [
   ("¿La Defensa Pública es realmente gratis?", "Sí. Es un servicio del Ministerio de Justicia para personas que no pueden pagar un abogado. En la primera atención evalúan tu situación."),
   ("¿Necesito abogado para pedir pensión de alimentos?", "No necesariamente. Puedes conciliar en la DEMUNA o presentar la demanda con el formulario gratuito del Poder Judicial sin firma de abogado. Lo explicamos en nuestra guía de pensión de alimentos."),
   ("¿La Fundación Atenea cobra por orientar?", "No. Toda nuestra orientación es gratuita y confidencial."),
  ],
 },
 {
  "file": "guia-violencia-familiar-piura.html",
  "tag": "Violencia",
  "title": "Violencia familiar en Piura: qué hacer y dónde denunciar",
  "short": "¿Sufres violencia en Piura? Qué hacer, dónde denunciar y cómo pedir protección",
  "desc": "Qué hacer si sufres violencia en Piura: Línea 100, dónde denunciar, medidas de protección de la Ley 30364 y apoyo gratuito del CEM.",
  "h1": '¿Sufres violencia? <span class="ital mag">No estás sola ni solo.</span>',
  "lead": "La violencia física, psicológica, sexual o económica no es normal ni es tu culpa. Esta guía te dice qué hacer, dónde denunciar en Piura y cómo pedir protección.",
  "related": ["programa-mujeres.html", "programa-varones.html"],
  "sections": [
   ("Si estás en peligro ahora",
    "<ul class=\"list\"><li><strong>Policía: 105.</strong></li><li><strong>Línea 100:</strong> gratuita, las 24 horas, orientación y derivación inmediata. Atiende a mujeres y varones.</li><li>Si puedes, ve a un lugar seguro con una persona de confianza.</li></ul>"),
   ("Qué se considera violencia",
    "<p>La Ley N.º 30364 protege a mujeres y a todos los integrantes del grupo familiar frente a cuatro tipos de violencia: <strong>física</strong>, <strong>psicológica</strong>, <strong>sexual</strong> y <strong>económica o patrimonial</strong> (por ejemplo, quitarte el dinero, impedirte trabajar o dejar de cubrir lo necesario para vivir).</p>"),
   ("Dónde denunciar",
    "<p>Puedes denunciar en <strong>cualquier comisaría</strong>, en la <strong>Fiscalía</strong> o directamente en el <strong>Juzgado de Familia</strong>. La denuncia puede ser verbal o escrita, es <strong>gratuita</strong> y <strong>no necesitas abogado</strong>. No hace falta tener pruebas para denunciar: la Policía no puede negarse a recibir tu denuncia.</p>"
    "<p>También puede denunciar otra persona que conozca los hechos.</p>"),
   ("Medidas de protección",
    "<p>Con tu denuncia, el Juzgado de Familia puede dictar <strong>medidas de protección</strong> en plazos cortos, que dependen del nivel de riesgo. Por ejemplo:</p>"
    "<ul class=\"list amber\"><li>Retiro del agresor de la casa.</li><li>Prohibición de acercarse o de comunicarse contigo.</li><li>Prohibición de tener armas.</li><li>Asignación económica de emergencia y otras medidas para tus hijas e hijos.</li></ul>"
    "<p>No cumplir una medida de protección es delito.</p>"),
   ("Apoyo gratuito: Centro Emergencia Mujer",
    "<p>Los <strong>Centros Emergencia Mujer (CEM)</strong> brindan atención legal, psicológica y social gratuita, te acompañan durante la denuncia y en el proceso, y atienden también a varones, niñas, niños y personas adultas mayores.</p>"),
   ("Un plan de seguridad",
    "<ul class=\"list\"><li>Guarda copias de tu DNI y de los de tus hijos en un lugar seguro o en tu correo.</li><li>Acuerda una palabra clave con alguien de confianza para pedir ayuda.</li><li>Ten a mano los números 105 y 100.</li><li>Guarda mensajes, fotos o audios que muestren la violencia.</li></ul>"),
   ("Cómo te acompaña la Fundación Atenea",
    "<p>Te escuchamos sin juicios, te orientamos y te acompañamos a los servicios públicos. No hacemos mediación en casos de violencia. Conoce <a href=\"programa-mujeres.html\">Mujeres que avanzan</a> y <a href=\"programa-varones.html\">Varones y familias</a>.</p>"),
  ],
  "faqs": [
   ("¿Necesito pruebas para denunciar violencia?", "No. Puedes denunciar con tu relato. Las pruebas se recogen durante la investigación; si tienes mensajes, fotos o audios, guárdalos."),
   ("¿Los varones también pueden denunciar violencia familiar?", "Sí. La Ley 30364 protege a todos los integrantes del grupo familiar. La Línea 100 y los CEM atienden también a varones."),
   ("¿Cuánto cuesta denunciar?", "Nada. La denuncia es gratuita y no necesitas abogado."),
  ],
 },
 {
  "file": "guia-pension-de-alimentos-piura.html",
  "tag": "Familia",
  "title": "Pensión de alimentos en Piura: cómo pedirla sin abogado",
  "short": "Pensión de alimentos en Piura: cómo pedirla paso a paso",
  "desc": "Pide pensión de alimentos en Piura sin abogado: conciliación en la DEMUNA o demanda en el Juzgado de Paz Letrado. Requisitos y qué hacer si no pagan.",
  "h1": 'Pensión de alimentos, <span class="ital mag">paso a paso.</span>',
  "lead": "Tus hijas e hijos tienen derecho a alimentos: comida, vivienda, salud, educación, vestido y recreación. Así puedes pedirlos en Piura, incluso sin abogado.",
  "related": ["programa-orientacion.html", "programa-mujeres.html", "programa-ninez.html"],
  "sections": [
   ("Camino 1: conciliar",
    "<p>Si es posible conversar, pueden llegar a un acuerdo en la <strong>DEMUNA</strong> de tu municipalidad o en un centro de conciliación gratuito del Ministerio de Justicia. El acta de conciliación tiene valor legal: si no se cumple, se puede exigir ante un juez.</p>"),
   ("Camino 2: demandar ante el juez",
    "<p>Si no hay acuerdo, presenta una <strong>demanda de alimentos</strong> ante el <strong>Juzgado de Paz Letrado</strong> del lugar donde vive la niña, niño o la persona que pide los alimentos. El Poder Judicial tiene un <strong>formulario gratuito</strong> que puedes presentar <strong>sin firma de abogado</strong>.</p>"),
   ("Qué necesitas",
    "<ul class=\"list amber\"><li>Tu DNI.</li><li>Partida o acta de nacimiento de la niña o el niño.</li><li>Dirección donde se puede notificar a la otra persona.</li><li>Pruebas de los gastos: boletas de colegio, salud, alimentación, recibos.</li><li>Si la conoces, información sobre los ingresos de la otra persona (dónde trabaja, negocio, bienes).</li></ul>"),
   ("¿De cuánto será la pensión?",
    "<p>No hay un monto fijo. El juez la decide considerando las <strong>necesidades</strong> de quien pide y las <strong>posibilidades económicas</strong> de quien debe pagar. Por eso es importante sustentar bien los gastos.</p>"),
   ("Si no pagan",
    "<ul class=\"list\"><li>Pide al juzgado la <strong>liquidación</strong> de lo que se debe.</li><li>Quien adeuda tres cuotas o más puede ser inscrito en el <strong>Registro de Deudores Alimentarios Morosos (REDAM)</strong>.</li><li>No pagar lo ordenado por el juez puede dar lugar a una denuncia por <strong>omisión a la asistencia familiar</strong>.</li></ul>"),
   ("Ayuda gratuita",
    "<p>La <strong>Defensa Pública</strong> (Fono ALEGRA 1884) puede asignarte un abogado gratuito. En la Fundación Atenea te ayudamos a ordenar tus documentos y te derivamos: <a href=\"programa-orientacion.html\">orientación gratuita</a> · <a href=\"guia-asesoria-legal-gratuita-piura.html\">dónde pedir asesoría legal gratuita</a>.</p>"),
  ],
  "faqs": [
   ("¿Puedo pedir pensión de alimentos sin abogado?", "Sí. Puedes usar el formulario gratuito del Poder Judicial y presentarlo en el Juzgado de Paz Letrado sin firma de abogado, o conciliar en la DEMUNA."),
   ("¿Dónde presento la demanda en Piura?", "Ante el Juzgado de Paz Letrado que corresponda al domicilio de quien pide los alimentos. Si tienes dudas, el Fono ALEGRA 1884 te orienta."),
   ("¿Qué pasa si la otra persona no paga?", "Puedes pedir la liquidación de la deuda, su inscripción en el REDAM y, si persiste, denunciar por omisión a la asistencia familiar."),
  ],
 },
 {
  "file": "guia-sis-gratuito-piura.html",
  "tag": "Salud",
  "title": "SIS gratuito en Piura: cómo afiliarte y qué cubre | Atenea",
  "short": "SIS gratuito: cómo afiliarte y qué hacer si algo no está cubierto",
  "desc": "Cómo afiliarte al SIS gratuito en Piura si no tienes seguro de salud, qué cubre, cómo reclamar y qué hacer si un medicamento o examen no está cubierto.",
  "h1": 'SIS gratuito: <span class="ital mag">tu salud primero.</span>',
  "lead": "Si no tienes seguro de salud, puedes afiliarte al Seguro Integral de Salud (SIS) gratuito. Te explicamos cómo hacerlo en Piura y qué hacer si algo no está cubierto.",
  "related": ["programa-salud.html", "programa-orientacion.html"],
  "sections": [
   ("¿Quién puede afiliarse?",
    "<p>Toda persona residente en el Perú que <strong>no tenga otro seguro de salud</strong> (como EsSalud o un seguro privado) puede afiliarse al <strong>SIS gratuito</strong>. Las niñas y niños recién nacidos también pueden ser afiliados.</p>"),
   ("Cómo afiliarte",
    "<ul class=\"list amber\"><li>Acércate con tu DNI al establecimiento de salud del Ministerio de Salud más cercano (posta, centro de salud u hospital).</li><li>También puedes consultar tu afiliación en la web oficial del SIS.</li><li>Si eres extranjera o extranjero residente, pregunta por los documentos que se aceptan.</li></ul>"),
   ("Qué cubre",
    "<p>El SIS cubre consultas, medicamentos, exámenes, hospitalización y procedimientos incluidos en su plan de beneficios, además de un grupo de enfermedades de alto costo. La atención se da en los establecimientos públicos de salud.</p>"),
   ("Si algo no está cubierto o te lo niegan",
    "<ul class=\"list\"><li>Pide que te expliquen por escrito por qué no está cubierto.</li><li>Presenta tu reclamo en el libro de reclamaciones del establecimiento o ante SUSALUD, que protege los derechos de los pacientes.</li><li>Si necesitas un medicamento o examen fuera de la cobertura, <a href=\"programa-salud.html\">nuestro programa de salud</a> puede ayudarte a cubrirlo total o parcialmente.</li></ul>"),
   ("Consejos para tu tratamiento",
    "<ul class=\"list\"><li>Guarda en una carpeta recetas, resultados y citas.</li><li>Pregunta siempre la próxima fecha de control.</li><li>Lleva a una persona de confianza a las citas importantes.</li></ul>"),
  ],
  "faqs": [
   ("¿El SIS gratuito tiene algún costo?", "No. La afiliación y la atención cubierta por el SIS gratuito no tienen costo para la persona asegurada."),
   ("¿Puedo tener SIS si tengo EsSalud?", "No. El SIS gratuito es para quienes no tienen otro seguro de salud."),
   ("¿Qué hago si un medicamento no está cubierto?", "Pide la explicación por escrito, reclama si corresponde y escríbenos: el programa de salud de la Fundación Atenea puede ayudarte con medicamentos y exámenes no cubiertos."),
  ],
 },
 {
  "file": "guia-como-donar-en-piura.html",
  "tag": "Donar",
  "title": "Cómo donar en Piura de forma segura · Fundación Atenea",
  "short": "Cómo donar en Piura de forma segura y cuándo puedes deducirlo",
  "desc": "Cómo elegir una fundación u ONG en Piura para donar con seguridad: RUC, SUNARP, transparencia y cuándo tu donación es deducible.",
  "h1": 'Donar en Piura, <span class="ital mag">con confianza.</span>',
  "lead": "Donar transforma vidas cuando llega a quien lo necesita. Estos son los puntos para revisar antes de donar a cualquier fundación u ONG, incluida la nuestra.",
  "related": ["programa-ayuda.html", "programa-salud.html"],
  "sections": [
   ("Cinco cosas que debes revisar",
    "<ul class=\"list amber\"><li><strong>RUC activo y habido</strong> en la consulta RUC de SUNAT.</li><li><strong>Inscripción en SUNARP</strong> como fundación o asociación.</li><li>En el caso de fundaciones, su inscripción ante el <strong>Consejo de Supervigilancia de Fundaciones</strong>.</li><li><strong>Transparencia</strong>: estatuto, órganos de gobierno y uso de los fondos publicados.</li><li><strong>Canales oficiales</strong> a nombre de la institución, nunca a cuentas personales.</li></ul>"),
   ("Cuándo puedes deducir tu donación",
    "<p>Las donaciones son deducibles del impuesto a la renta solo si la entidad que las recibe está <strong>calificada por SUNAT como entidad perceptora de donaciones</strong> y te entrega un <strong>comprobante de recepción de donaciones</strong>. En ese caso:</p>"
    "<ul class=\"list\"><li><strong>Empresas</strong>: hasta el 10 % de su renta neta de tercera categoría.</li><li><strong>Personas</strong> con renta de cuarta y quinta categoría: hasta el 10 % de la suma de su renta neta del trabajo y de fuente extranjera.</li></ul>"
    "<p>Verifica en SUNAT si la entidad está calificada antes de donar con ese fin.</p>"),
   ("Otras formas de ayudar",
    "<p>Además de dinero, puedes donar tu tiempo como voluntaria o voluntario, tu experiencia profesional o bienes que se necesiten (alimentos, útiles, medicamentos con fecha vigente). Pregunta siempre qué se necesita antes de llevar donaciones en especie.</p>"),
   ("La Fundación Atenea, en claro",
    "<p>La Fundación Atenea Piura Perú está <strong>inscrita en SUNARP</strong> (partida N.º 11345692) y tiene <strong>RUC 20616737172</strong>. Está en trámite su inscripción ante el Consejo de Supervigilancia de Fundaciones y, después, la calificación de SUNAT como entidad perceptora de donaciones: <strong>hasta entonces, nuestras donaciones no son deducibles</strong>. Lo actualizaremos en <a href=\"transparencia.html\">Transparencia</a>.</p>"
    "<p><a class=\"btn btn-main\" href=\"involucrate.html#donar\">Ver cómo donar →</a></p>"),
  ],
  "faqs": [
   ("¿Cómo sé si una ONG de Piura es confiable?", "Revisa su RUC en SUNAT, su inscripción en SUNARP, que publique su estatuto y el uso de los fondos, y que reciba donaciones solo en cuentas a nombre de la institución."),
   ("¿Toda donación se puede deducir del impuesto a la renta?", "No. Solo las hechas a entidades calificadas por SUNAT como perceptoras de donaciones, con comprobante de recepción de donaciones y dentro de los límites de la ley."),
   ("¿Las donaciones a la Fundación Atenea son deducibles?", "Todavía no. Estamos tramitando la inscripción ante el Consejo de Supervigilancia de Fundaciones y luego la calificación de SUNAT. Avisaremos en la sección de Transparencia."),
  ],
 },
]

GUIDE_FILES = {g["file"] for g in GUIDES}

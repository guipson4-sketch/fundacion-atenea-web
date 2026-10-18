#!/usr/bin/env python3
"""Genera las páginas del sitio de la Fundación Atenea con un sistema visual común."""
import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")

WA = ""; WA_TXT = ""      # sin WhatsApp oficial todavía: no se muestra ningún número
MAIL = "contacto@ateneapiuraperu.org"
ADDR = "Jr. Circunvalación 1384, Piura"
RUC = ""                 # sin RUC todavía
HOURS = "Lunes a viernes, 9:00 a 18:00"

NAV = [("nosotros.html","Nosotros"),("programas.html","Programas"),("historias.html","Historias"),
       ("involucrate.html","Involúcrate"),("transparencia.html","Transparencia"),("contacto.html","Contacto")]

def head(title, desc, canon=""):
    ld = LD if canon == "" else ""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://ateneapiuraperu.org/assets/og-atenea.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fundación Atenea">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://ateneapiuraperu.org/assets/og-atenea.jpg">{ld}
<meta property="og:locale" content="es_PE">
<meta name="theme-color" content="#3E0D2C">
<link rel="icon" href="assets/logo-atenea-transparente.png">
<link rel="canonical" href="https://ateneapiuraperu.org/{canon}">
<meta property="og:url" content="https://ateneapiuraperu.org/{canon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/atenea.css">
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
"""

LD = """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"NGO","name":"Fundación Atenea","alternateName":"Atenea Piura",
"url":"https://ateneapiuraperu.org","logo":"https://ateneapiuraperu.org/assets/logo-atenea-transparente.png",
"image":"https://ateneapiuraperu.org/assets/og-atenea.jpg",
"description":"Fundación sin fines de lucro con sede en Piura que acompaña a mujeres, varones, niñas, niños y familias en situación de vulnerabilidad en todo el Perú.",
"email":"contacto@ateneapiuraperu.org","nonprofitStatus":"Nonprofit",
"address":{"@type":"PostalAddress","streetAddress":"Jr. Circunvalación 1384","addressLocality":"Piura","addressRegion":"Piura","addressCountry":"PE"},
"areaServed":{"@type":"Country","name":"Perú"},
"knowsAbout":["Violencia contra la mujer","Violencia familiar","Atención psicológica a varones","Niñez","Salud","Orientación legal","Ayuda humanitaria"]}
</script>"""

def header(cur):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a></li>' for h,t in NAV)
    return f"""<header class="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Fundación Atenea, inicio"><img src="assets/logo-atenea-transparente.png" alt="Fundación Atenea" width="146" height="56"></a>
    <nav aria-label="Principal"><ul class="nav">{items}</ul></nav>
    <a class="btn btn-mag" href="involucrate.html#donar">Donar</a>
    <details class="menu"><summary>Menú</summary><ul>{items}<li><a href="involucrate.html#donar">Donar</a></li></ul></details>
  </div>
</header>
<main id="contenido">
"""

FOOT = f"""</main>
<footer class="foot">
  <div class="wrap">
    <p class="big">Desde Piura, <span>juntos</span><br>llegamos más lejos.</p>
    <div class="foot-cols">
      <div><span class="logo-w"><img src="assets/logo-atenea-blanco.png" alt="Fundación Atenea" width="166" height="64"></span></div>
      <div><h4>Fundación</h4><ul><li><a href="nosotros.html">Nosotros</a></li><li><a href="programas.html">Programas</a></li><li><a href="historias.html">Historias</a></li><li><a href="transparencia.html">Transparencia y estatuto</a></li><li><a href="consultorias.html">Consultorías</a></li></ul></div>
      <div><h4>Participa</h4><ul><li><a href="involucrate.html#donar">Donar</a></li><li><a href="involucrate.html#voluntariado">Voluntariado</a></li><li><a href="involucrate.html#alianzas">Alianzas</a></li><li><a href="contacto.html">Contacto</a></li></ul></div>
      <div><h4>Contacto</h4><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{ADDR}</li><li>{HOURS}</li></ul></div>
    </div>
    <div class="legal">
      <span>© 2026 Fundación Atenea · Piura, Perú · En trámite de inscripción registral</span>
      <span><a href="privacidad.html">Privacidad</a> · <a href="terminos.html">Términos</a> · <a href="reclamaciones.html">Libro de Reclamaciones</a></span>
    </div>
  </div>
</footer>
<script src="assets/atenea.js"></script>
</body>
</html>
"""

def crumb(*parts):
    out = ['<a href="index.html">Inicio</a>']
    for p in parts:
        out.append(f'<a href="{p[0]}">{p[1]}</a>' if isinstance(p, tuple) else p)
    return '<nav class="crumb" aria-label="Ruta de navegación">' + '<span aria-hidden="true">/</span>'.join(out) + '</nav>'

def phero(crumbs, h1, lead, side="", img=None, cap=None):
    media = (f'<figure class="pimg"><img src="assets/img/{img}" alt="" width="1400" height="560"><figcaption>{cap or "Fotografía referencial. Se reemplazará por imágenes propias con consentimiento informado."}</figcaption></figure>'
             if img else '<div class="pband" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>')
    return f"""<section class="phero"><div class="wrap">
  {crumb(*crumbs)}
  <h1>{h1}</h1>
  <div class="meta"><p class="lead">{lead}</p><div class="side">{side}</div></div>
  {media}
</div></section>
"""

def shead(num, eyebrow, h2, p="", cls="h2"):
    return f'<div class="shead"><div><p class="eyebrow"><b>{num}</b> {eyebrow}</p><h2 class="{cls}">{h2}</h2></div>{f"<p class=\"lead\">{p}</p>" if p else ""}</div>'

def cta(h="Hoy alguien necesita que <span class=\"ital\">no lo dejemos solo.</span>"):
    return f"""<section class="cta"><div class="wrap">
  <h2>{h}</h2>
  <div class="btns"><a class="btn btn-main" href="involucrate.html#donar">Donar ahora →</a><a class="btn btn-line" href="contacto.html">Contáctanos</a></div>
</div></section>
"""

def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in items) + '</div>'

FAQ = [
 ("¿La ayuda de la fundación tiene algún costo?","No. Toda la orientación y el apoyo que brindamos son gratuitos y confidenciales. Nunca te pediremos dinero a cambio de ayuda."),
 ("¿Cómo sé que mi donación llega a quien la necesita?","Publicaremos estados financieros y una memoria anual con resultados, personas atendidas y uso de los fondos. Solo recibiremos donaciones por los canales oficiales publicados en esta web, que aún no están habilitados."),
 ("¿La fundación está formalmente constituida?","La Fundación Atenea está en trámite de inscripción registral (SUNARP y Consejo de Supervigilancia de Fundaciones). Cuando concluya, publicaremos los documentos en la sección de Transparencia."),
 ("¿Quién puede pedir ayuda?","Mujeres y varones en situación de violencia o abandono, niñas y niños en riesgo, personas enfermas sin recursos y familias en situación de vulnerabilidad, desde Piura y a distancia en todo el Perú. Escríbenos y evaluamos tu caso sin compromiso."),
 ("¿Cómo puedo ser voluntaria, voluntario o aliado?","Escríbenos desde la página de contacto contándonos tu profesión o la de tu organización. Buscamos profesionales de salud, derecho, psicología, educación y comunicación, además de empresas e instituciones."),
]

STEPS = """<div class="steps">
  <div class="step"><b>01</b><h3>Nos cuentas tu caso</h3><p>Por el formulario, por correo o a distancia. Te escuchamos sin juicios y con total reserva.</p></div>
  <div class="step"><b>02</b><h3>Evaluamos tu situación</h3><p>Una profesional revisa contigo qué necesitas: salud, orientación, ayuda material o acompañamiento.</p></div>
  <div class="step"><b>03</b><h3>Te acompañamos</h3><p>Activamos el apoyo, te conectamos con los servicios que correspondan y hacemos seguimiento.</p></div>
</div>"""

PROGRAMS = [
 ("programa-mujeres.html","Mujeres que avanzan","mujeres.jpg","Acompañamiento a mujeres en situación de violencia, abandono o jefatura de hogar, hasta su autonomía económica.","var(--magenta)"),
 ("programa-varones.html","Varones y familias","orientacion.jpg","Orientación psicológica, legal y social para varones que sufren maltrato, y apoyo a las familias para convivir sin violencia.","var(--coral)"),
 ("programa-ninez.html","Niñez protegida","ninez.jpg","Nutrición, refuerzo escolar y espacios de cuidado para niñas y niños mientras sus familias se recuperan.","var(--amber)"),
 ("programa-salud.html","Salud y acompañamiento","salud.jpg","Medicamentos, exámenes, traslados y compañía para personas enfermas sin recursos.","var(--sky)"),
 ("programa-orientacion.html","Orientación gratuita","orientacion.jpg","Asesoría legal, psicológica y social, presencial o a distancia, con profesionales habilitados.","var(--coral)"),
 ("programa-ayuda.html","Ayuda humanitaria","ayuda.jpg","Kits, salud y reconstrucción para familias afectadas por lluvias y emergencias en la región.","var(--violet)"),
]

def prog_cards():
    return '<div class="pgrid">' + "".join(
        f'<a class="pcard" href="{h}"><img src="assets/img/{im}" alt="" width="1400" height="933"><span class="pn"><span>0{i+1}</span><span>Ver programa →</span></span><h3>{t}</h3><p>{d}</p></a>'
        for i,(h,t,im,d,c) in enumerate(PROGRAMS)) + '</div>'

def prog_rows(exclude=None):
    out = []
    i = 0
    for h,t,im,d,c in PROGRAMS:
        if h == exclude: continue
        i += 1
        out.append(f'<a class="row" href="{h}"><span class="n">0{i}</span><h3>{t}</h3><p class="body">{d}</p><span class="go">Ver programa →</span></a>')
    return '<div class="rows">' + "".join(out) + '</div>'

PAGES = {}

# ---------------- INICIO ----------------
PAGES["index.html"] = ("Fundación Atenea · Piura, Perú", "Fundación sin fines de lucro con sede en Piura que acompaña a mujeres, varones, niñas, niños y familias en situación de vulnerabilidad en todo el Perú.", "index.html", f"""
<section class="fb">
  <img src="assets/img/portada.jpg" alt="Una madre abrazando a su hija (fotografía referencial)" width="1400" height="933" fetchpriority="high">
  <span class="tag-i">Fundación sin fines de lucro · Sede en Piura · Todo el Perú</span>
  <div class="wrap">
    <h1>Juntos por un <span class="ital">mejor mañana.</span></h1>
    <div class="fb-meta">
      <p>Acompañamos a mujeres, varones, niñas, niños y familias que enfrentan violencia, enfermedad o pobreza, con orientación gratuita y confidencial, apoyo concreto y seguimiento. Nadie debería cargar solo lo que puede cargarse entre todos.</p>
      <div class="btns"><a class="btn btn-main" href="contacto.html">Necesito ayuda →</a><a class="btn btn-line" href="involucrate.html">Quiero ayudar</a></div>
    </div>
  </div>
</section>

<section class="sec tight bg-white"><div class="wrap">
  <div class="trust">
    <div><i></i><b>Atención gratuita</b><span>Ninguna persona paga por la ayuda que recibe.</span></div>
    <div><i></i><b>Confidencial</b><span>Datos protegidos por la Ley N.º 29733.</span></div>
    <div><i></i><b>Mujeres y varones</b><span>Atendemos a toda persona en situación de vulnerabilidad.</span></div>
    <div><i></i><b>Todo el Perú</b><span>Sede en Piura y orientación a distancia en todo el país.</span></div>
  </div>
</div></section>

<section class="sec"><div class="wrap g12">
  <p class="eyebrow" style="grid-column:1/4"><b>01</b> Dónde estamos hoy</p>
  <div style="grid-column:4/13">
    <p class="statement">Atenea está en sus primeros pasos. <em>Todavía no tenemos cifras de actividad ni testimonios que mostrar, y no los vamos a inventar.</em> Cada logro se publicará aquí, con fecha y con evidencia.</p>
    <div class="road" style="margin-top:72px">
      <div class="st on"><i></i><span class="pill">En curso</span><h3>Constitución e inscripción</h3><p>Escritura pública y trámite de inscripción en SUNARP y en el Consejo de Supervigilancia de Fundaciones.</p></div>
      <div class="st"><i></i><span class="pill">Próximamente</span><h3>Consejo, equipo y aliados</h3><p>Designación del Consejo de Administración y convenios con universidades y colegios profesionales.</p></div>
      <div class="st"><i></i><span class="pill">Próximamente</span><h3>Primeras campañas</h3><p>Orientación gratuita, salud y ayuda humanitaria, con voluntariado capacitado.</p></div>
      <div class="st"><i></i><span class="pill">Próximamente</span><h3>Primer informe público</h3><p>Resultados, personas atendidas y estados financieros, publicados en esta web.</p></div>
    </div>
  </div>
</div></section>

<section class="sec bg-white"><div class="wrap g12">
  <p class="eyebrow" style="grid-column:1/4"><b>02</b> Por qué existimos</p>
  <div style="grid-column:4/13">
    <p class="statement">En Piura, más de una de cada cuatro personas vive en pobreza. Detrás de esa cifra hay <em>mujeres que sostienen hogares solas</em>, varones que sufren maltrato en silencio, niñas y niños con anemia y familias que enfrentan una enfermedad sin red. Atenea nace en Piura para ser esa red y quiere serlo en todo el Perú.</p>
    <div class="facts f3" style="margin-top:72px">
      <div><strong>28,1 %</strong><span>de la población de Piura en pobreza monetaria; el promedio nacional es 25,7 %.</span><small>INEI, 2025</small></div>
      <div><strong>4 578</strong><span>casos de violencia atendidos por los CEM de Piura entre enero y julio de 2026.</span><small>MIMP, Programa Warmi Ñan</small></div>
      <div><strong>43,7 %</strong><span>de niñas y niños de 6 a 35 meses en Piura tiene anemia.</span><small>INEI, ENDES 2025</small></div>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  {shead("03","Programas",'Seis frentes, <span class="ital mag">una misma familia.</span>',"Cada caso entra por una puerta, pero se atiende completo: una persona que llega por violencia suele necesitar también salud, escuela para sus hijos y un ingreso propio.")}
  {prog_cards()}
</div></section>

<section class="band">
  <img src="assets/img/costa.jpg" alt="Costa desértica del norte del Perú (fotografía referencial)" width="2000" height="1125">
  <div class="wrap">
    <p class="eyebrow" style="color:rgba(255,255,255,.75)"><b style="color:#F6E08A">Piura</b> Costa norte del Perú</p>
    <h2 class="h2" style="margin-top:20px">Del desierto al mar, <span class="ital">nadie se queda atrás.</span></h2>
    <p>Nacemos en Piura y trabajaremos con campañas en sus ocho provincias y orientación a distancia para personas de todo el Perú.</p>
  </div>
</section>

<section class="sec bg-white"><div class="wrap">
  {shead("04","Cómo ayudar",'Hay muchas formas <span class="ital">de sumar.</span>',"Estamos construyendo la red desde el inicio. Tu aporte puede ser tiempo, conocimiento o recursos.")}
  <div class="cols">
    <div class="col"><span class="k">Dona</span><h3>Tu aporte, en ayuda concreta</h3><p>Los canales oficiales de donación se habilitarán al concluir la inscripción. Te avisaremos aquí y por correo.</p><p><a class="tlink" href="involucrate.html#donar">Ver cómo donar →</a></p></div>
    <div class="col"><span class="k">Voluntariado</span><h3>Tu tiempo y tu profesión</h3><p>Salud, derecho, psicología, trabajo social, educación y comunicación: sumamos profesionales y estudiantes.</p><p><a class="tlink" href="involucrate.html#voluntariado">Quiero ser voluntaria/o →</a></p></div>
    <div class="col"><span class="k">Alianzas</span><h3>Empresas e instituciones</h3><p>Programas de responsabilidad social, convenios y consultorías: lo recaudado va íntegro a los programas.</p><p><a class="tlink" href="involucrate.html#alianzas">Ser aliado →</a></p></div>
  </div>
</div></section>

<section class="sec bg-sand"><div class="wrap split">
  <div class="l">
    <p class="eyebrow"><b>05</b> Estatuto y transparencia</p>
    <h2 class="h2" style="margin-top:28px">Las reglas <span class="ital">que nos damos.</span></h2>
  </div>
  <div class="r">
    <p class="lead" style="color:var(--ink)">La Fundación Atenea es una persona jurídica sin fines de lucro, con domicilio en Piura, regida por el Código Civil y supervisada por el Consejo de Supervigilancia de Fundaciones. Su patrimonio se destina solo a sus fines y no se reparte entre quienes la dirigen.</p>
    <div class="btns" style="margin-top:36px"><a class="btn btn-main" href="transparencia.html#estatuto">Leer el estatuto</a><a class="btn btn-line" href="transparencia.html">Transparencia</a></div>
  </div>
</div></section>

<section class="sec bg-white"><div class="wrap split">
  <div class="l">
    <p class="eyebrow"><b>06</b> Contacto</p>
    <h2 class="h2" style="margin-top:28px">Escríbenos. <span class="ital mag">Respondemos.</span></h2>
    <dl class="kv" style="margin-top:48px">
      <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      <div><dt>Sede</dt><dd>{ADDR} · Perú</dd></div>
      <div><dt>Atención</dt><dd>{HOURS}</dd></div>
    </dl>
  </div>
  <div class="r">{{FORM}}</div>
</div></section>
""")

CONTACT_FORM = """<form class="form" name="contacto" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mail="Consulta desde la web" novalidate>
  <input type="hidden" name="form-name" value="contacto"><p hidden><label>No llenar: <input name="bot-field"></label></p>
  <div class="f full"><span class="flabel" id="motivo-l">Motivo</span>
    <div class="chips" role="radiogroup" aria-labelledby="motivo-l">
      <input type="radio" name="motivo" id="m1" value="Necesito ayuda" checked><label for="m1">Necesito ayuda</label>
      <input type="radio" name="motivo" id="m2" value="Quiero donar"><label for="m2">Donar</label>
      <input type="radio" name="motivo" id="m3" value="Voluntariado"><label for="m3">Voluntariado</label>
      <input type="radio" name="motivo" id="m4" value="Alianza o consultoría"><label for="m4">Alianza o consultoría</label>
      <input type="radio" name="motivo" id="m5" value="Prensa"><label for="m5">Prensa</label>
    </div>
  </div>
  <div class="f"><label for="nombre">Nombre</label><input id="nombre" name="nombre" autocomplete="name" required></div>
  <div class="f"><label for="contacto">Teléfono o correo</label><input id="contacto" name="contacto" autocomplete="email" required></div>
  <div class="f full"><label for="mensaje">Mensaje</label><textarea id="mensaje" name="mensaje" required></textarea></div>
  <label class="consent"><input type="checkbox" name="autorizo" value="si" required> Autorizo el tratamiento de mis datos conforme a la Ley N.º 29733, solo para atender mi consulta.</label>
  <div class="send"><button class="btn btn-main" type="submit">Enviar mensaje →</button><small role="status">Respondemos en 48 horas hábiles.</small></div>
  <p class="callout" style="grid-column:1/-1;margin:0"><strong>¿Estás en peligro ahora?</strong> Llama a la Línea 100 (gratuita, 24 horas) o a la Policía al 105.</p>
</form>"""

# ---------------- NOSOTROS ----------------
PAGES["nosotros.html"] = ("Nosotros · Fundación Atenea", "Quiénes somos: una fundación piurana al lado de quienes atraviesan sus momentos más difíciles.", "nosotros.html",
phero(["Nosotros"], 'Cada persona es una pieza. <span class="ital mag">Juntas, un mosaico.</span>',
 "La Fundación Atenea nace en Piura para estar al lado de quienes atraviesan sus momentos más difíciles: una enfermedad sin recursos, una situación de violencia, el abandono o la pobreza.",
 '<a class="btn btn-main" href="#equipo">Cómo nos organizamos</a><a class="btn btn-line" href="transparencia.html#estatuto">Leer el estatuto</a>', "mujeres.jpg") + f"""
<section class="sec"><div class="wrap g12">
  <p class="eyebrow" style="grid-column:1/4"><b>01</b> Propósito</p>
  <div style="grid-column:4/13">
    <p class="statement">Como el mosaico de nuestro logo, creemos que cada persona que ayudamos, cada voluntaria y cada aliado <em>suman color a una misma causa</em>: que nadie enfrente sola lo que puede enfrentarse acompañada.</p>
    <div class="cols c2" style="margin-top:72px">
      <div class="col"><span class="k">Misión</span><h3>Estar presentes</h3><p>Brindar apoyo, acompañamiento y oportunidades a mujeres, varones, niñas, niños y familias en situación de vulnerabilidad en el Perú.</p></div>
      <div class="col"><span class="k">Visión</span><h3>Ser referente</h3><p>Ser la fundación referente en el Perú en asistencia social cercana, transparente y con impacto medible.</p></div>
    </div>
  </div>
</div></section>

<section class="sec bg-ink"><div class="wrap">
  {shead("02","Valores",'Cinco palabras <span class="ital cor">que se cumplen.</span>')}
  <div class="rows">
    <div class="row"><span class="n">01</span><h3>Empatía</h3><p class="body">Escuchamos antes de proponer. Cada historia es distinta.</p></div>
    <div class="row"><span class="n">02</span><h3>Dignidad</h3><p class="body">Ayudar nunca significa decidir por la otra persona.</p></div>
    <div class="row"><span class="n">03</span><h3>Transparencia</h3><p class="body">Rendimos cuentas de cada sol y de cada acción.</p></div>
    <div class="row"><span class="n">04</span><h3>Compromiso</h3><p class="body">Acompañamos hasta que la familia pueda caminar sola.</p></div>
    <div class="row"><span class="n">05</span><h3>Respeto</h3><p class="body">Tratamos a cada persona con dignidad, sin importar quién sea.</p></div>
  </div>
</div></section>

<section class="sec bg-white" id="equipo"><div class="wrap">
  {shead("03","Cómo nos organizamos",'Un gobierno claro, <span class="ital">áreas con función.</span>',"Estos son los órganos y las áreas previstos en el estatuto y en nuestro organigrama. Los nombres se publicarán cuando concluya la inscripción.")}
  <div class="cols">
    <div class="col"><span class="k">Gobierno</span><h3>Consejo de Administración</h3><p>Tres miembros (presidencia, vicepresidencia y secretaría), con cargos ad honorem. Dirige la fundación y aprueba sus estados financieros.</p></div>
    <div class="col"><span class="k">Gestión</span><h3>Gerencia General</h3><p>Representa legalmente a la fundación, ejecuta las decisiones del Consejo y presenta los estados financieros y la memoria anual.</p></div>
    <div class="col"><span class="k">Atención</span><h3>Programas</h3><p>Salud, mujeres, varones y familias, niñez, orientación gratuita y ayuda humanitaria, con profesionales habilitados.</p></div>
    <div class="col"><span class="k">Recursos</span><h3>Administración y finanzas</h3><p>Contabilidad externa, tesorería y registro de cada donación.</p></div>
    <div class="col"><span class="k">Red</span><h3>Alianzas y voluntariado</h3><p>Convenios con universidades y colegios profesionales, y voluntariado capacitado.</p></div>
    <div class="col"><span class="k">Confianza</span><h3>Ética y datos personales</h3><p>Atiende quejas y reclamos y cuida el tratamiento de los datos conforme a la Ley N.º 29733.</p></div>
  </div>
</div></section>

<section class="sec bg-sand"><div class="wrap">
  {shead("04","Cómo trabajamos",'Serio, cercano <span class="ital">y medible.</span>')}
  <div class="cols c4">
    <div class="col"><span class="k">Pilar 1</span><h3>Institucionalidad</h3><p>Constitución por escritura pública y trámite de inscripción en SUNARP y en el Consejo de Supervigilancia de Fundaciones.</p></div>
    <div class="col"><span class="k">Pilar 2</span><h3>Aliados y voluntariado</h3><p>Universidades, colegios profesionales, empresas e instituciones de Piura y de todo el país.</p></div>
    <div class="col"><span class="k">Pilar 3</span><h3>Campañas en territorio</h3><p>Salud, ayuda humanitaria y orientación gratuita, empezando por las provincias de Piura.</p></div>
    <div class="col"><span class="k">Pilar 4</span><h3>Rendición de cuentas</h3><p>Resultados, personas atendidas y estados financieros que se publicarán en esta web.</p></div>
  </div>
</div></section>

<section class="sec bg-white"><div class="wrap">
  {shead("05","Agenda 2030",'Alineados con los <span class="ital">ODS.</span>')}
  <div class="facts">
    <div><strong>ODS 1</strong><span>Fin de la pobreza</span></div>
    <div><strong>ODS 3</strong><span>Salud y bienestar</span></div>
    <div><strong>ODS 5</strong><span>Igualdad de género</span></div>
    <div><strong>ODS 10</strong><span>Reducción de las desigualdades</span></div>
  </div>
</div></section>
""" + cta())

# ---------------- PROGRAMAS ----------------
PAGES["programas.html"] = ("Programas · Fundación Atenea", "Seis líneas de acción para acompañar a mujeres, varones, niñas, niños, personas enfermas y familias en todo el Perú.", "programas.html",
phero(["Programas"], 'Seis formas de <span class="ital mag">estar presentes.</span>',
 "Mujeres, niñez, salud, orientación y ayuda humanitaria. Toda la atención es gratuita y confidencial.",
 '<a class="btn btn-main" href="contacto.html">Solicitar apoyo →</a><small>En emergencias: Línea 100 · Policía 105</small>') + f"""
<section class="sec bg-white"><div class="wrap">
  {shead("01","Qué hacemos",'Elige <span class="ital mag">por dónde entrar.</span>',"Cada programa tiene su puerta, pero trabajamos el caso completo con la familia.")}
  {prog_cards()}
</div></section>
<section class="sec bg-ink"><div class="wrap">
  {shead("02","¿Necesitas ayuda?",'No tienes que hacerlo solo ni sola. <span class="ital cor">Así te acompañamos.</span>',"Tus datos se protegen conforme a la Ley N.º 29733.")}
  {STEPS}
  <div class="btns" style="margin-top:56px"><a class="btn btn-main" href="contacto.html">Solicitar apoyo</a><a class="btn btn-line" href="mailto:ayuda@ateneapiuraperu.org">Escribir por correo</a></div>
</div></section>
<section class="sec"><div class="wrap">
  {shead("03","Piura en cifras",'La realidad <span class="ital">que queremos cambiar.</span>',"Detrás de cada cifra hay una mujer, un varón, una niña o un paciente que necesita apoyo.")}
  <div class="facts">
    <div><strong>28,1 %</strong><span>de la población de Piura vive en pobreza monetaria.</span><small>INEI, 2025</small></div>
    <div><strong>4 578</strong><span>casos de violencia atendidos por los CEM de Piura, enero–julio 2026.</span><small>MIMP, Warmi Ñan</small></div>
    <div><strong>48,6 %</strong><span>de las mujeres de Piura que han tenido pareja sufrió violencia de ella alguna vez.</span><small>MIMP, Warmi Ñan</small></div>
    <div><strong>43,7 %</strong><span>de niñas y niños de 6 a 35 meses tiene anemia.</span><small>INEI, ENDES 2025</small></div>
  </div>
</div></section>
<section class="sec bg-white"><div class="wrap">
  {shead("04","Cobertura",'Desde Piura <span class="ital">a todo el país.</span>',"Nacemos en Piura, con campañas previstas en sus ocho provincias y orientación a distancia para todo el Perú.")}
  <div class="cols c4">""" + "".join(f'<div class="col"><span class="k">Provincia</span><h3>{p}</h3></div>' for p in ["Piura","Sullana","Paita","Talara","Sechura","Morropón","Ayabaca","Huancabamba"]) + """</div>
</div></section>
""" + cta())

def program(file, name, lead, img, offers, who, needs, quote, cite, h1, story=None):
    offers_html = "".join(f'<div class="col"><h3>{t}</h3><p>{d}</p></div>' for t,d in offers)
    who_html = "".join(f"<li>{w}</li>" for w in who)
    needs_html = "".join(f"<li>{n}</li>" for n in needs)
    PAGES[file] = (f"{name} · Fundación Atenea", lead, "programas.html",
    phero([("programas.html","Programas"), name], h1, lead,
      f'<a class="btn btn-main" href="contacto.html">Solicitar apoyo →</a><a class="btn btn-line" href="mailto:ayuda@ateneapiuraperu.org">Escribir por correo</a>', img) + f"""
<section class="sec"><div class="wrap">
  {shead("01","Qué ofrecemos",'Así <span class="ital">te apoyamos.</span>')}
  <div class="cols c4">{offers_html}</div>
</div></section>
<section class="sec bg-white"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>02</b> A quién ayudamos</p><h2 class="h2-s" style="margin:28px 0 40px">¿Este programa <span class="ital">es para ti?</span></h2><ul class="list">{who_html}</ul></div>
  <div class="r"><p class="eyebrow"><b>03</b> Requisitos</p><h2 class="h2-s" style="margin:28px 0 40px">Qué <span class="ital">necesitas.</span></h2><ul class="list amber">{needs_html}</ul>
  <p class="callout">La atención es gratuita y confidencial. Si te falta algún documento, igual te escuchamos.</p></div>
</div></section>
<section class="sec bg-ink"><div class="wrap">
  {shead("04","Cómo acceder",'Tres pasos <span class="ital cor">simples.</span>')}
  {STEPS}
</div></section>
{story or '''<section class="sec bg-white"><div class="wrap">
  <p class="eyebrow"><b>05</b> Nuestro compromiso</p>
  <p class="statement" style="margin-top:40px">Te escuchamos sin juicios y con reserva. <em>Este programa está en etapa de inicio:</em> la atención se activará a medida que concluya la inscripción de la fundación y se complete la red de profesionales.</p>
  <p class="callout" style="margin-top:40px"><strong>¿Es una emergencia?</strong> Llama a la Línea 100 (gratuita, 24 horas) o a la Policía al 105. Si quieres que te avisemos cuando el programa esté activo, escríbenos desde la página de contacto.</p>
</div></section>'''}
<section class="sec"><div class="wrap">
  {shead("06","Otros programas",'Conoce <span class="ital">también.</span>')}
  {prog_rows(exclude=file)}
</div></section>
""" + cta())

program("programa-mujeres.html","Mujeres que avanzan",
 "Apoyamos a mujeres en situación de violencia, abandono o jefatura de hogar para que recuperen su seguridad y su autonomía económica.",
 "mujeres.jpg",
 [("Acompañamiento en casos de violencia","Orientación, acompañamiento a denuncias y articulación con el CEM y la Policía."),("Apoyo psicológico","Sesiones individuales y grupos de apoyo con psicólogas especializadas."),("Capacitación","Talleres de oficios, habilidades digitales y educación financiera."),("Emprendimiento","Capital semilla, asesoría y ferias para vender sus productos.")],
 ["Mujeres víctimas de violencia física, psicológica, sexual o económica.","Madres jefas de hogar en situación de pobreza.","Mujeres en situación de abandono."],
 ["DNI (si no lo tienes, igual te atendemos).","Contarnos tu situación: la atención es confidencial."],
 "Tras salir de una relación violenta, recibió acompañamiento psicológico y legal. Luego participó en el taller de repostería y hoy vende sus productos en ferias de Piura.",
 "Testimonio anónimo · Mujeres que avanzan", 'Mujeres <span class="ital mag">que avanzan.</span>')

program("programa-varones.html","Varones y familias",
 "Acompañamos a varones que sufren maltrato físico, psicológico o económico, y apoyamos a las familias para convivir sin violencia. Nadie tiene que callar lo que le pasa.",
 "orientacion.jpg",
 [("Apoyo psicológico","Sesiones individuales y grupos de apoyo con psicólogos y psicólogas colegiados."),("Orientación legal","Cómo denunciar, qué medidas de protección existen y a dónde acudir, con derivación a la Policía, el Ministerio Público y los CEM."),("Convivencia sin violencia","Talleres para parejas y familias sobre comunicación, crianza y manejo de conflictos."),("Derivación y seguimiento","Te conectamos con los servicios públicos que corresponden y hacemos seguimiento a tu caso.")],
 ["Varones víctimas de maltrato físico, psicológico o económico.","Padres y esposos que sufren amenazas o violencia en su hogar.","Familias que necesitan ayuda para convivir sin violencia."],
 ["DNI (si no lo tienes, igual te atendemos).","Contarnos tu situación: la atención es confidencial."],
 "", "", 'Varones <span class="ital mag">y familias.</span>',
 story='''<section class="sec bg-white"><div class="wrap">
  <p class="eyebrow"><b>05</b> Cómo cuidamos tu caso</p>
  <p class="statement" style="margin-top:40px">Te escuchamos sin juicios y con reserva. Un profesional colegiado evalúa tu situación primero. <em>No hacemos mediación en casos de violencia:</em> si hay riesgo, te acompañamos a las autoridades.</p>
  <p class="callout" style="margin-top:40px"><strong>¿Estás en peligro ahora?</strong> Llama a la Línea 100 (gratuita, 24 horas, atiende a mujeres y varones) o a la Policía al 105.</p>
</div></section>''')

program("programa-ninez.html","Niñez protegida",
 "Cuidamos que niñas y niños crezcan sanos, aprendan y jueguen en un entorno seguro mientras sus familias se recuperan.",
 "ninez.jpg",
 [("Nutrición","Tamizaje y prevención de anemia, suplementos y orientación alimentaria a las familias."),("Refuerzo escolar","Acompañamiento en tareas, lectura y útiles escolares para que nadie deje la escuela."),("Espacios de cuidado","Ludoteca y cuidado infantil mientras sus madres asisten a talleres o citas."),("Protección","Detección de riesgo y articulación con la DEMUNA y los servicios de protección.")],
 ["Hijas e hijos de mujeres atendidas por la fundación.","Niñas y niños de 0 a 12 años en situación de pobreza o riesgo.","Familias con niñas o niños con anemia o desnutrición."],
 ["DNI o partida de nacimiento de la niña o el niño.","Tarjeta de control de salud, si la tienen.","Acompañamiento de la madre, padre o apoderado."],
 "Su hija tenía anemia moderada. Con las visitas mensuales y la orientación en alimentación, a los seis meses sus valores ya eran normales.",
 "Luz C. · Catacaos", 'Niñez <span class="ital mag">protegida.</span>')

program("programa-salud.html","Salud y acompañamiento",
 "Acompañamos a personas enfermas sin recursos para que nadie deje su tratamiento por falta de dinero o de compañía.",
 "salud.jpg",
 [("Medicamentos y exámenes","Cubrimos total o parcialmente medicamentos, análisis e imágenes no cubiertos por el SIS."),("Traslados","Movilidad a citas, quimioterapias y hemodiálisis en Piura y, cuando se requiere, a Lima."),("Acompañamiento","Voluntariado que acompaña a pacientes y familias en hospitalizaciones y trámites."),("Orientación en salud","Afiliación al SIS, citas y derechos como paciente.")],
 ["Personas con enfermedades crónicas o graves: cáncer, insuficiencia renal, diabetes, VIH, entre otras.","Pacientes en situación de pobreza o sin red de apoyo familiar.","Adultos mayores y personas con discapacidad."],
 ["DNI del paciente.","Informe o receta médica reciente.","Declaración simple de situación económica (te ayudamos a llenarla)."],
 "Rosa fue diagnosticada con cáncer de mama y no podía pagar los exámenes complementarios. La fundación cubrió sus análisis y organizó sus traslados. Hoy continúa su tratamiento acompañada por una voluntaria.",
 "Rosa, 52 años · Castilla", 'Salud que <span class="ital mag">acompaña.</span>')

program("programa-orientacion.html","Orientación gratuita",
 "Asesoría legal, psicológica y social gratuita, presencial o a distancia, a cargo de profesionales habilitados.",
 "orientacion.jpg",
 [("Asesoría legal","Alimentos, tenencia, violencia familiar, herencias y trámites ante el Estado."),("Atención psicológica","Primera escucha, contención emocional y derivación a servicios especializados."),("Orientación social","Acceso a SIS, Pensión 65, Juntos y otros programas sociales."),("Atención a distancia","Consultas por WhatsApp o videollamada para quienes no pueden movilizarse.")],
 ["Cualquier persona en situación de vulnerabilidad de la región Piura.","Prioridad a mujeres, pacientes y adultos mayores."],
 ["Solo necesitas contarnos tu caso.","DNI y documentos relacionados, si los tienes."],
 "No sabía cómo acceder a Pensión 65. Con la orientación de la fundación reunió sus documentos y hoy recibe la pensión.",
 "Don Julio, 71 años · Piura", 'Orientación <span class="ital mag">gratuita.</span>')

program("programa-ayuda.html","Ayuda humanitaria",
 "Llevamos ayuda inmediata a familias afectadas por lluvias, inundaciones y otras emergencias en la región Piura.",
 "ayuda.jpg",
 [("Kits de emergencia","Alimentos, agua, abrigo, higiene y útiles para familias damnificadas."),("Campañas de salud","Atención básica y medicamentos en zonas afectadas."),("Voluntariado en territorio","Brigadas para distribución y apoyo comunitario."),("Reconstrucción","Apoyo para recuperar la vivienda y los medios de vida.")],
 ["Familias damnificadas por emergencias y desastres naturales.","Comunidades rurales con difícil acceso a servicios.","Albergues y comedores populares."],
 ["Registro en el padrón de la zona afectada o constancia de la autoridad local.","DNI del jefe o jefa de familia."],
 "Durante las lluvias intensas, su vivienda se inundó. Recibieron kits de alimentos e higiene y, semanas después, materiales para reparar el techo.",
 "Familia Quispe · Sechura", 'Ayuda <span class="ital mag">humanitaria.</span>')

# ---------------- HISTORIAS ----------------
PAGES["historias.html"] = ("Guías y novedades · Fundación Atenea", "Guías prácticas y novedades de la Fundación Atenea.", "historias.html",
phero(["Guías y novedades"], 'Información <span class="ital mag">que acompaña.</span>',
 "Guías prácticas para quienes enfrentan violencia, enfermedad o pobreza, y las novedades de la fundación a medida que ocurran.",
 '<a class="btn btn-main" href="#guias">Ver guías</a>') + f"""
<section class="sec" id="guias"><div class="wrap">
  {shead("01","Guías",'Información <span class="ital">que acompaña.</span>')}
  <div class="rows">
    <article class="row"><span class="n">Violencia</span><h3>¿Sufres violencia? Estos son tus canales de ayuda gratuitos</h3><div class="body"><p>Nadie tiene que enfrentar la violencia solo ni sola. En el Perú existen servicios gratuitos y confidenciales todos los días, para mujeres y para varones.</p><ul><li><strong>Línea 100:</strong> gratuita, 24 horas, orientación y derivación inmediata.</li><li><strong>Centros Emergencia Mujer:</strong> atención legal, psicológica y social gratuita; atienden también a varones.</li><li><strong>Emergencia:</strong> Policía al 105.</li></ul></div></article>
    <article class="row"><span class="n">Salud</span><h3>Cómo acompañar a un familiar durante un tratamiento</h3><div class="body"><p>Una enfermedad cambia la vida de toda la familia. Estos consejos hacen el camino más llevadero.</p><ul><li>Guarda en una carpeta recetas, resultados y citas.</li><li>Si tienes SIS, consulta qué medicamentos y exámenes están cubiertos.</li><li>Cuida también de ti: comparte las tareas y pide ayuda.</li></ul></div></article>
    <article class="row"><span class="n">Niñez</span><h3>Anemia infantil: señales y cómo prevenirla</h3><div class="body"><p>Casi la mitad de niñas y niños pequeños de Piura tiene anemia. Se puede prevenir.</p><ul><li>Controla la hemoglobina en el centro de salud desde los 6 meses.</li><li>Incluye sangrecita, hígado, bazo o pescado en sus comidas.</li><li>Pide los suplementos gratuitos de hierro en tu establecimiento de salud.</li></ul></div></article>
  </div>
</div></section>

<section class="sec bg-white"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>02</b> Novedades</p><h2 class="h2-s" style="margin-top:28px">Aquí contaremos <span class="ital">lo que hagamos.</span></h2></div>
  <div class="r"><p class="lead">Todavía no hay actividades que reportar: la fundación está en trámite de inscripción. Cuando haya campañas, talleres o convenios, los publicaremos aquí, con fecha y resultados verificables. Suscríbete al boletín para enterarte primero.</p></div>
</div></section>

{{NEWS}}
""")

NEWS = """<section class="sec bg-ink"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>·</b> Boletín</p><h2 class="h2-s" style="margin-top:28px">Buenas noticias <span class="ital cor">desde Piura.</span></h2><p class="lead" style="margin-top:24px">Una vez al mes: historias, avances y formas concretas de ayudar. Sin spam.</p></div>
  <div class="r"><form class="form inline-form" name="boletin" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mail="Suscripción al boletín" novalidate>
    <input type="hidden" name="form-name" value="boletin"><p hidden><label>No llenar: <input name="bot-field"></label></p>
    <div class="f"><label for="bn">Nombre</label><input id="bn" name="nombre" autocomplete="name" required></div>
    <div class="f"><label for="be">Correo</label><input id="be" name="correo" type="email" autocomplete="email" required></div>
    <button class="btn btn-main" type="submit">Suscribirme</button>
    <small role="status" class="muted" style="grid-column:1/-1;font-size:13px"></small>
  </form></div>
</div></section>
"""

# ---------------- INVOLÚCRATE ----------------
PAGES["involucrate.html"] = ("Involúcrate · Fundación Atenea", "Dona, ofrece tu tiempo o súmate como aliado de la Fundación Atenea.", "involucrate.html",
phero(["Involúcrate"], 'Suma tu color <span class="ital mag">al mosaico.</span>',
 "Dona, ofrece tu tiempo o súmate como aliado. Cada aporte se convierte en ayuda concreta, desde Piura y en todo el Perú.",
 '<a class="btn btn-mag" href="#donar">Donar ahora →</a><a class="btn btn-line" href="#voluntariado">Ser voluntaria/o</a>', "voluntariado.jpg") + f"""
<section class="sec bg-white" id="donar"><div class="wrap">
  {shead("01","Dona",'Tu aporte, <span class="ital">en ayuda concreta.</span>',"Aún no hemos habilitado los canales oficiales de donación: se publicarán aquí al concluir la inscripción de la fundación.")}
  <div class="cols">
    <div class="col"><span class="k">Cuentas oficiales</span><h3>Muy pronto</h3><p>Cuenta bancaria, Yape y Plin a nombre de la Fundación Atenea. Nunca recibiremos donaciones en cuentas personales.</p></div>
    <div class="col"><span class="k">En línea</span><h3>Pago con Mercado Pago</h3><p>Cuando se active, podrás donar con tarjeta de forma segura desde esta página. La fundación nunca ve los datos de tu tarjeta.</p></div>
    <div class="col"><span class="k">Constancia</span><h3>Cada aporte, documentado</h3><p>Emitiremos una constancia por cada donación y publicaremos cómo se usó.</p></div>
  </div>
  <div class="donate" id="donar-tarjeta">
    <div><p class="eyebrow"><b>En línea</b> Tarjeta</p><h3 class="h2-s" style="margin-top:16px">Dona en un minuto, <span class="ital">de forma segura.</span></h3>
    <p class="muted" style="margin-top:16px">El pago se procesa en Mercado Pago. Si todavía no está habilitado, te lo diremos al intentar donar.</p></div>
    <form class="form donate-form" novalidate>
      <div class="f full"><span class="flabel" id="monto-l">Monto (S/)</span><div class="chips" role="radiogroup" aria-labelledby="monto-l">
        <input type="radio" name="monto" id="d30" value="30"><label for="d30">S/ 30</label>
        <input type="radio" name="monto" id="d60" value="60" checked><label for="d60">S/ 60</label>
        <input type="radio" name="monto" id="d120" value="120"><label for="d120">S/ 120</label>
        <input type="radio" name="monto" id="d250" value="250"><label for="d250">S/ 250</label>
        <input type="radio" name="monto" id="dotro" value="otro"><label for="dotro">Otro</label></div></div>
      <div class="f full otro" hidden><label for="dmonto">Otro monto (S/)</label><input id="dmonto" name="otro" type="number" min="5" max="20000" step="1" inputmode="numeric"></div>
      <div class="f"><label for="dnombre">Nombre (opcional)</label><input id="dnombre" name="nombre" autocomplete="name"></div>
      <div class="f"><label for="demail">Correo para tu constancia</label><input id="demail" name="email" type="email" autocomplete="email"></div>
      <div class="send"><button class="btn btn-main" type="submit">Donar ahora →</button><small role="status"></small></div>
    </form>
  </div>
  <p class="callout"><strong>Aviso:</strong> no pedimos donaciones por llamadas ni a cuentas personales. Solo valen los canales publicados en esta página.</p>
</div></section>

<section class="sec"><div class="wrap">
  {shead("02","En qué se usará tu aporte",'Cada sol <span class="ital">tiene destino.</span>',"Estas son las áreas a las que irán los recursos, de acuerdo con el estatuto. Publicaremos los montos reales cuando existan.")}
  <div class="cols c4">
    <div class="col"><span class="k">Salud</span><h3>Medicamentos y traslados</h3><p>Apoyo a personas enfermas sin recursos para que no abandonen su tratamiento.</p></div>
    <div class="col"><span class="k">Orientación</span><h3>Atención profesional</h3><p>Asesoría legal, psicológica y social gratuita, a mujeres y varones.</p></div>
    <div class="col"><span class="k">Niñez y familia</span><h3>Nutrición y cuidado</h3><p>Prevención de anemia, refuerzo escolar y espacios seguros.</p></div>
    <div class="col"><span class="k">Emergencias</span><h3>Ayuda humanitaria</h3><p>Kits de alimentos, higiene y abrigo para familias afectadas.</p></div>
  </div>
</div></section>

<section class="sec bg-ink" id="voluntariado"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>03</b> Voluntariado</p><h2 class="h2" style="margin-top:28px">Dona tu tiempo <span class="ital cor">y tu talento.</span></h2></div>
  <div class="r"><p class="lead">Profesionales y estudiantes de salud, derecho, psicología, educación y comunicación pueden sumarse a campañas, acompañamiento hospitalario, refuerzo escolar y asesorías gratuitas.</p>
  <div class="btns" style="margin-top:36px"><a class="btn btn-main" href="contacto.html">Quiero ser voluntaria/o →</a></div></div>
</div></section>

<section class="sec bg-white" id="alianzas"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>04</b> Alianzas</p><h2 class="h2" style="margin-top:28px">Empresas <span class="ital">con propósito.</span></h2></div>
  <div class="r"><p class="lead">Construyamos programas de responsabilidad social con impacto real y medible en Piura y en todo el país, o contrata nuestras consultorías: lo recaudado se destina íntegramente a los programas.</p>
  <div class="btns" style="margin-top:36px"><a class="btn btn-main" href="contacto.html">Ser aliado</a><a class="btn btn-line" href="consultorias.html">Ver consultorías</a></div></div>
</div></section>

<section class="sec"><div class="wrap">
  {shead("05","Preguntas frecuentes",'Resolvemos <span class="ital">tus dudas.</span>')}
  {faq(FAQ)}
</div></section>
{{NEWS}}
""")

# ---------------- TRANSPARENCIA + ESTATUTO ----------------
ARTS = [
 ("Art. 1","Denominación y naturaleza","<p>La fundación se denomina «Fundación Atenea». Se constituye con fines exclusivos de beneficencia y asistencia social, sin fines de lucro, conforme al artículo 100 del Código Civil, y se rige por su estatuto y las normas aplicables.</p>"),
 ("Art. 2","Duración y domicilio","<p>Tiene duración indefinida y domicilio en el distrito, provincia y departamento de Piura. Puede establecer oficinas o representaciones en cualquier lugar del Perú o en el extranjero, si es necesario para sus fines.</p>"),
 ("Art. 3","Sin fines de lucro","<p>No distribuye, directa ni indirectamente, sus recursos, rentas, donaciones o patrimonio entre la fundadora, los administradores, los miembros de sus órganos, personas vinculadas o terceros. Todo recurso se destina a sus fines. No tiene filiación política ni religiosa.</p>"),
 ("Art. 4","Fines y objetivos","<p>Apoyar a personas y familias en situación de pobreza, vulnerabilidad, necesidad o desamparo, priorizando a personas enfermas y a mujeres en situación de vulnerabilidad, así como a otros grupos que requieran apoyo social. Entre sus objetivos:</p><ol><li>Ayuda social y humanitaria a personas de escasos recursos.</li><li>Apoyo a personas enfermas: medicamentos, exámenes, traslados y acompañamiento.</li><li>Programas de asistencia social para mujeres en situación de vulnerabilidad.</li><li>Apoyo a niñas, niños, adolescentes, personas adultas mayores y personas con discapacidad.</li><li>Campañas de entrega gratuita de alimentos, medicamentos, ropa y otros bienes de primera necesidad.</li><li>Orientación, acompañamiento y derivación a servicios de salud y asistencia social.</li><li>Prevención y sensibilización sobre salud, violencia y discriminación.</li><li>Apoyo a familias afectadas por emergencias y desastres naturales.</li></ol>"),
 ("Art. 5","Patrimonio","<p>Lo constituyen el aporte de la fundadora, las contribuciones y donaciones de personas naturales o jurídicas, nacionales o extranjeras, los bienes que adquiera y los frutos de sus bienes, siempre que se destinen íntegramente a sus fines.</p>"),
 ("Art. 9","Contabilidad","<p>Está obligada a llevar contabilidad y los libros que señalen las leyes y los que una buena administración demande.</p>"),
 ("Art. 10","Órganos de administración","<p>El Consejo de Administración y la Gerencia General. Los cargos del Consejo los designa la fundadora; la Gerencia General la designa el Consejo.</p>"),
 ("Art. 11","Consejo de Administración","<p>Lo integran tres miembros: presidencia, vicepresidencia y secretaría, con cargos de seis años. Se reúne en sesión ordinaria cada trimestre y una vez al año, dentro de los tres meses del cierre del ejercicio, para aprobar los estados financieros que presenta la Gerencia General.</p>"),
 ("Art. 14","Cargos sin lucro","<p>Los miembros del Consejo ejercen su cargo sin fines de lucro: solo pueden reembolsarse gastos necesarios, razonables y debidamente sustentados. De sus resoluciones se deja constancia en un libro de actas.</p>"),
 ("Art. 17","Gerencia General","<p>Tiene la representación legal y las facultades de gestión necesarias para administrar la fundación dentro de su objeto, conforme a las instrucciones del Consejo: dirigir las actividades, cuidar la contabilidad, presentar estados financieros y memoria anual, y contratar al personal.</p>"),
 ("Art. 18","Disolución","<p>El Consejo puede decidir la disolución y la liquidación conforme a la ley. Pagadas las obligaciones, el patrimonio remanente no se distribuye entre la fundadora, los administradores o terceros: se destina a otra entidad sin fines de lucro de beneficencia o asistencia social en el Perú.</p>"),
]
arts = "".join(f'<div class="art"><h3><small>{n}</small>{t}</h3>{b}</div>' for n,t,b in ARTS)

PAGES["transparencia.html"] = ("Transparencia y estatuto · Fundación Atenea", "Estatuto, órganos de gobierno, estados financieros y memoria anual de la Fundación Atenea.", "transparencia.html",
phero(["Transparencia"], 'Cada sol, <span class="ital mag">a la vista.</span>',
 "Publicamos nuestro estatuto y nuestra información institucional y financiera para que sepas cómo usamos cada aporte.",
 '<a class="btn btn-main" href="#estatuto">Leer el estatuto</a><a class="btn btn-line" href="#documentos">Documentos</a>') + f"""
<section class="sec bg-white" id="documentos"><div class="wrap">
  {shead("01","Documentos",'Cuentas claras, <span class="ital">confianza que crece.</span>')}
  <div class="rows">
    <a class="row" href="#estatuto"><span class="n">01</span><h3>Estatuto</h3><p class="body">Resumen del texto fundacional: fines, gobierno, patrimonio y disolución.</p><span class="go">Leer →</span></a>
    <div class="row"><span class="n">02</span><h3>Consejo de Administración</h3><p class="body">Quiénes dirigen la fundación y cómo se eligen.</p><span class="go muted">Próximamente</span></div>
    <div class="row"><span class="n">03</span><h3>Estados financieros</h3><p class="body">Ingresos y gastos, presentados al Consejo de Supervigilancia de Fundaciones.</p><span class="go muted">Al cierre 2026</span></div>
    <div class="row"><span class="n">04</span><h3>Memoria anual</h3><p class="body">Actividades, personas atendidas y resultados del año.</p><span class="go muted">Al cierre 2026</span></div>
  </div>
</div></section>

<section class="sec bg-sand" id="estatuto"><div class="wrap split">
  <div class="l sticky">
    <p class="eyebrow"><b>02</b> Estatuto</p>
    <h2 class="h2" style="margin-top:28px">Las reglas <span class="ital">que nos damos.</span></h2>
    <p class="lead" style="margin-top:28px;font-size:18px">Resumen del estatuto de la Fundación Atenea, que se rige por el Código Civil peruano y estará sujeta al Consejo de Supervigilancia de Fundaciones.</p>
    <p class="callout"><strong>Resumen informativo.</strong> El texto vinculante es el de la escritura pública. La fundación está en trámite de inscripción en SUNARP.</p>
    <div class="btns" style="margin-top:28px"><a class="btn btn-line" href="contacto.html">Solicitar texto completo</a></div>
  </div>
  <div class="r"><div class="arts">{arts}</div></div>
</div></section>

<section class="sec"><div class="wrap">
  {shead("03","Preguntas frecuentes",'Resolvemos <span class="ital">tus dudas.</span>')}
  {faq(FAQ)}
</div></section>
""" + cta())

# ---------------- CONSULTORÍAS ----------------
SERV = [("Prevención del hostigamiento sexual","Capacitaciones para empresas e instituciones conforme a la Ley N.º 27942."),
        ("Igualdad de género","Talleres y asesoría para entornos laborales más justos y seguros."),
        ("Inclusión laboral","Acompañamiento a empresas en la inclusión de personas con discapacidad."),
        ("Diagnósticos y estudios sociales","Líneas de base, investigación e indicadores sociales para Piura."),
        ("Proyectos y responsabilidad social","Diseño, ejecución y evaluación de programas para poblaciones vulnerables."),
        ("Asistencia técnica a gobiernos locales","Apoyo técnico, no partidario, en programas sociales municipales y regionales.")]
PAGES["consultorias.html"] = ("Consultorías · Fundación Atenea", "Consultorías y capacitaciones sociales para empresas e instituciones; lo recaudado financia los programas de la fundación.", "",
phero(["Consultorías"], 'Tu organización también <span class="ital mag">transforma el Perú.</span>',
 "Consultorías y capacitaciones especializadas en temas sociales. Todo lo que recibimos por estos servicios se destina íntegramente a nuestros programas.",
 '<a class="btn btn-main" href="contacto.html">Solicitar propuesta →</a>') + f"""
<section class="sec bg-white"><div class="wrap">
  {shead("01","Servicios",'Seis líneas <span class="ital">de trabajo.</span>')}
  <div class="rows">""" + "".join(f'<div class="row"><span class="n">0{i+1}</span><h3>{t}</h3><p class="body">{d}</p></div>' for i,(t,d) in enumerate(SERV)) + f"""</div>
</div></section>
<section class="sec bg-ink"><div class="wrap">
  {shead("02","Agenda 2030",'Alineados con los <span class="ital cor">ODS.</span>')}
  <div class="facts">
    <div><strong>ODS 1</strong><span>Fin de la pobreza</span></div>
    <div><strong>ODS 3</strong><span>Salud y bienestar</span></div>
    <div><strong>ODS 5</strong><span>Igualdad de género</span></div>
    <div><strong>ODS 10</strong><span>Reducción de las desigualdades</span></div>
  </div>
</div></section>
""" + cta())

# ---------------- CONTACTO ----------------
PAGES["contacto.html"] = ("Contacto · Fundación Atenea", "Escríbenos, llámanos o visítanos en Piura.", "contacto.html",
phero(["Contacto"], 'Escríbenos. <span class="ital mag">Respondemos.</span>',
 "Estamos para escucharte. Respondemos en un plazo máximo de 48 horas hábiles y tus datos son confidenciales.",
 '<a class="btn btn-main" href="mailto:ayuda@ateneapiuraperu.org">Escribir a ayuda@ →</a><small>En emergencias: Línea 100 · Policía 105</small>') + f"""
<section class="sec bg-white"><div class="wrap split">
  <div class="l">
    <p class="eyebrow"><b>01</b> Datos de contacto</p>
    <dl class="kv" style="margin-top:32px">
      <div><dt>Correo general</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      <div><dt>Necesito ayuda</dt><dd><a href="mailto:ayuda@ateneapiuraperu.org">ayuda@ateneapiuraperu.org</a></dd></div>
      <div><dt>Voluntariado</dt><dd><a href="mailto:voluntariado@ateneapiuraperu.org">voluntariado@ateneapiuraperu.org</a></dd></div>
      <div><dt>Alianzas y consultoría</dt><dd><a href="mailto:alianzas@ateneapiuraperu.org">alianzas@ateneapiuraperu.org</a></dd></div>
      <div><dt>Datos personales y reclamos</dt><dd><a href="mailto:privacidad@ateneapiuraperu.org">privacidad@ateneapiuraperu.org</a></dd></div>
      <div><dt>Sede</dt><dd>{ADDR} · Perú</dd></div>
      <div><dt>Atención</dt><dd>{HOURS}</dd></div>
    </dl>
  </div>
  <div class="r"><p class="eyebrow" style="margin-bottom:32px"><b>02</b> Formulario</p>{{FORM}}</div>
</div></section>
""")

# ---------------- LEGALES ----------------
def legal(file, title, h1, lead, sections, extra=""):
    body = "".join(f'<div class="art"><h3>{t}</h3>{b}</div>' for t,b in sections)
    PAGES[file] = (f"{title} · Fundación Atenea", lead, "",
    phero([title], h1, lead, '<small>Última actualización: octubre de 2026.</small>') + f"""
<section class="sec bg-white"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>·</b> {title}</p></div>
  <div class="r">{extra}<div class="arts legal-arts">{body}</div></div>
</div></section>
""")

legal("privacidad.html","Política de privacidad",'Política de <span class="ital mag">privacidad.</span>',"Cómo protegemos tus datos personales conforme a la Ley N.º 29733.",[
 ("Responsable",f"<p>La Fundación Atenea, con domicilio en {ADDR}, Perú, es responsable del tratamiento de los datos personales que nos proporcionas, conforme a la Ley N.º 29733 y su Reglamento.</p>"),
 ("Datos que recopilamos","<ul><li>Identificación y contacto: nombre, correo, teléfono.</li><li>Información que compartes al solicitar ayuda o escribirnos.</li><li>Datos de donaciones para emitir constancias.</li></ul>"),
 ("Finalidad","<p>Atender consultas y solicitudes de apoyo, gestionar donaciones y voluntariado, y enviarte el boletín si te suscribes.</p>"),
 ("Confidencialidad","<p>La información sobre salud o violencia se trata con estricta reserva y solo la conoce el personal que te atiende. No vendemos ni cedemos tus datos.</p>"),
 ("Tus derechos","<p>Puedes ejercer tus derechos de acceso, rectificación, cancelación y oposición escribiendo a <a href=\"mailto:privacidad@ateneapiuraperu.org\">privacidad@ateneapiuraperu.org</a> o en nuestra sede. Responderemos dentro de los plazos que establece la ley.</p>"),
 ("Proveedores que nos ayudan","<p>Para operar este sitio usamos proveedores que tratan datos en nuestro nombre y que pueden almacenarlos o procesarlos fuera del Perú: <strong>Cloudflare</strong> (alojamiento del sitio y base de datos de mensajes), <strong>Resend</strong> (envío de correos de aviso y constancias), <strong>Google Workspace</strong> (correo institucional) y <strong>Mercado Pago</strong> (pagos con tarjeta; nosotros no vemos ni guardamos los datos de tu tarjeta). El asistente virtual del sitio usa un servicio de inteligencia artificial: no escribas en él datos personales ni de salud.</p>"),
 ("Conservación","<p>Conservamos tus datos solo el tiempo necesario para la finalidad indicada y según las obligaciones legales aplicables.</p>")])
legal("terminos.html","Términos de uso",'Términos <span class="ital mag">de uso.</span>',"Condiciones de uso del sitio web de la Fundación Atenea.",[
 ("Uso del sitio","<p>Este sitio tiene fines informativos sobre la labor de la Fundación Atenea. Al usarlo, aceptas estos términos.</p>"),
 ("Contenido","<p>Los textos, logotipos e imágenes pertenecen a la fundación o se usan con autorización. No pueden reproducirse con fines comerciales sin permiso.</p>"),
 ("Información orientativa","<p>Las guías son orientativas y no reemplazan la atención profesional, médica o legal. En emergencias, llama a la Línea 100 o a la Policía (105).</p>"),
 ("Donaciones","<p>La fundación solo recibe donaciones por los canales publicados en este sitio y no responde por aportes hechos a terceros que usen su nombre.</p>"),
 ("Contacto",f'<p>Para consultas sobre estos términos, escríbenos a <a class="tlink" href="mailto:{MAIL}">{MAIL}</a>.</p>')])

PAGES["reclamaciones.html"] = ("Libro de Reclamaciones · Fundación Atenea", "Registra tu reclamo o queja. Respondemos en un plazo máximo de 15 días hábiles.", "",
phero(["Libro de Reclamaciones"], 'Libro de <span class="ital mag">Reclamaciones.</span>',
 "Conforme al Código de Protección y Defensa del Consumidor (Ley N.º 29571). Responderemos en un plazo máximo de 15 días hábiles.",
 f'<small>Fundación Atenea<br>{ADDR}, Perú</small>') + """
<section class="sec bg-white"><div class="wrap split">
  <div class="l"><p class="eyebrow"><b>·</b> Hoja de reclamación virtual</p><p class="lead" style="margin-top:28px;font-size:18px">Reclamo: disconformidad con el servicio. Queja: malestar con la atención recibida.</p></div>
  <div class="r"><form class="form" name="reclamaciones" method="POST" data-netlify="true" netlify-honeypot="bot-field" data-mail="Libro de Reclamaciones" novalidate>
    <input type="hidden" name="form-name" value="reclamaciones"><p hidden><label>No llenar: <input name="bot-field"></label></p>
    <h2 class="h2-s f full" style="font-size:28px">1. Identificación</h2>
    <div class="f full"><label for="rn">Nombre completo</label><input id="rn" name="nombre" autocomplete="name" required></div>
    <div class="f"><label for="rd">DNI / CE</label><input id="rd" name="documento" required></div>
    <div class="f"><label for="rt">Teléfono</label><input id="rt" name="telefono" autocomplete="tel" required></div>
    <div class="f full"><label for="rdo">Domicilio</label><input id="rdo" name="domicilio" autocomplete="street-address" required></div>
    <div class="f full"><label for="re">Correo electrónico</label><input id="re" name="correo" type="email" autocomplete="email" required></div>
    <h2 class="h2-s f full" style="font-size:28px;margin-top:24px">2. Detalle</h2>
    <div class="f full"><span class="flabel" id="tipo-l">Tipo</span><div class="chips" role="radiogroup" aria-labelledby="tipo-l">
      <input type="radio" name="tipo" id="t1" value="Reclamo" checked><label for="t1">Reclamo</label>
      <input type="radio" name="tipo" id="t2" value="Queja"><label for="t2">Queja</label></div></div>
    <div class="f full"><label for="rdesc">Descripción</label><textarea id="rdesc" name="descripcion" required></textarea></div>
    <div class="f full"><label for="rp">Pedido</label><textarea id="rp" name="pedido" required style="min-height:80px"></textarea></div>
    <label class="consent"><input type="checkbox" name="autorizo" value="si" required> Declaro que la información es verdadera y autorizo el tratamiento de mis datos.</label>
    <div class="send"><button class="btn btn-main" type="submit">Enviar reclamo →</button><small role="status"></small></div>
  </form></div>
</div></section>
""")

PAGES["gracias.html"] = ("Gracias · Fundación Atenea", "Gracias por tu donación.", "",
"""<section class="phero" style="padding-bottom:128px"><div class="wrap">
  <p class="eyebrow"><b>Donación</b> Fundación Atenea</p>
  <h1 style="margin-top:32px">Gracias por <span class="ital">sumar tu color.</span></h1>
  <div class="meta"><p class="lead" id="gracias-msg">Tu donación fue recibida. Te enviaremos la constancia al correo que indicaste. Con tu aporte, una mujer, un varón, una niña o un paciente en Piura no enfrenta solo su situación.</p>
  <div class="side"><a class="btn btn-main" href="index.html">Volver al inicio →</a><a class="btn btn-line" href="transparencia.html">Ver cómo usamos los fondos</a></div></div>
</div></section>
<script>(function(){var q=new URLSearchParams(location.search),s=q.get('status')||q.get('collection_status')||'',m=document.getElementById('gracias-msg');if(/pendiente|pending|in_process/.test(location.search))m.textContent='Tu pago está en proceso. Cuando se confirme, te enviaremos la constancia al correo que indicaste.';else if(/rejected|failure/.test(s))m.textContent='El pago no se completó. No se hizo ningún cobro; puedes intentarlo de nuevo desde Involúcrate o donar por Yape.'})();</script>
""")

PAGES["404.html"] = ("Página no encontrada · Fundación Atenea", "La página que buscas no existe o fue movida.", "",
"""<section class="phero" style="padding-bottom:128px"><div class="wrap">
  <p class="eyebrow"><b>404</b> Página no encontrada</p>
  <h1 style="margin-top:32px">Esta pieza <span class="ital mag">no está en el mosaico.</span></h1>
  <div class="meta"><p class="lead">La página que buscas no existe o fue movida.</p><div class="side"><a class="btn btn-main" href="index.html">Volver al inicio →</a><a class="btn btn-line" href="contacto.html">Contacto</a></div></div>
</div></section>
""")

for f,(title,desc,cur,body) in PAGES.items():
    body = body.replace("{FORM}", CONTACT_FORM).replace("{NEWS}", NEWS)
    with open(os.path.join(OUT,f),"w") as fh:
        fh.write(head(title,desc,"" if f=="index.html" else f[:-5]) + header(cur) + body + FOOT)
print(len(PAGES),"páginas")

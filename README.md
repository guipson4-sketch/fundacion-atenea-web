# Fundación Atenea · Sitio web

Sitio web institucional de la **Fundación Atenea**, fundación sin fines de lucro con sede en Piura, Perú, dedicada a la beneficencia y asistencia social, con prioridad en personas enfermas y mujeres en situación de vulnerabilidad.

## Estructura

```
index.html          Inicio
nosotros.html       Quiénes somos, cómo trabajamos, ODS
programas.html      Programas y cómo pedir ayuda
consultorias.html   Consultorías para empresas e instituciones
involucrate.html    Donar, voluntariado y alianzas
historias.html      Historias y recursos
transparencia.html  Documentos institucionales y preguntas frecuentes
contacto.html       Datos de contacto, formulario y mapa
privacidad.html     Política de privacidad (Ley 29733)
terminos.html       Términos de uso
reclamaciones.html  Libro de Reclamaciones virtual
404.html            Página no encontrada
assets/             Logo y fotografías
```

## Ver en local

Abre `index.html` en el navegador, o sirve la carpeta:

```bash
python3 -m http.server 8000
```

## Publicación

Sitio estático: se puede publicar en GitHub Pages, Netlify o Vercel sin compilación.

## Pendientes

- WhatsApp y correo oficiales (pie de página).
- Canales de donación (Yape, Plin, cuenta bancaria) al concluir la inscripción.
- Logo en SVG con fondo transparente y favicon.
- Fotografías reales de las actividades (con consentimiento informado).

## Fuentes de las cifras

- INEI, pobreza monetaria 2025 (Piura 28,1 %; nacional 25,7 %).
- MIMP – Programa Warmi Ñan: casos atendidos por los CEM de Piura, enero–julio 2026.
- INEI – ENDES 2025: anemia en niñas y niños de 6 a 35 meses en Piura.

## Fotografías

Las fotos de `assets/foto-*.jpg` son provisionales, de [Unsplash](https://unsplash.com) (licencia libre). Reemplázalas por fotos propias de la fundación cuando estén disponibles.

## Boceto: contenido de ejemplo a reemplazar

Esta versión es un boceto para aprobación. Antes de publicar con dominio propio:

- Quitar la franja amarilla «Boceto en revisión» (`class="draft-bar"`) de todas las páginas.
- Equipo y mensaje de la presidenta (`nosotros.html`): nombres, cargos y fotos de ejemplo.
- Cifras de impacto (`index.html`, atributos `data-count`), testimonios, aliados y notas de prensa: de ejemplo.
- RUC, partida registral, WhatsApp (`wa.me/51900000000`), correo, cuentas bancarias y QR de Yape/Plin: de ejemplo.
- Enlaces de redes sociales y de prensa (`href="#"`).
- Formularios de contacto, boletín y reclamaciones: conectarlos a un servicio de envío (p. ej. Formspree).

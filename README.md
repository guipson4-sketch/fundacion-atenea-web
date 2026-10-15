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
programa-*.html     Una página por programa (salud, mujeres, ayuda, orientación)
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

- Reemplazar datos ilustrativos: WhatsApp, correo, dirección, RUC, cuentas de donación,
  nombres del equipo y testimonios (todos marcados como ilustrativos).
- Quitar la franja amarilla «Versión de muestra» al publicar los datos oficiales.
- Sustituir el resumen del estatuto por el texto inscrito en SUNARP.
- Conectar los formularios a un servicio (Netlify Forms o Formspree); hoy abren el correo.
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
- Video de portada (`assets/video-portada.mp4`, de Mixkit, licencia libre) y casos de cada programa: de ejemplo.
- Zonas del mapa de cobertura (`programas.html`, lista `ZONAS` en el script del mapa).
- Enlaces de redes sociales y de prensa (`href="#"`).
- Formularios de contacto, boletín y reclamaciones: conectarlos a un servicio de envío (p. ej. Formspree).

## Asistente de soporte con IA (Gemini)

El chat de la esquina inferior derecha responde dudas sobre la fundación con la API de Gemini.
La clave **nunca** llega al navegador: la página llama a `/api/chat`, una función de Netlify
(`netlify/functions/chat.mjs`) que añade la clave y consulta a Gemini.

Publicado en https://fundacion-atenea.netlify.app. Hoy funciona con **Netlify AI Gateway**: Netlify
inyecta la clave de Gemini automáticamente y el consumo se descuenta de los créditos gratuitos de
Netlify. Para usar en su lugar el plan gratuito de Google, añade tu propia `GEMINI_API_KEY`.

Puesta en marcha con clave propia:
1. Crea una clave gratuita en Google AI Studio (aistudio.google.com → Get API key).
2. Publica el repositorio en Netlify (Add new site → Import from GitHub). `netlify.toml` ya está configurado.
3. En Netlify → Site configuration → Environment variables, añade:
   - `GEMINI_API_KEY` = tu clave (obligatoria).
   - `ALLOWED_ORIGINS` = `https://tu-dominio.org` (recomendado; bloquea llamadas desde otras webs).
   - `GEMINI_MODEL` = opcional; por defecto `gemini-3.5-flash-lite`.
4. Vuelve a desplegar.

Lo que sabe el asistente está en `netlify/functions/knowledge.mjs`; actualízalo cuando cambien
datos, programas o cuentas. Protecciones: máx. 6 mensajes por minuto por visitante, mensajes de
hasta 800 caracteres, últimos 10 turnos de historial y respuestas de hasta 500 tokens.

Importante: en el plan gratuito Google puede usar las conversaciones para mejorar sus productos.
Por eso el chat pide no compartir datos personales y deriva los casos a WhatsApp. Si llegan
consultas sensibles con frecuencia, conviene activar facturación (plan de pago) en Google AI Studio.
GitHub Pages no ejecuta funciones: para que el chat funcione, el sitio debe estar en Netlify.

## Imágenes

Todas las fotografías del sitio están en `assets/img/` con nombre fijo. Para cambiar una, reemplaza
el archivo conservando el nombre (JPG horizontal 3:2, mínimo 1600 px de ancho):

| Archivo | Dónde aparece |
|---|---|
| `portada.jpg` | Portada a pantalla completa |
| `mujeres.jpg` | Programa Mujeres que avanzan, portada (díptico) |
| `ninez.jpg` | Programa Niñez protegida |
| `salud.jpg` | Programa Salud y acompañamiento |
| `orientacion.jpg` | Programa Orientación gratuita |
| `ayuda.jpg` | Programa Ayuda humanitaria |
| `voluntariado.jpg` | Nosotros, Involúcrate |

Las actuales son de banco de imágenes y provisionales.

Fotografías de muestra: Unsplash (licencia Unsplash, uso libre). Sustituir por fotos propias con
consentimiento informado antes del lanzamiento oficial.

// Dominio canónico: www.ateneapiuraperu.org → ateneapiuraperu.org (301), conservando ruta y parámetros.
// Evita que Google indexe dos versiones del mismo sitio.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === 'www.ateneapiuraperu.org') {
    url.hostname = 'ateneapiuraperu.org';
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}

<?php
// Formularios del sitio: se guardan en MySQL y se avisa por correo.
require __DIR__ . '/_lib.php';
solo_post(); origen_ok(); limitar('form', 5);
$permitidos = [
  'contacto'      => ['motivo', 'nombre', 'contacto', 'mensaje', 'autorizo'],
  'boletin'       => ['nombre', 'correo'],
  'reclamaciones' => ['nombre', 'documento', 'telefono', 'domicilio', 'correo', 'tipo', 'descripcion', 'pedido', 'autorizo'],
];
$f = $_POST['form-name'] ?? '';
if (!isset($permitidos[$f])) out(400, ['error' => 'Formulario desconocido']);
if (!empty($_POST['bot-field'])) out(200, ['ok' => true]);           // trampa antispam
$datos = [];
foreach ($permitidos[$f] as $k) $datos[$k] = mb_substr(trim((string)($_POST[$k] ?? '')), 0, 4000);
if (in_array('autorizo', $permitidos[$f], true) && $datos['autorizo'] === '') out(400, ['error' => 'Debes autorizar el uso de tus datos.']);

$pdo = db();
if ($pdo) $pdo->prepare('INSERT INTO mensajes (formulario, datos, ip_hash) VALUES (?,?,?)')
  ->execute([$f, json_encode($datos, JSON_UNESCAPED_UNICODE), ip_hash()]);

$to = cfg()['aviso_email'] ?? '';
$enviado = false;
if ($to) {
  $txt = "Nuevo formulario «$f» en ateneapiuraperu.org\n\n";
  foreach ($datos as $k => $v) $txt .= ucfirst($k) . ": $v\n";
  $reply = filter_var($datos['correo'] ?? $datos['contacto'] ?? '', FILTER_VALIDATE_EMAIL);
  $hdr = "From: Web Fundación Atenea <no-responder@ateneapiuraperu.org>\r\nContent-Type: text/plain; charset=UTF-8" . ($reply ? "\r\nReply-To: $reply" : '');
  $enviado = @mail($to, '=?UTF-8?B?' . base64_encode("Web: nuevo mensaje ($f)") . '?=', $txt, $hdr);
}
if (!$pdo && !$enviado) out(500, ['error' => 'No pudimos registrar tu mensaje. Escríbenos por WhatsApp.']);
out(200, ['ok' => true]);

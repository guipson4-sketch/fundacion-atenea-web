<?php
// Panel privado para leer los mensajes guardados. Contraseña en config.php (admin_hash).
require __DIR__ . '/_lib.php';
session_set_cookie_params(['httponly' => true, 'secure' => true, 'samesite' => 'Strict']);
session_start();
header('X-Robots-Tag: noindex');
$hash = cfg()['admin_hash'] ?? '';
if (!$hash) { http_response_code(503); exit('Panel no configurado.'); }
if (isset($_POST['clave'])) {
  limitar('admin', 5, 300);
  if (password_verify($_POST['clave'], $hash)) { session_regenerate_id(true); $_SESSION['ok'] = 1; }
}
if (isset($_GET['salir'])) { session_destroy(); header('Location: admin.php'); exit; }
$h = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
?><!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mensajes · Fundación Atenea</title>
<style>body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#FBF7F3;color:#2A0F22}main{max-width:1100px;margin:0 auto;padding:32px 20px}
h1{color:#3E0D2C}table{width:100%;border-collapse:collapse;background:#fff}td,th{padding:10px;border-bottom:1px solid #eee;vertical-align:top;text-align:left}
th{background:#3E0D2C;color:#fff}input,button,select{font:inherit;padding:10px 14px;border-radius:10px;border:1px solid #ddd}button{background:#D6287F;color:#fff;border:0}
dl{margin:0}dt{font-weight:600;font-size:12px;text-transform:uppercase;color:#6E5566}dd{margin:0 0 6px}</style></head><body><main>
<?php if (empty($_SESSION['ok'])): ?>
<h1>Panel de mensajes</h1><form method="post"><input type="password" name="clave" placeholder="Contraseña" required autofocus> <button>Entrar</button></form>
<?php else:
  $pdo = db(); $tipo = $_GET['f'] ?? '';
  $q = $pdo ? $pdo->prepare('SELECT * FROM mensajes ' . ($tipo ? 'WHERE formulario=? ' : '') . 'ORDER BY id DESC LIMIT 300') : null;
  if ($q) $q->execute($tipo ? [$tipo] : []); ?>
<h1>Mensajes recibidos</h1>
<p><a href="?">Todos</a> · <a href="?f=contacto">Contacto</a> · <a href="?f=boletin">Boletín</a> · <a href="?f=reclamaciones">Reclamaciones</a> · <a href="?f=donacion-iniciada">Donaciones iniciadas</a> · <a href="?salir">Salir</a></p>
<?php if (!$pdo): ?><p>No hay conexión con la base de datos. Revisa config.php.</p><?php else: ?>
<table><tr><th>#</th><th>Fecha</th><th>Formulario</th><th>Datos</th></tr>
<?php foreach ($q as $r): ?><tr><td><?= (int)$r['id'] ?></td><td><?= $h($r['creado']) ?></td><td><?= $h($r['formulario']) ?></td><td><dl>
<?php foreach (json_decode($r['datos'], true) ?: [] as $k => $v): ?><dt><?= $h($k) ?></dt><dd><?= nl2br($h($v)) ?></dd><?php endforeach ?></dl></td></tr>
<?php endforeach ?></table><?php endif; endif ?>
</main></body></html>

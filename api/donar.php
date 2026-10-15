<?php
// Pasarela de donaciones: Mercado Pago Checkout Pro. El token queda en config.php.
require __DIR__ . '/_lib.php';
solo_post(); origen_ok(); limitar('donar', 10);
$token = cfg()['mp_token'] ?? '';
if (!$token) out(503, ['error' => 'Las donaciones con tarjeta se activarán muy pronto. Mientras tanto puedes donar por Yape, Plin o transferencia.']);

$b = body_json();
$monto = round((float)($b['monto'] ?? 0), 2);
if ($monto < 5 || $monto > 20000) out(400, ['error' => 'Elige un monto entre S/ 5 y S/ 20 000.']);
$email = filter_var($b['email'] ?? '', FILTER_VALIDATE_EMAIL) ?: null;
$nombre = mb_substr(trim((string)($b['nombre'] ?? '')), 0, 80);
$sitio = rtrim(cfg()['sitio'] ?? '', '/');

$pref = [
  'items' => [['id' => 'donacion', 'title' => 'Donación · Fundación Atenea', 'quantity' => 1, 'currency_id' => 'PEN', 'unit_price' => $monto]],
  'back_urls' => ['success' => "$sitio/gracias", 'pending' => "$sitio/gracias?estado=pendiente", 'failure' => "$sitio/involucrate#donar"],
  'auto_return' => 'approved', 'statement_descriptor' => 'FUND ATENEA',
  'external_reference' => 'don-' . time(), 'metadata' => ['tipo' => 'donacion', 'nombre' => $nombre],
];
if ($email) $pref['payer'] = ['email' => $email, 'name' => $nombre ?: null];
[$code, $data] = http_json('https://api.mercadopago.com/checkout/preferences', $pref, ["Authorization: Bearer $token"]);
if ($code < 200 || $code >= 300 || empty($data['init_point'])) { error_log("MercadoPago $code"); out(502, ['error' => 'No pudimos conectar con la pasarela. Intenta de nuevo o dona por Yape.']); }

if ($pdo = db()) $pdo->prepare('INSERT INTO mensajes (formulario, datos, ip_hash) VALUES (?,?,?)')
  ->execute(['donacion-iniciada', json_encode(['monto' => $monto, 'nombre' => $nombre, 'email' => $email], JSON_UNESCAPED_UNICODE), ip_hash()]);
out(200, ['url' => $data['init_point']]);

<?php
// Utilidades comunes de la API (no se accede directamente).
declare(strict_types=1);
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === '_lib.php') { http_response_code(404); exit; }

function cfg(): array {
  static $c = null;
  if ($c === null) { $f = __DIR__ . '/config.php'; $c = is_file($f) ? require $f : []; }
  return $c;
}
function out(int $status, array $body): never {
  http_response_code($status);
  header('Content-Type: application/json; charset=utf-8');
  header('Cache-Control: no-store');
  echo json_encode($body, JSON_UNESCAPED_UNICODE);
  exit;
}
function solo_post(): void { if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(405, ['error' => 'Método no permitido']); }
function origen_ok(): void {
  $o = $_SERVER['HTTP_ORIGIN'] ?? '';
  $ok = cfg()['origenes'] ?? [];
  if ($o && $ok && !in_array($o, $ok, true)) out(403, ['error' => 'Origen no permitido']);
}
function body_json(): array { $d = json_decode(file_get_contents('php://input') ?: '', true); return is_array($d) ? $d : []; }
function ip_hash(): string { return hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . '|atenea'); }

// Límite de peticiones por IP con archivos temporales (sin base de datos).
function limitar(string $clave, int $max, int $seg = 60): void {
  $dir = sys_get_temp_dir() . '/atenea-rl'; @mkdir($dir, 0700, true);
  $f = "$dir/" . $clave . '-' . ip_hash();
  $t = time(); $hits = array_filter(json_decode(@file_get_contents($f) ?: '[]', true) ?: [], fn($x) => $t - $x < $seg);
  $hits[] = $t; @file_put_contents($f, json_encode(array_values($hits)), LOCK_EX);
  if (count($hits) > $max) out(429, ['error' => 'Demasiadas solicitudes seguidas. Espera un minuto, por favor.']);
}
function db(): ?PDO {
  $c = cfg(); if (empty($c['db_name'])) return null;
  try {
    $pdo = new PDO("mysql:host={$c['db_host']};dbname={$c['db_name']};charset=utf8mb4", $c['db_user'], $c['db_pass'],
      [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    $pdo->exec("CREATE TABLE IF NOT EXISTS mensajes (
      id INT AUTO_INCREMENT PRIMARY KEY, formulario VARCHAR(40) NOT NULL, datos JSON NOT NULL,
      ip_hash CHAR(64) NOT NULL, leido TINYINT(1) NOT NULL DEFAULT 0, creado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      INDEX(formulario), INDEX(creado)) CHARACTER SET utf8mb4");
    return $pdo;
  } catch (Throwable $e) { error_log('DB: ' . $e->getMessage()); return null; }
}
function http_json(string $url, array $payload, array $headers): array {
  $ch = curl_init($url);
  curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 25,
    CURLOPT_HTTPHEADER => array_merge(['Content-Type: application/json'], $headers),
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE)]);
  $res = curl_exec($ch); $code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
  return [$code, $res === false ? null : json_decode($res, true), $res];
}

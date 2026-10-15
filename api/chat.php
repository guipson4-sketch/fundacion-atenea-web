<?php
// Asistente de soporte: la clave de Gemini queda en el servidor (config.php).
require __DIR__ . '/_lib.php';
solo_post(); origen_ok(); limitar('chat', 6);
$key = cfg()['gemini_key'] ?? '';
if (!$key || str_starts_with($key, 'PEGA_')) out(500, ['error' => 'El asistente no está configurado todavía.']);

$hist = body_json()['messages'] ?? [];
$contents = [];
foreach (array_slice(is_array($hist) ? $hist : [], -10) as $m) {
  if (!is_array($m) || !in_array($m['role'] ?? '', ['user', 'model'], true) || !is_string($m['text'] ?? null) || trim($m['text']) === '') continue;
  $contents[] = ['role' => $m['role'], 'parts' => [['text' => mb_substr($m['text'], 0, 800)]]];
}
if (!$contents || end($contents)['role'] !== 'user') out(400, ['error' => 'Falta el mensaje']);

$model = preg_replace('/[^a-z0-9.\-]/', '', cfg()['gemini_model'] ?? 'gemini-3.5-flash-lite');
[$code, $data] = http_json("https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent", [
  'systemInstruction' => ['parts' => [['text' => file_get_contents(__DIR__ . '/conocimiento.txt')]]],
  'contents' => $contents,
  'generationConfig' => ['temperature' => 0.3, 'maxOutputTokens' => 500],
], ["x-goog-api-key: $key"]);

if ($code === 429) out(429, ['error' => 'El asistente alcanzó su límite por ahora. Escríbenos por WhatsApp y te respondemos.']);
if ($code < 200 || $code >= 300 || !$data) { error_log("Gemini $code"); out(502, ['error' => 'El asistente no está disponible en este momento.']); }
$txt = trim(implode('', array_map(fn($p) => $p['text'] ?? '', $data['candidates'][0]['content']['parts'] ?? [])));
out(200, ['reply' => $txt !== '' ? $txt : 'No puedo responder eso. Escríbenos por WhatsApp y una persona del equipo te ayudará.']);

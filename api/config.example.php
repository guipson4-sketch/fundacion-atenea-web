<?php
// Copia este archivo como config.php (en la misma carpeta) y completa tus datos.
// config.php NO se sube a GitHub: contiene claves privadas.
return [
  // Gemini (aistudio.google.com > Get API key)
  'gemini_key'   => 'PEGA_AQUI_TU_CLAVE_DE_GEMINI',
  'gemini_model' => 'gemini-3.5-flash-lite',

  // Mercado Pago (Tus integraciones > Credenciales de producción > Access Token)
  'mp_token'     => '',

  // Base de datos MySQL (hPanel > Bases de datos > MySQL)
  'db_host' => 'localhost',
  'db_name' => 'u000000000_atenea',
  'db_user' => 'u000000000_atenea',
  'db_pass' => '',

  // Avisos por correo de cada formulario recibido
  'aviso_email' => 'contacto@ateneapiuraperu.org',

  // Panel de mensajes (/api/admin.php): genera el hash con  php -r "echo password_hash('TuClave', PASSWORD_DEFAULT);"
  'admin_hash' => '',

  'sitio'   => 'https://ateneapiuraperu.org',
  'origenes'=> ['https://ateneapiuraperu.org', 'https://www.ateneapiuraperu.org'],
];

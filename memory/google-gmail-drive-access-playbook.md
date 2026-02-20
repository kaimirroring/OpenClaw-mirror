# Playbook: Conectar una cuenta Google (Gmail + Drive) para MailOps en OpenClaw

Fecha: 2026-02-20
Estado: validado en producción (cuenta 1)

## Objetivo
Conectar una cuenta Google para:
- leer/modificar Gmail (clasificar/etiquetar/archivar)
- crear/editar archivos en Drive

## Resumen del flujo (end-to-end)
1. Crear proyecto en Google Cloud (ej. `OpenClaw-MailOps`).
2. Habilitar APIs: Gmail API + Drive API.
3. Configurar OAuth Consent Screen (External/testing).
4. Crear OAuth Client tipo **Desktop app** y descargar `client_secret.json`.
5. Subir `client_secret.json` al VPS en ruta segura.
6. Crear venv Python aislado e instalar dependencias Google.
7. Ejecutar flujo OAuth manual y generar `token.json`.
8. Ejecutar script de triage (`scripts/gmail_triage.py`).
9. Programar cron (cada 15 min).
10. (Opcional) One-shot de limpieza para depurar inbox inmediatamente.

---

## 1) Google Cloud (cuenta objetivo)
- Console: https://console.cloud.google.com/
- Proyecto: crear/usar uno dedicado (recomendado: `OpenClaw-MailOps`).
- APIs habilitadas:
  - Gmail API
  - Google Drive API
- OAuth Consent:
  - tipo: External (testing ok)
  - app name: `OpenClaw MailOps`
  - test user: correo de la cuenta que se conectará
- Scopes mínimos usados:
  - `https://www.googleapis.com/auth/gmail.modify`
  - `https://www.googleapis.com/auth/gmail.labels`
  - `https://www.googleapis.com/auth/drive.file`

## 2) OAuth client
- Credentials -> Create credentials -> OAuth client ID
- Tipo: Desktop app
- Descargar JSON (renombrar localmente a `client_secret.json`)

## 3) Rutas seguras en VPS
```bash
mkdir -p /home/jose/.openclaw/secrets/google
chmod 700 /home/jose/.openclaw/secrets
chmod 700 /home/jose/.openclaw/secrets/google
```

Subir desde Windows (PowerShell local):
```powershell
scp "D:\ruta\client_secret.json" jose@100.108.76.104:/home/jose/.openclaw/secrets/google/client_secret.json
```

Permisos:
```bash
chmod 600 /home/jose/.openclaw/secrets/google/client_secret.json
```

## 4) Entorno Python aislado (evita conflictos de paquetes)
```bash
python3 -m venv /home/jose/.openclaw/venvs/google-mailops
source /home/jose/.openclaw/venvs/google-mailops/bin/activate
pip install --upgrade pip
pip install google-auth google-auth-oauthlib google-api-python-client requests-oauthlib oauthlib
```

## 5) Generar token OAuth (`token.json`)
Problema conocido: en versiones nuevas no existe `run_console()`.
Solución usada: script en archivo + input interactivo.

Crear script:
`/home/jose/.openclaw/secrets/google/oauth_flow.py`

Ejecutar:
```bash
source /home/jose/.openclaw/venvs/google-mailops/bin/activate
python /home/jose/.openclaw/secrets/google/oauth_flow.py
chmod 600 /home/jose/.openclaw/secrets/google/token.json
```

Resultado esperado:
- `TOKEN_OK /home/jose/.openclaw/secrets/google/token.json`

## 6) Script de triage Gmail
Script activo:
- `/home/jose/.openclaw/workspace/scripts/gmail_triage.py`

Comportamiento actual:
- crea/usa labels `OC/*`
- clasifica correos recientes
- política conservadora: archiva low-value según reglas

## 7) Automatización por cron
```bash
*/15 * * * * /bin/bash -lc "source /home/jose/.openclaw/venvs/google-mailops/bin/activate && python /home/jose/.openclaw/workspace/scripts/gmail_triage.py" >> /home/jose/.openclaw/logs/gmail-triage.log 2>&1
```

## 8) One-shot de limpieza (a demanda)
Uso validado para depurar inbox inmediatamente:
- archivó correos etiquetados low-value (`Newsletters/Promotions/To-Review`) manteniendo labels.

## 9) Repetir para otra cuenta Google
Para conectar otra cuenta:
1. Repetir OAuth desde esa cuenta Google.
2. Guardar credenciales en ruta separada, por ejemplo:
   - `/home/jose/.openclaw/secrets/google/account2/client_secret.json`
   - `/home/jose/.openclaw/secrets/google/account2/token.json`
3. Duplicar script/cron con rutas de cuenta 2.

## 10) Notas operativas
- No borrar correos en automático en fases iniciales.
- Archivar != eliminar.
- Mantener logs para auditoría.

# OpenClaw Workspace (Respaldo de configuración)

Este repositorio guarda la configuración, memoria y personalización del asistente para poder restaurar rápido en migraciones (por ejemplo, cambio de VPS).

## Objetivo

- Tener **versionado** de toda la configuración relevante del workspace.
- Mantener **backups automáticos** con commits periódicos.
- Generar **tags semanales** como puntos de recuperación.
- Permitir **redundancia** con un segundo remoto (`mirror`) cuando esté configurado.

## Estructura y propósito de cada archivo/carpeta

### Raíz del repositorio

- `AGENTS.md`  
  Guía operativa del asistente dentro del workspace: memoria, seguridad, forma de trabajo, heartbeats y criterios de actuación.

- `SOUL.md`  
  Define la identidad/voz del asistente (estilo, límites, personalidad).

- `USER.md`  
  Perfil operativo del usuario: preferencias técnicas, infraestructura, reglas de aprobación y forma de trabajo.

- `TOOLS.md`  
  Notas locales de herramientas/entorno (atajos, dispositivos, preferencias técnicas específicas).

- `IDENTITY.md`  
  Identidad declarativa del asistente (nombre, vibra, avatar, etc.).

- `HEARTBEAT.md`  
  Checklist para tareas periódicas de heartbeat. Si está vacío, no se ejecutan chequeos periódicos adicionales.

- `README.md`  
  Este documento.

- `.gitignore`  
  Exclusiones de Git para evitar versionar archivos no deseados.

### Carpeta `memory/`

- `memory/YYYY-MM-DD-*.md`  
  Memoria diaria y notas cronológicas de contexto operativo.

### Carpeta `.openclaw/`

- `.openclaw/auto-backup.sh`  
  Script de backup automático. Hace `git add -A`, crea commit si hay cambios y hace push a `origin` y también a `mirror` si existe.

- `.openclaw/weekly-tag.sh`  
  Script de versionado semanal. Crea tag `weekly-YYYY-Www` y lo publica en `origin` y `mirror` (si existe).

- `.openclaw/auto-backup.log`  
  Log de ejecuciones automáticas del backup.

- `.openclaw/workspace-state.json`  
  Estado interno del workspace generado por OpenClaw.

## Automatizaciones configuradas

### 1) Backup automático cada 30 minutos

Cron:

```cron
*/30 * * * * /home/jose/.openclaw/workspace/.openclaw/auto-backup.sh >> /home/jose/.openclaw/workspace/.openclaw/auto-backup.log 2>&1
```

### 2) Tag semanal automático

Cron recomendado (UTC):

```cron
15 3 * * 1 /home/jose/.openclaw/workspace/.openclaw/weekly-tag.sh >> /home/jose/.openclaw/workspace/.openclaw/auto-backup.log 2>&1
```

## Redundancia con segundo repositorio (`mirror`)

Para activar espejo en un segundo repo remoto:

```bash
git remote add mirror git@github.com:TU_USUARIO/TU_REPO_REDUNDANTE.git
```

Si ya existe y quieres cambiar URL:

```bash
git remote set-url mirror git@github.com:TU_USUARIO/TU_REPO_REDUNDANTE.git
```

Una vez configurado `mirror`, los scripts empujan automáticamente backups y tags también a ese remoto.

## Restauración rápida en nuevo VPS

1. Clonar repo principal.
2. Verificar llaves SSH para push.
3. Instalar cron jobs.
4. Validar ejecución manual de scripts (`auto-backup.sh` y `weekly-tag.sh`).

## Nota de seguridad

- Usar llaves SSH dedicadas por repositorio (Deploy Keys o llave técnica separada).
- Evitar tokens globales cuando no sean necesarios.
- Proteger permisos en `~/.ssh` y revisar accesos periódicamente.

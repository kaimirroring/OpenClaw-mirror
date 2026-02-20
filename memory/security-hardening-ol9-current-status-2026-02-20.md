# Security Hardening Status - Oracle Linux 9 (2026-02-20)

| ID | Qué se debe hacer / qué resuelve | ¿Implementado en servidor actual? | Criticidad |
|---|---|---|---|
| SEC-000 | Backups de configs críticas antes de cambios (rollback rápido). | Sí: backup `sshd_config` presente y backup fail2ban creado en `/root/sec-backups/fail2ban.2026-02-20-085720`. | ⭐⭐⭐⭐☆ |
| SEC-001 | Asegurar panel OpenClaw no expuesto públicamente (`127.0.0.1:18789`) + firewall sin 18789 abierto. | Sí: OpenClaw escucha en `127.0.0.1:18789` y firewalld solo expone `ssh`. | ⭐⭐⭐⭐⭐ |
| SEC-002 | Permisos restrictivos en credenciales OpenClaw. | Sí: `/home/jose/.openclaw/credentials` en `700`, owner `jose`. | ⭐⭐⭐⭐☆ |
| SEC-003 | Hardening SSH sin romper túnel local (`-L`). | **Sí (implementado ahora)**: `00-hardening.conf` activo; `X11Forwarding no`, `AllowAgentForwarding no`, `MaxAuthTries 3`, `LoginGraceTime 30`. | ⭐⭐⭐⭐⭐ |
| SEC-004 | Firewall mínimo viable (SSH only, sin servicios extra). | Sí: zona public con `services: dhcpv6-client ssh`, sin puertos adicionales. | ⭐⭐⭐⭐⭐ |
| SEC-004.1 | Restringir SSH a IP pública fija (opcional). | No: no hay rich-rule de IP fija aplicada. | ⭐⭐⭐⭐☆ |
| SEC-005 | Fail2ban activo para sshd (bloqueo de bruteforce). | Sí: jail `sshd` activo (stats y bans visibles). | ⭐⭐⭐⭐☆ |
| SEC-006A | Acceso al panel por túnel SSH (sin exposición pública). | Parcial/Sí funcional por diseño; validar cliente Windows/NSSM desde laptop. | ⭐⭐⭐⭐☆ |
| SEC-007 | Panel OpenClaw con token + pairing. | Sí: auth `token` y eventos de `pairing required` observados. | ⭐⭐⭐⭐⭐ |
| SEC-008 | Allowlist de WhatsApp. | Sí: `allowFrom` configurado para `+19512716200`. | ⭐⭐⭐⭐☆ |
| SEC-009 | Observabilidad diaria de seguridad. | Parcial: comandos definidos; falta cron dedicado de healthcheck si se desea. | ⭐⭐⭐☆☆ |
| SEC-010 | Beneficio global (postura endurecida y controlada). | Parcial alto: base sólida aplicada; pendiente opcional SEC-004.1 y rutina diaria SEC-009. | ⭐⭐⭐⭐☆ |
| SEC-011 | Pendientes priorizados para cierre. | Parcial alto: SEC-009 ya automatizado con cron diario; pendiente opcional SEC-004.1 (restringir SSH por IP fija). | ⭐⭐⭐⭐⭐ |

## Evidence highlights
- SSH hardening effective values:
  - `x11forwarding no`
  - `allowagentforwarding no`
  - `maxauthtries 3`
  - `logingracetime 30`
- Listener status:
  - `0.0.0.0:22` (sshd)
  - `127.0.0.1:18789` (OpenClaw)
- Firewall:
  - active zone `public`, services: `ssh`, no custom ports.
- Fail2ban:
  - jail `sshd` active, historical bans recorded.
- Observabilidad diaria:
  - cron root: `10 6 * * * /usr/local/sbin/openclaw-sec-daily.sh`
  - log: `/var/log/openclaw-security/daily-YYYY-MM-DD.log`

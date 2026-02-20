# Security Hardening Control Table (Template)

Use this template for host-hardening projects (OpenClaw + SSH + firewall + fail2ban).

## Table format (keep this structure)

| ID | Qué se debe hacer / qué resuelve | ¿Implementado en servidor actual? | Criticidad |
|---|---|---|---|
| SEC-000 | [Descripción breve + para qué sirve] | [Sí / No / Parcial + evidencia corta] | ⭐⭐⭐⭐⭐ |

### Criticidad rubric
- ⭐⭐⭐⭐⭐ = crítico (exposición remota directa / acceso no autorizado)
- ⭐⭐⭐⭐☆ = alto (reduce superficie o evita escalación)
- ⭐⭐⭐☆☆ = medio (operación/observabilidad)
- ⭐⭐☆☆☆ = bajo
- ⭐☆☆☆☆ = informativo

## Mandatory response format before implementation

When user requests a specific ID, ALWAYS answer first with:

1. **Resultado general** (Estado: Sí/No/Parcial)
2. **Evidencia clave** (comandos/salidas relevantes)
3. **Comparativo vs objetivo** (tabla corta de controles)
4. **Conclusión** (qué falta exactamente)

Then wait for explicit user approval before changes.

## Execution policy
- Never implement state-changing steps before explicit approval.
- For approved steps: run with backup + validation + reload + rollback path.
- Stop after each SEC-ID and report final verification.

## Oracle Linux 9 baseline IDs
- SEC-000 Backups previos
- SEC-001 No exposición pública de panel (loopback + firewall)
- SEC-002 Permisos de credenciales OpenClaw
- SEC-003 Hardening SSH
- SEC-004 Firewall mínimo viable
- SEC-004.1 Restricción SSH por IP
- SEC-005 Fail2ban sshd jail
- SEC-006A Túnel SSH operativo
- SEC-007 Seguridad panel OpenClaw (token + pairing)
- SEC-008 Allowlist WhatsApp
- SEC-009 Observabilidad diaria
- SEC-010 Resultado global de postura
- SEC-011 Pendientes en orden

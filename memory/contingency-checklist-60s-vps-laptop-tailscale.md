# Checklist de contingencia (60s) - VPS + Laptop por Tailscale

Objetivo: validar rápidamente que, incluso tras reinicio de VPS y laptop, el acceso seguro sigue operativo.

## Paso 0 (precondición)
- Reiniciar VPS y laptop.
- Esperar 1-2 minutos tras login.

## Paso 1 - Laptop Windows (20s)
```powershell
tailscale status
ssh jose@100.108.76.104 "echo OK_TAILNET && hostname && date -u"
```
Esperado:
- nodo VPS visible en `tailscale status`
- respuesta `OK_TAILNET`

## Paso 2 - VPS (20s)
```bash
sudo systemctl is-active tailscaled firewalld sshd fail2ban
sudo firewall-cmd --zone=public --list-services
sudo firewall-cmd --zone=trusted --list-sources
```
Esperado:
- todos `active`
- `public` sin `ssh`
- `trusted` contiene `100.64.0.0/10`

## Paso 3 - OpenClaw (20s)
```bash
openclaw gateway status
openclaw status
```
Esperado:
- gateway en loopback `127.0.0.1:18789`
- estado general saludable

## Criterio final
- Si todo lo esperado se cumple -> continuidad operativa OK.
- Si falla acceso SSH por tailnet, usar rollback temporal:
```bash
sudo firewall-cmd --permanent --zone=public --add-service=ssh
sudo firewall-cmd --reload
```

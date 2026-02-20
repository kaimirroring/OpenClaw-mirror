# Manual: Conexión directa y segura Laptop (Windows 11) <-> VPS (Oracle Linux 9) con Tailscale

Last updated: 2026-02-20

## Objetivo
Mantener acceso remoto estable y seguro sin depender de IP pública fija ni configuración de router doméstico.

## Modelo de seguridad
- SSH público en internet: **cerrado** en firewall público.
- SSH permitido solo desde red privada Tailscale (`100.64.0.0/10`).
- Autenticación por identidad (cuenta Tailscale) + claves SSH.

## Implementación realizada (servidor OL9)
1. Instalación Tailscale (repo RHEL9 compatible):
   - `https://pkgs.tailscale.com/stable/rhel/9/tailscale.repo`
2. Servicio habilitado:
   - `tailscaled` activo y en autoarranque.
3. Nodo autenticado en tailnet:
   - VPS tailnet IP: `100.108.76.104`
4. Firewall endurecido:
   - Zona `trusted` con source `100.64.0.0/10`
   - Zona `public` sin servicio `ssh`
5. Backup firewall previo al cambio:
   - `/root/sec-backups/firewalld.2026-02-20-100005`

## Validaciones realizadas
- Conexión desde laptop por tailnet:
  - `ssh jose@100.108.76.104` -> OK
- `firewall-cmd --zone=public --list-all`:
  - sin `ssh`
- `firewall-cmd --zone=trusted --list-all`:
  - source `100.64.0.0/10`

## Pasos operativos para laptop Windows 11
1. Instalar Tailscale:
   - https://tailscale.com/download/windows
2. Iniciar sesión con la misma cuenta tailnet.
3. Conectar al VPS por tailnet:
   - `ssh jose@100.108.76.104`
4. (Opcional) Crear alias en PowerShell profile para acceso rápido.

## Comandos útiles (servidor)
- Estado Tailscale:
  - `sudo tailscale status`
- IP tailnet:
  - `sudo tailscale ip -4`
- Estado firewall:
  - `sudo firewall-cmd --zone=public --list-all`
  - `sudo firewall-cmd --zone=trusted --list-all`

## Rollback rápido (si se necesita abrir SSH público temporal)
```bash
sudo firewall-cmd --permanent --zone=public --add-service=ssh
sudo firewall-cmd --reload
```

## Notas
- Este enfoque evita lockout por IP dinámica del ISP.
- No requiere abrir puertos en router doméstico.
- Recomendado mantener fail2ban activo igualmente.

# Fallback Manual - SSH Tunnel (Windows 11) para OpenClaw Control UI

Objetivo: mantener una ruta alternativa al panel (`127.0.0.1:18789`) usando túnel SSH desde laptop.

## Requisitos
- Acceso SSH al VPS (por Tailscale o por regla pública restringida).
- OpenSSH client en Windows.

## Comando base
```powershell
ssh -N -L 18789:127.0.0.1:18789 jose@100.108.76.104
```

Luego abrir en navegador local:
- `http://127.0.0.1:18789/`

## Modo servicio en Windows (NSSM)
1. Instalar NSSM.
2. Crear servicio `OpenClawTunnel` con:
   - Application: `C:\Windows\System32\OpenSSH\ssh.exe`
   - Arguments: `-N -L 18789:127.0.0.1:18789 jose@100.108.76.104`
3. Start type: Automatic.

## Validación
```powershell
sc query OpenClawTunnel
curl http://127.0.0.1:18789/ | select -First 2
```

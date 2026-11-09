---
id: RUN-016
tipo: Runbook
type: Runbook
title: Exponer el stack al internet con cloudflared
description: Tunel saliente sin abrir puertos ni tocar el firewall; agnostico a credenciales.
estado: probado
dueno: rol:devops
fecha: 2026-11-09
relaciona: [DEC-005, runbooks]
status: stable
generated: copilot-agent/2026.10
---

## Disparador y objetivo

Cuando se necesita que un revisor externo alcance el stack (demo de tesis,
revision de Felipe) sin abrir puertos en el router ni modificar el firewall
del host. Objetivo: URL publica HTTPS en menos de 2 minutos. Elegido en
[DEC-005](../decisions/DEC-005-exposicion-publica-tunel.md) sobre Tailscale
Funnel por no requerir cuenta ni credenciales en modo demo.

## Procedimiento

1. Stack arriba y frontend en el puerto host `FRONTEND_PORT` (3000 local,
   39005 en el DGX): `docker ps --filter name=exam_frontend`.
2. Tunel rapido (sin credenciales ni cuenta):
   `docker run --rm -d --name exam_tunnel cloudflare/cloudflared:latest
   tunnel --url http://host.docker.internal:FRONTEND_PORT --no-autoupdate`.
   Requiere la imagen (una vez): `docker pull cloudflare/cloudflared:latest`.
3. Leer la URL de los logs: `docker logs exam_tunnel 2>&1 | Select-String
   "trycloudflare"`. Ejemplo de formato: `https://<4-palabras>.trycloudflare.com`.
4. Alternativa con credenciales (URL estable, requiere tunnel token propio,
   nunca en el repo): `docker run --rm -d --name exam_tunnel
   cloudflare/cloudflared:latest tunnel --no-autoupdate run
   --token $TUNNEL_TOKEN`. La variable va en el entorno del host o en un
   `.env` fuera de git; el runbook no la define.

## Verificacion y cierre

SPA: `Invoke-WebRequest <URL>/` -> 200. API: `<URL>/subjects` con
`Accept: application/json` -> 401 sin token (la auth sigue activa).
Con credenciales de prueba del propietario: login 200 y listado 200.
WS: `new WebSocket("wss://<URL sin https://>/ws")` -> open.
Stop: `docker rm -f exam_tunnel` (el quick tunnel muere con el contenedor;
la URL queda invalida). El propietario marca `vigente` tras una demo real.

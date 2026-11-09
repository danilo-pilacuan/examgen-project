---
id: QT-016
tipo: TestCase
type: TestCase
title: Exposicion publica via cloudflared
description: SPA, auth API y WebSocket funcionan a traves de la URL publica del tunel.
estado: aprobada
dueno: rol:propietario
fecha: 2026-11-09
relaciona: [REQ-001]
status: stable
fase: 0
generated: copilot-agent/2026.10
---

## Objetivo

Verifica que la exposicion de RUN-016 sirve el caso de uso central de
REQ-001 (seccion 9 de AGENTS.md) sin abrir puertos ni desactivar la auth
multi-profesor. Precondicion: stack arriba y tunel `exam_tunnel` activo.

## Caso que debe pasar

1. `docker logs exam_tunnel` muestra `https://<slug>.trycloudflare.com`.
2. `GET <URL>/` -> 200 con el HTML de la SPA.
3. Login via `<URL>/auth/login` con cuenta de prueba del propietario -> 200.
4. `GET <URL>/subjects` con `Accept: application/json` ->
   200 y el numero esperado de materias del usuario.
5. `new WebSocket("wss://<host>/ws")` abre (101).

## Caso que debe ser rechazado

1. `GET <URL>/subjects` sin token -> 401 (la auth no se relaja por exponer).
2. Tras `docker rm -f exam_tunnel`, la URL queda invalida (el quick tunnel
   no sobrevive al contenedor; nadie debe poder reutilizarla).

Evidencia de la ejecucion de 2026-11-09 (05:57 UTC-5): SPA 200, login 200,
subjects 200 con 8 materias, WS open, 401 sin token - registrada en
PROGRESS.md. QT aprobada por el agente; `verified` pendiente del propietario.

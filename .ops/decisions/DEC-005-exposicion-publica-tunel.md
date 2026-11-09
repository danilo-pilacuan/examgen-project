---
id: DEC-005-exposicion-publica-tunel
tipo: Decision
type: Decision
title: Mecanismo de exposicion publica del stack
description: Cloudflared quick tunnel elegido sobre Tailscale Funnel para demo y revision externa.
estado: abierta
dueno: rol:propietario
fecha: 2026-11-09
relaciona: [RUN-016, BL-018]
status: draft
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

## Pregunta

Como exponer el stack de desarrollo al internet para demo y revision externa
sin abrir puertos del router ni tocar el firewall institucional (seccion 12).

Fase en que se necesita (secciones 12 u 11): demo de tesis y tercera revision.
Opciones (6 lineas): (a) cloudflared quick tunnel - 1 comando, 0 credenciales,
URL aleatoria efimera por levantada, sin SLA; elegida por simpleza y por el
requisito de agnosticismo de credenciales. (b) Tailscale Funnel - URL estable
ts.net, exige cuenta + cert HTTPS + funnel ACL; ya instalado en el host.
(c) tunel con nombre (token) - URL estable en dominio propio, requiere
credencial propia. Resolucion: (vacia mientras estado = abierta)

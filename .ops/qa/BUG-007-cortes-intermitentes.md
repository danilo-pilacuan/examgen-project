---
id: BUG-007
tipo: Defect
type: Defect
title: Cortes de stream intermitentes bajo uso intensivo (ERR_INCOMPLETE_CHUNKED)
description: Fiabilidad general del chat degradada bajo uso sostenido; misma familia que BUG-003.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): 3 incidentes en ~90 turnos (08:29, 09:10 y el turno vacio del lote
5). En el del examen el corte fue exactamente a los 60 s; en los otros ocurrio durante
rafagas de turnos.

## Causa

Misma familia que BUG-003 (timeouts de proxy + ausencia de keepalive/heartbeat); posible
contribucion de `proxy_buffering` activo sobre `text/event-stream`.

## Fix y verificacion

Mismo paquete que BUG-003 (RFC-01/02): timeouts largos + `proxy_buffering off` +
heartbeat, y reintentos con backoff en el cliente SSE. Verificado en ronda 3 (C3/C8) y en
la campana de la etapa 15 sin recurrencia.
---
id: BUG-003
tipo: Defect
type: Defect
title: SSE del chat muere a los 60 s (timeout nginx) y cancela la generacion
description: Ningun examen podia generarse por chat; el stream se cortaba sin artefacto ni error.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): exactamente 60 s tras iniciar el turno (09:09:16 -> 09:10:16), el
navegador registra `net::ERR_INCOMPLETE_CHUNKED_ENCODING`; burbuja del asistente vacia,
sin card de artefacto, sin fila en `exams`, sin JSON, 0 llamadas a `POST /compile`.

## Causa

`proxy_read_timeout` de nginx por defecto = 60 s; la generacion de examen (LLM x N
preguntas + compilacion) tarda mas y el SSE no enviaba bytes; el frontend no reintentaba
ni informaba.

## Fix y verificacion

RFC-01/02: en `location /api/` timeouts 3600s + `proxy_buffering off`; heartbeat SSE
`": ping\n\n"` cada ~15 s propagado en las 3 capas; el cliente ignora frames de
comentario y muestra "connection lost + Retry" en caso de corte. Verificado en ronda 3
(C3/C8): turnos de mas de 60 s completan con `artifact_ready` y ZIP; matar exam_app
muestra el aviso y el Retry reenvia el turno.
---
id: BL-017
tipo: BacklogItem
type: BacklogItem
title: Tabla threads para conversaciones multi-dispositivo
description: Los metadatos de hilos viven en localStorage; migrar a tabla threads en Postgres.
estado: listo
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001, BUG-023, BUG-022, DEC-004]
status: draft
---

## Descripcion

Nota de sesion de la ronda 2: los metadatos de threads (id/titulo) siguen en
`localStorage` (por navegador); el contenido vive en el checkpointer Postgres. Para
multi-dispositivo haria falta una tabla `threads` (backlog post-V1).

Re-elevado en ronda 7 (2026-10-27): el reporte "no veo conversaciones pasadas"
es exactamente esta brecha (BUG-023) y se agrava con BUG-022 (sin owner en los
hilos, cualquier usuario lee/escribe el hilo ajeno). La propuesta (a) de DEC-004
cierra los tres: tabla con owner + listado + validacion 403.

## Criterio de salida

La sidebar lista los hilos desde la BD; el mismo usuario ve sus conversaciones desde otro
navegador; un usuario no ve ni toca los hilos ajenos.

## IMPL

IMPL-015; re-diagnosticado en IMPL-024
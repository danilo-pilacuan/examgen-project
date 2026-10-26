---
id: BL-017
tipo: BacklogItem
type: BacklogItem
title: Tabla threads para conversaciones multi-dispositivo
description: Los metadatos de hilos viven en localStorage; migrar a tabla threads en Postgres.
estado: idea
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001]
status: draft
---

## Descripcion

Nota de sesion de la ronda 2: los metadatos de threads (id/titulo) siguen en
`localStorage` (por navegador); el contenido vive en el checkpointer Postgres. Para
multi-dispositivo haria falta una tabla `threads` (backlog post-V1).

## Criterio de salida

La sidebar lista los hilos desde la BD; el mismo usuario ve sus conversaciones desde otro
navegador.

## IMPL

IMPL-015
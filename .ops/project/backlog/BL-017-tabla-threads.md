---
id: BL-017
tipo: BacklogItem
type: BacklogItem
title: Tabla threads para conversaciones multi-dispositivo
description: Los metadatos de hilos viven en localStorage; migrar a tabla threads en Postgres.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001, BUG-023, BUG-022, DEC-004, IMPL-025, QT-008]
status: done
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

IMPL-025 (2026-10-27): tabla `chat_threads` (migracion b8c9d0e1f2a3) +
GET/PATCH/DELETE /api/chat/threads + ownership en history/stream/invoke;
sidebar server-side con badges. Verificado en QT-008 (API 12/12 PASS +
Playwright PASS). Purga del checkpointer huerfano queda fuera de este item
(seguimiento separado).
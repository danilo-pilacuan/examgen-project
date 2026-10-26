---
id: BL-003
tipo: BacklogItem
type: BacklogItem
title: Indexacion de material en background con progreso
description: La subida bloquea el request ~2 min por capitulo; mover indexing a tarea en fondo con evento de progreso.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

`POST /api/files` hace extraccion + embeddings (bge-m3) sincronos en el request; la vista
Material queda en "Uploading..." ~2 min por capitulo de ~14 chunks y un libro completo
seria decenas de minutos (ISS-01, ronda 1). Indexar en background y notificar por WS/SSE.

## Criterio de salida

La subida responde en segundas; un evento `material_indexed` (o equivalente) actualiza la
vista al terminar; la UI muestra progreso por archivo.

## IMPL

IMPL-013
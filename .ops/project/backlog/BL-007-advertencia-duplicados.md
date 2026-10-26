---
id: BL-007
tipo: BacklogItem
type: BacklogItem
title: Advertencia de duplicados al guardar preguntas del chat
description: Reintentos del QA dejaron temas repetidos; avisar por similitud de embedding antes de guardar.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

El banco quedo con 91 preguntas para ~87 temas pedidos; varios temas repetidos con
redacciones distintas (ISS-08, ronda 1). La dedup del evaluador solo aplica dentro del
pipeline, no entre guardados del chat. En `save_question`/`save_pending_question`,
advertir si la similitud con preguntas existentes supera un umbral (usar el embedding ya
calculado) y pedir confirmacion.

## Criterio de salida

Guardar una pregunta con similitud alta contra el banco muestra advertencia y pide
confirmacion explicita antes de insertar.

## IMPL

IMPL-013
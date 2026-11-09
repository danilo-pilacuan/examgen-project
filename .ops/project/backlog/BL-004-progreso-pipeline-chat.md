---
id: BL-004
tipo: BacklogItem
type: BacklogItem
title: Eventos de progreso del pipeline en el chat
description: Durante el turno de examen solo se ve Thinking; emitir progreso por pregunta y estado de compilacion.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

Durante el turno de examen el profesor no sabe si avanzo (ISS-02, ronda 1): solo
"Thinking..." durante minutos. Los eventos `tool_start/tool_end` ya existen; usarlos para
el pipeline y anadir un estado "compiling LaTeX..." (ISS-02).

## Criterio de salida

El chat muestra progreso por pregunta generada/evaluada y el estado de compilacion; el
corte de stream se distingue de "procesando".

## IMPL

IMPL-013
---
id: BUG-010
tipo: Defect
type: Defect
title: El guardado HITL por texto consume el item pendiente aunque el stream muera
description: Estado del banco impredecible desde la vista del profesor (a veces guardo, a veces no, a veces sin verificar).
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): tras el turno vacio de q41 (BUG-006), el intento de re-guardar
respondio "no pending question left to save": el turno muerto ejecuto la tool (o la vacio)
sin entregar respuesta al profesor. En el lote 5 (q56) el mismo patron dejo la pregunta
guardada pero sin verificar pese a que el profesor pidio verificacion.

## Causa

`save_pending_question` limpiaba el pending (`set_pending_item(None, None)`) despues de
guardar; si el stream moria tras la tool, el profesor no sabia si guardo y no habia
re-consulta por statement.

## Fix y verificacion

Fix 11.3: registrar el id guardado en `PendingItemStore` ANTES de limpiar el pending y
emitir `question_saved` antes de limpiar; si el guardado falla, NO limpiar; tolerar
re-consulta por statement + subject respondiendo el estado real del banco. Verificado en
ronda 3 (C9): "already saved, id X, verified" en vez de "no pending question"; en
conversacion nueva, mensaje honesto "no pending question to save"; sin duplicados en BD.
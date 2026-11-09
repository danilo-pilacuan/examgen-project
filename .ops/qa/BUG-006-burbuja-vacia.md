---
id: BUG-006
tipo: Defect
type: Defect
title: Turno de chat termina con burbuja de asistente VACIA sin error
description: Perdida silenciosa de trabajo del profesor; el stream se cortaba sin propagar error.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19), lote 4, q41 ("database constraints CHECK and UNIQUE"): el turno de
guardado termino (boton Stop desaparecio) y el ultimo mensaje del asistente quedo con 0
caracteres; la pregunta no se guardo y el item pendiente se perdio (el siguiente turno
respondio "there is no pending question left to save"; ver BUG-010).

## Causa

El stream se corta sin propagar error al store (el `catch` de `useChatStream` solo hacia
`finishMessage`); sin heartbeat no se distingue "procesando" de "muerto". Familia de
BUG-003.

## Fix y verificacion

RFC-02: evento `error` tipado al cortarse el stream; en el frontend, la burbuja marca
"Connection lost" con boton Retry; `failMessage`/`clearMessageFailure` en el store.
Verificado en ronda 3 (C8): matar exam_app a mitad de turno -> aviso + Retry; el Retry
reenvia el turno y el contenido queda persistido en el checkpointer.
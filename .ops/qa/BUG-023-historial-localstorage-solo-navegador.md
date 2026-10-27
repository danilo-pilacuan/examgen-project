---
id: BUG-023
tipo: Defect
type: Defect
title: El historial de conversaciones vive solo en localStorage del navegador
description: Sidebar vacia tras limpiar storage, en otro navegador/dispositivo; el listado no se acota por usuario y borrar en UI no purga el checkpointer.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BL-017, BUG-013, BUG-022, QT-007, IMPL-024, DEC-004]
status: draft
---

## Evidencia

Ronda 7 (2026-10-27, Playwright + BD). Bug reportado por el propietario:
"no veo conversaciones pasadas en el historial de conversaciones".

1. Mismo navegador: 2 hilos de control de qa-r7 en Postgres (checkpoints)
   visibles e hidratables al hacer click. PASS local.
2. Se removio `mvp_chat_threads` de localStorage + reload -> sidebar con
   0 conversaciones aunque los 2 hilos siguen en BD. Este es el repro exacto
   del reporte (storage limpiado, otro navegador u otro dispositivo).
3. logout/login con el mismo navegador: los hilos reaparecen sin filtro por
   usuario; al registrar un usuario nuevo (qa-r7-ui-temp) en el mismo
   navegador este hereda y lee el historial de qa-r7 (faceta de BUG-022).
4. Borrar un hilo con la X de la sidebar quita la entrada de la lista, pero
   el contenido sigue en `checkpoints` y accesible por el endpoint history
   (a7e551d2 y fda8e443 quedaron huerfanos y legibles).

## Causa

`useThreadId.ts:4` guarda el listado (id/titulo) en
`localStorage['mvp_chat_threads']`, acotado al navegador, no al usuario; el
contenido vive en el checkpointer PostgresSaver. No existe endpoint de
listado de hilos (BL-017, pendiente desde ronda 2) ni purga del checkpointer.

## Fix y verificacion

BL-017: tabla `threads` con owner + endpoint `GET /api/chat/threads` que
liste solo hilos propios; la sidebar debe hidratarse desde la BD (criterio
de BL-017: el mismo usuario ve sus conversaciones desde otro navegador).
Verificacion: limpiar storage + reload conserva el historial; usuario B no
ve hilos de A; DELETE de hilo purga o marca el thread.

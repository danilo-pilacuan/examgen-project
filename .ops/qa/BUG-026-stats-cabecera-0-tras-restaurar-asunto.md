---
id: BUG-026
tipo: Defect
type: Defect
title: Estadisticas de cabecera 0/0 hasta re-seleccion manual del asunto activo
description: Al restaurar el asunto activo (login o Activate en Materias) los chips "N questions / N chunks" muestran 0/0 y el panel dice "No subject selected" hasta re-seleccionar en el combobox.
estado: corregido
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-009, IMPL-026, BUG-009]
status: draft
---

## Evidencia

Ronda 9 (2026-10-27, Playwright, usuario A):

1. Tras login correcto, la vista Materias muestra Eva como "Active" pero el
   header muestra `0 questions / 0 chunks` (BD real: 445 preguntas / 41
   chunks). Cero peticiones fallidas en consola; la consola solo registra
   `GET /subjects`, `GET /auth/me`, `GET /api/chat/threads`,
   `GET /api/chat/history/{id}`.
2. Re-seleccion manual de Eva en el combobox dispara
   `GET /subjects/{id}/questions|material|exams` y los chips pasan a
   `200 questions / 41 chunks`.
3. Tras hacer click en "Activate" de Eva en la vista Materias (recien
   logueado): mismo estado 0/0; se recupera igual con re-seleccion manual.

## Causa

`AppHeader` solo re-consulta los stores de preguntas/material/examenes en el
handler `onSubjectChange` del combobox (evento de cambio de usuario). Los
caminos programaticos que fijan el asunto activo (restauracion inicial de la
sesion y boton "Activate" de la vista Materias) actualizan el store del
asunto pero no disparan esa carga de estadisticas; los chips y la barra de
contexto leen stores vacios. Regresion parcial del fix de BUG-009.

## Fix y verificacion

Centralizar la carga de estadisticas en un watcher de `activeSubjectId`
(mismo patron que `ExamsView` ya usa: `$(() => c.activeSubjectId, ...)` con
`immediate: true`) en vez del handler del combobox. Verificacion: login ->
chips correctos sin interaccion; "Activate" en Materias -> chips correctos;
cambio por combobox sigue funcionando (regresion C10).

## Ejecucion del fix (2026-10-28, ronda 12)

Corregido en frontend c327682 (bump meta 299b118): `AppHeader.vue`
centraliza la carga en un watcher de `activeSubjectId` con `immediate:
true`; el handler del combobox queda solo como cambio de usuario.

Verificacion en vivo (bug026.spec.cjs, nueva spec e2e; 3/3 caminos):

- login -> chips correctos con cero interaccion (6q/28c Database Systems).
- "Activate" en Materias -> chips correctos (6q/85c Economia Aplicada).
- cambio por combobox -> chips correctos (regresion C10).

Conteos validados contra la BD real (6 preguntas / 28 y 85 chunks).
Regresion: suite e2e completa 16/16 PASS (15 versionadas + bug026).

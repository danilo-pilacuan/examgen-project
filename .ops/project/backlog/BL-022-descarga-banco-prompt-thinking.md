---
id: BL-022
tipo: BacklogItem
type: BacklogItem
title: Descarga del banco con campos de auditoria prompt y thinking
description: Boton Download bank en la lista de preguntas; el JSON incluye prompt y thinking desde llm_responses; detalle de fila muestra ambos campos.
estado: hecho
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [REQ-001, BL-015]
status: draft
---

## Descripcion

Mandato del propietario: anadir en el frontend, en la lista de preguntas del
banco, la funcionalidad para descargar el banco de preguntas donde tambien se
puedan ver los campos de pensamiento (thinking) y prompt.

`generated_questions` no guarda prompt ni thinking; viven solo en la auditoria
`llm_responses` (context `pipeline:generator`, raw_answer = JSON del item con
clave `statement`, la misma clave con la que el pipeline persiste
question_text). El endpoint `GET /subjects/{id}/questions/export` (exam-app
40e6750) correlaciona por statement exacto, newest-first-wins, y degrada
elegante: thinking null + `thinking_capture_enabled:false` (LLM_CAPTURE_THINKING
esta deshabilitado en vivo; 0/686 filas con thinking). Frontend f19813f:
boton Download bank (archivo `question_bank_<subject>_<date>.json`), alerta de
confirmacion que explica el thinking faltante, y bloques colapsables
Prompt/Thinking en el detalle de fila con fallback noPrompt. i18n EN/ES.

## Criterio de salida

Descarga real del JSON con total_questions > 0 y prompt poblado; UI muestra los
bloques de auditoria; suite e2e verde con casos F7/F7b nuevos.

## IMPL

IMPL-029 (ronda 12 extendida)

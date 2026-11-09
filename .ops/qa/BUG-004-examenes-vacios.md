---
id: BUG-004
tipo: Defect
type: Defect
title: El pipeline compila y publica examenes VACIOS como completed
description: El profesor recibia un examen sin preguntas como exito; aprobaba el flujo sin items.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

`data/agent_outputs/Parcial_1.json` (03:13): `total_questions: 2`, `items: []`, sin
`rejection_log` ni `total_llm_calls`. Los 4 PDFs (25.395 B identicos) contenian 1 pagina
con portada, "Question:", "Total Points: 0" y ninguna pregunta. Estado `completed` y ZIP
publicado en el chat (ronda 1, 2026-10-19).

## Causa

Las ranuras terminaban en `rejection_log` (los `except` de `generator_node`/
`evaluator_node` tragaban la excepcion y la convertian en rechazo) y
`assembler_node`/`compiler_node` no validaban `len(approved_items) > 0`;
`generate_exam_pdf` solo validaba que el banco tuviera preguntas.

## Fix y verificacion

RFC-04 (fail-fast): `compiler_node` con `approved_items` vacio -> `status="failed"` sin
compilar; `should_retry_compilation` -> end; `generate_exam_pdf` devuelve el error con
`rejection_log` resumido en vez del ZIP; `rejection_log` + `total_llm_calls` incluidos en
el JSON; errores de generator/evaluator logueados en `llm_responses`
(`pipeline:generator_error`/`evaluator_error`). Verificado en ronda 3 (C6): examen de un
tema sin preguntas -> el agente lo detecta y ofrece alternativas; con 2 preguntas genera
el examen con 2 items (sin PDFs vacios).
---
id: BUG-028
tipo: Defect
type: Defect
title: Banco heredado con 933/1239 preguntas en espanol (dato previo al contrato de idioma)
description: El contrato "todo el sistema en ingles" se cumple para contenido nuevo, pero el banco semilla heredado sigue en espanol.
estado: abierto            # abierto | corregido | verificado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [QT-010]        # QT que lo detecto
status: draft
---

## Evidencia

Suite Playwright ronda 10, test L2 (informativo):
`[lang-report] questions sample=200 spanish-like=200` (materia Eva,
limit=200). Censo BD completo (2026-10-28):
`SELECT count(*) FROM generated_questions WHERE question_text ~ '[¿¡]|[áéíóúñÁÉÍÓÚÑ]';`
-> 933 de 1239 preguntas con acentos/marcas de apertura espanolas (331 con
¿/¡). Las 3 preguntas nuevas de QA_R10_English_Gen (creadas tras el rebuild
con prompts en ingles) estan 100% en ingles.

## Causa

Dato, no defecto de codigo: las preguntas semilla (Eva/Lucia/Maria/Pablo/
Sofia y QA R6/R7) se generaron antes de que los prompts de generacion
(exam_pipeline/nodes.py, conversational/tools.py, shared/verifier.py)
exigieran ingles (fix de la ronda 10, commits de esta sesion). El material
fuente indexado esta en espanol, y los prompts antiguos no fijaban idioma,
por lo que el LLM generaba items en el idioma del material.

## Fix y verificacion

Fix de codigo ya aplicado y verificado para contenido nuevo (E1-EN PASS).
Queda abierta la decision del propietario sobre el dato heredado:
(a) regenerar/traducir el banco semilla, (b) dejarlo como legado y marcarlo
en UI, o (c) purgarlo. Mientras tanto L2 queda informativo (no falla la
suite). Verificacion: `npx playwright test` en projects/frontend (15/15).

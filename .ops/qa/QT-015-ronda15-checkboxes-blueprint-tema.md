---
id: QT-015
tipo: TestCase
type: TestCase
title: Ronda 15 - checkboxes Bloom/dificultad y blueprint por tema
description: QA Playwright del rediseno de ExamsView (BL-024): render, toggles, rechazo de suma excedida con 0 llamadas API y generacion real POST 200.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-11-06
relaciona: [BL-024, REQ-001, BUG-030, IMPL-031]
status: draft
fase: 6
---

## Objetivo

Verificar en navegador el rediseno del formulario Generate de ExamsView
(checkboxes de niveles reales, selectores numericos por tema) sin cambiar el
contrato del backend. Deriva de la regla 3 de la seccion 0 (caso adversarial
obligatorio). Precondicion: imagen frontend reconstruida con los cambios.

## Casos que deben pasar

- R15-1 (render): los 3 grupos son checkboxes (Bloom 6 niveles, dificultad 3,
  tipos 6), todos marcados por defecto; sin selects de presets.
- R15-2 (toggles): desmarcar Remember/Understand/Analyze deja el payload de
  bloom_distribution solo con apply/evaluate/create (~1/3 cada uno).
- R15-3 (temas): el panel avanzado lista los 3 temas reales de la materia
  (Econometrics, general, Macroeconomics) con input numerico 0-50 y el hint
  interpolado "(of 10)".
- R15-4 (E2E real): total 2, Econometrics 2, tipos multiple_choice +
  short_answer -> POST /exams/generate 200 tras ~4 min; examen persistido en
  la lista con boton ZIP; form cerrado.

## Caso que debe ser rechazado

- R15-R (suma excedida): conteos 30+30 con total 10 -> warning inline "sum
  (60) exceeds exam total (10)"; click en Generate -> 0 llamadas API
  (verificado con listener de requests).

## Resultado (2026-11-06, evidencia real)

- R15-1/2/3 PASS (page a02d72e3, materia "Economia Aplicada - QA11", id
  6c9e3cc3-6599-4868-a8a4-685bbb12bc30); payload capturado:
  bloom_distribution {apply:0.34, evaluate:0.33, create:0.33},
  topics_weight {"Econometrics":1}, allowed_question_types
  ["multiple_choice","short_answer"].
- R15-R PASS: warning visible y 0 requests POST.
- R15-4 PASS: POST 200, examen "2 questions" con ZIP en la lista.
- BUG-030 detectado y corregido en la ronda (hint "(of )" -> "(of 10)").
- vue-tsc exit 0; vite build verde; curl 200 tras rebuild.
- Pendiente del propietario: cierre de QT-015 y BUG-030.

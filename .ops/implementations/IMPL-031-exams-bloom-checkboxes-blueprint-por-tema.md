---
id: IMPL-031-exams-bloom-checkboxes-blueprint-por-tema
tipo: Implementation
type: Implementation
title: Exams - Bloom/dificultad como checkboxes y blueprint por tema
description: Redisenio frontend-only de ExamsView.vue (ronda 15) tras el feedback de Felipe; BUG-030 detectado y corregido en la misma ronda; QA en navegador con generacion real.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-11-06
relaciona: [BL-024, QT-015, BUG-030]
status: draft
---

## Alcance

Incluye: ExamsView.vue (checkbox groups de Bloom/dificultad, selectores
numericos por tema en el panel avanzado, guard de suma vs total, payload
equivalente) e i18n en.ts/es.ts (claves bloomLevels, difficultyLevels,
perTopic, perTopicSum, perTopicTotalError, topicsEmpty, topicsLoadError;
removidas presets y distribuciones custom). Contrato de backend sin cambios.

No incluye: backend/planner; verificacion final del propietario.

## Diseno

- Bloom/dificultad: nivel real como valor de checkbox (no presets); seleccion
  vacia cae a distribucion uniforme de todos los niveles; `levelsToDist`
  normaliza a suma 1.0 con el resto de redondeo en la primera clave
  (tolerancia backend 0.98-1.02).
- Temas: los temas reales salen del banco de la materia activa (watch de
  activeSubjectId, reset al cambiar); cada tema tiene un input numerico
  0-50; `applyTopicCounts` convierte conteos a pesos (conteo/suma, resto a
  la primera clave; fallback {general: 1.0} si todo en 0).
- Guards en generate(): 0 tipos de pregunta (ronda 14) y suma de temas >
  total del examen, ambos con mensaje inline y sin llamada API.
- minScore step corregido 0.05 -> 0.01 (los grids custom de 0.05 fueron
  removidos con el redisenio).

## Pasos atomicos

1) script de ExamsView (niveles + temas + guards); 2) template (checkbox
groups + dist-grid de temas + hints/errores); 3) i18n EN/ES; 4) vue-tsc +
build; 5) rebuild Docker + QA Playwright (render, rechazo, E2E real);
6) docs .ops + commits.

## Rollback

git revert del commit del submodulo frontend (sin migraciones ni backend).

## Ejecucion real (2026-11-06)

- vue-tsc exit 0 (tras corregir 2 errores: helper generico debe recibir el
  array crudo, no Ref); vite build verde; imagen frontend reconstruida y
  contenedor recreado (verificado con curl 200, exit code de compose no
  fiable por stderr en PowerShell).
- QA en navegador (page a02d72e3, materia "Economia Aplicada - QA11"):
  render de 3 grupos de checkboxes, toggles actualizan distribuciones,
  selectores por tema con los 3 temas reales, rechazo suma 60 > total 10
  con 0 llamadas API, E2E real: total 2, Econometrics 2, 3 niveles Bloom
  desmarcados, payload {bloom_distribution:{apply:0.34,evaluate:0.33,
  create:0.33}, topics_weight:{"Econometrics":1}, allowed_question_types:
  ["multiple_choice","short_answer"]} -> POST 200 tras ~4 min, examen
  persistido con ZIP.
- BUG-030 detectado en la ronda (interpolacion i18n sin parametros) y
  corregido en template + generate(); hint verificado "(of 10)".
- Pendiente del propietario: verificacion final de la ronda 15.

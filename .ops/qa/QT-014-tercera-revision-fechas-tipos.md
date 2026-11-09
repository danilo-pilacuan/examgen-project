---
id: QT-014
tipo: TestCase
type: TestCase
title: Tercera revision - fechas de verificacion y tipos restringibles (A1/A2)
description: Validacion estatica y de contrato de A1 (verified_at) y A2 extendido (allowed_question_types + panel avanzado); verificacion en navegador pendiente del propietario.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-11-05
relaciona: [BL-023, REQ-001, QT-013]
status: draft
fase: 6
---

## Objetivo

Verificar el contrato de A1/A2 (BL-023) sin stack Docker: validacion estatica
completa y casos de rechazo ejecutados contra los schemas reales. Deriva de la
regla 3 de la seccion 0 (toda prueba incluye caso adversarial). Precondicion
de la verificacion final: stack Docker rebuilt + alembic upgrade head.

## Casos que deben pasar

- A1-1: verified_at existe en models.py, migracion c9d0e1f2a3b4 (down_revision
  b8c9d0e1f2a3), QuestionOut/BankExportQuestion y Question (TS); un solo head.
- A1-2: service sella verified_at en creacion con verified_by_ai=True, en cada
  verificacion humana y lo pone NULL al quitarla (AST checks OK).
- A1-3: BankView muestra 2 columnas de fecha (creacion/verificacion, colspan 9).
- A2-1: blueprint default permite los 6 tipos (DEFAULT_OK).
- A2-2: dedup preserva orden (DEDUP_OK: ['essay','multiple_choice']).
- A2-3: planner filtra por Bloom contra el conjunto permitido y cae al conjunto
  completo si ningun preferido esta permitido (FALLBACK_OK/FALLBACK_OK2).
- A2-4: ExamsView envia allowed_question_types + retrieval; guard de 0 tipos;
  panel avanzado con distribucion custom (vue-tsc + build verdes).

## Caso que debe ser rechazado

- A2-R: allowed_question_types=[] -> ValidationError (REJECT_OK); via API seria
  422 (BUG-018 extra=forbid). En UI, generate() bloquea con noTypesError.

## Resultado (2026-11-05, evidencia real)

- DEFAULT_OK (6 tipos), REJECT_OK (ValidationError), DEDUP_OK, FALLBACK_OK,
  FALLBACK_OK2, PY_COMPILE_OK (7 archivos), HEADS ['c9d0e1f2a3b4'].
- tsc exit 0; vue-tsc exit 0 (tras fix 2x TS1345); vite build 4.74 s; lint de
  archivos cambiados limpio; AST checks STATIC/EXAM_APP/AGENTS_BACKEND/I18N/
  VIEWS OK.
- Commits: exam-app c38f871, agents-backend 57209b1, frontend fd6595a + ffaaada,
  core e4f8ea5 + 5c53ca0, meta e968a41; publicados en RC3/develop.

Estado: ejecutado (verificacion del propietario pendiente; nunca
auto-asignada por el agente). Datos de control: qa-r11@usfq.test.

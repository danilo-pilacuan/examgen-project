---
id: IMPL-030-tercera-revision-fechas-tipos
tipo: Implementation
type: Implementation
title: Tercera revision - fechas de verificacion y tipos de pregunta restringibles
description: A1 (verified_at + fechas en Bank) y A2 extendido (allowed_question_types + panel avanzado de blueprint) en core, exam-app, agents-backend y frontend.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-11-05
relaciona: [BL-023, QT-014]
status: draft
---

## Alcance

Incluye: A1 (columna verified_at con migracion, sellado en service layer, DTOs
exam-app, tipo TS, 2 columnas de fecha en BankView) y A2 extendido
(allowed_question_types en ExamBlueprint con validacion, filtrado en planner_node
con fallback, checkboxes + panel avanzado en ExamsView, i18n EN/ES).

No incluye: A3/A4, B1/B2, C1-C5 (pospuestos); verificacion E2E en navegador
(requiere rebuild Docker + alembic upgrade; pendiente del propietario).

## Diseno

- verified_at: sellado en `_utcnow()` del service (sin reloj de sistema en logica
  de negocio); se sella en creacion cuando verified_by_ai=True, se actualiza en
  cada verificacion humana y vuelve a NULL al quitarla; update_question no lo toca.
- allowed_question_types: campo nuevo en ExamBlueprint (BUG-018 extra=forbid
  exige declararlo); default los 6 tipos mantiene los constructores existentes
  (tools.py, run_pipeline.py, harness.py); lista vacia -> ValueError -> 422;
  dedup que preserva orden.
- Planner: filtra sus candidatos por Bloom contra el conjunto permitido; si ningun
  tipo preferido esta permitido, cae al conjunto permitido completo (choice
  determinista).
- Frontend: checkboxes de tipos con guard en generate() (error si 0), panel
  avanzado en <details> con distribucion custom de Bloom/dificultad y retrieval
  (use_rag, top_k, min_score); normalizadores aplicados antes de armar el payload.

## Pasos atomicos

1) migracion c9d0e1f2a3b4 + models.py; 2) service.py sellado; 3) schemas exam.py;
4) DTOs bank.py + 3 sitios de mapeo en subjects.py; 5) planner nodes.py;
6) domain.ts + BankView + ExamsView; 7) i18n en/es (16 claves); 8) validacion
estatica + caso de rechazo; 9) docs .ops + commits.

## Rollback

git revert de los commits por submodulo y `alembic downgrade b8c9d0e1f2a3`
(la migracion nueva solo anade la columna verified_at).

## Ejecucion real (2026-11-05)

- Validacion estatica verde: tsc exit 0; vue-tsc exit 0 (corrigio 2x TS1345 en
  ExamsView: normalizadores movidos a bloque if explicito); vite build 4.74 s;
  py_compile OK en 7 archivos Python; AST checks OK (service, models, schemas,
  mapeos, planner, 16 claves i18n, invariantes de vistas).
- Caso de rechazo ejecutado: allowed_question_types=[] -> ValidationError;
  default 6 tipos OK; dedup preserva orden; fallback del planner verificado
  (FALLBACK_OK/FALLBACK_OK2). Head unico de Alembic: c9d0e1f2a3b4.
- Lint de archivos cambiados limpio (el error de bug026.spec.cjs es preexistente).
- Pendiente del propietario: verificacion en navegador (rebuild Docker +
  alembic upgrade head) y suite e2e.

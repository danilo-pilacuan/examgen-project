# PROGRESS.md — Exam Generator

> Bitacora raiz de progreso (politica permanente de estado del repo, seccion 0 de
> `.github/copilot-instructions.md`). Reemplaza a `implementaciones/HANDOFF.md`
> como log raiz; el detalle por etapa vive en `.ops/implementations/IMPL-*.md`.
> Formato: una entrada por tarea, mas reciente primero. Coexiste con `.ops/project/progress.md`
> si en el futuro se aprueba el modelo OKF de bitacora.

## 2026-10-26

* **Hecho:** migracion de la carpeta `implementaciones/` al arbol `.ops` (BL-000 / IMPL-020):
  19 documentos de etapa -> `.ops/implementations/IMPL-NNN-*.md`; 18 bugs -> `.ops/qa/BUG-NNN.md`;
  22 items de backlog -> `.ops/project/backlog/BL-NNN.md`; REQ-001..003; handoff, plan,
  test-plan (C1-C15/R1-R7), traceability (REQ->BL->IMPL->QT->BUG), plantillas OKF y READMEs
  de carpeta. Referencias externas actualizadas (ARCHITECTURE.md, docs/informe_avance.md,
  readme.md); `implementaciones/` eliminado. Validacion: 89 archivos, ids unicos,
  frontmatter conforme, ASCII limpio, <=40 lineas de contenido.
* **Falta:** revision y `verified` del propietario sobre REQ/IMPL/BUG (el agente no escribe
  verified); IMPL-020 pasa a ejecutado tras esa revision.
* **Decision:** ninguna (convencion de mapeo documentada en `.ops/project/plan.md`).
* **Medicion:** 102 runs reales de la campana de evaluacion (etapa 15); H1-H5 resueltas.

## 2026-10-26 (sesion anterior)

* **Hecho:** etapa 16 — QA ronda 4 con Playwright: fix scroll global (BUG-17) y rewrite nginx
  del toggle de verificacion (BUG-17b); matriz de 10 casos verificada en navegador.
* **Falta:** suite Playwright versionada (BL-010).
* **Decision:** ninguna.
* **Medicion:** scrollHeight > clientHeight verificado en Exams/Bank/Subjects; PUT de
  verificacion 200 via nginx.

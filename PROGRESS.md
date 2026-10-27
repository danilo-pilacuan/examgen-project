# PROGRESS.md — Exam Generator

> Bitacora raiz de progreso (politica permanente de estado del repo, seccion 0 de
> `.github/copilot-instructions.md`). Reemplaza a `implementaciones/HANDOFF.md`
> como log raiz; el detalle por etapa vive en `.ops/implementations/IMPL-*.md`.
> Formato: una entrada por tarea, mas reciente primero. Coexiste con `.ops/project/progress.md`
> si en el futuro se aprueba el modelo OKF de bitacora.

## 2026-10-26 (informe de implementacion)

* **Hecho:** publicados en origin `166c71e` + `2155694` (QA ronda 5). Creado
  `docs/informe_implementacion.md`: informe integral en espanol para la tesis y defensa
  (resumen ejecutivo con metricas, arquitectura monorepo + 6 servicios, pipeline batch de
  6 nodos, agente ReAct con 15 tools y HITL, RAG, seguridad multi-tenant, framework de
  evaluacion, resultados de la campana 102 runs con H1-H5, 5 rondas de QA, metricas de
  escala verificadas contra la BD, limitaciones, trabajo futuro y guion de defensa con
  demo sugerida). 4 diagramas mermaid (arquitectura, pipeline, loop agente, RAG).
* **Falta:** escrito de la tesis (capitulos de implementacion y experimentacion); BUG-018
  endurecimiento; C2 con PDF grande real; BL-010 suite Playwright; revision `verified` del
  propietario; repos remotos de submodulos (etapa 01); inconsistencia del instruccionado
  (validate.yml referencia infra DigitalMe ausente).
* **Decision:** el informe es un documento de referencia integral, no duplica
  `docs/informe_avance.md` (avance de etapas): este resume el sistema terminado y los
  resultados; aquel el log de avance por etapa. Nombres de archivos no cambian.

## 2026-10-26 (ronda QA 5)

* **Hecho:** commit `166c71e` con el nuevo instruccionado del agente (copilot-instructions.md,
  skill ops-lifecycle, workflow validate.yml; sin publicar en origin). QA ronda 5 API-centrada
  (IMPL-021): routing nginx (Accept json, SPA fallback, OPTIONS/HEAD, /output 404), auth 401,
  aislamiento multi-tenant, 422 accionable, generacion E2E con banco vacio (16 llamadas LLM,
  8 preguntas, zip via /output 200), DELETE de pregunta, BUG-017b re-verificado (toggle 200
  bidireccional). num_versions verificado funcional (2 versiones / 4 PDFs con el campo
  anidado en `blueprint.metadata`); BUG-018 abierto como endurecimiento (Pydantic descarta
  campos extra del blueprint sin 422). C16-C20 agregados al test-plan. Sondas de QA
  purgadas de la BD.
* **Falta:** BUG-018 endurecimiento (extra=forbid); C2 con PDF grande real; BUG-016 retry;
  BL-010 suite Playwright; capitulo de experimentacion de la tesis; revision `verified` del
  propietario; publicar `RC2/develop` en origin; inconsistencia del instruccionado (validate.yml
  referencia infra DigitalMe ausente: tools/, mcp/, package.json raiz).
* **Decision:** contrato de /exams/generate confirmado con sondas contrastadas: metadatos
  (title/name/num_versions) viven en `blueprint.metadata` (el frontend ya lo anida asi);
  GET/DELETE /subjects/{id} sin endpoint (API minima por diseno, gap menor).
* **Medicion:** 5 sujetos de prueba aislados correctos; generacion ~0.5-4 min/run; zip
  101-130 KB; 0 rechazos de items; 3 rondas de generacion persistidas y purgadas.

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

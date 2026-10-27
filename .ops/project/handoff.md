---
id: handoff
tipo: Guide
type: Guide
title: Handoff entre sesiones
description: Punto de entrada de cada sesion; estado exacto donde se quedo el trabajo.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [plan, ops-readme]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

> **Ultima actualizacion:** 2026-10-27 (QA ronda 6: certificacion RC3 ejecutada) | **Rama:** `RC3/develop` |
> **Arbol:** ronda 6 de QA certificada (IMPL-023): BUG-016 y BUG-018 verificados como resueltos
> en navegador/API, RFC-10/11 PASS, C2 PASS con PDF 5.4 MB (211 chunks, RAG OK). Hallazgos nuevos
> BUG-019 (HUMAN duplicado tras Retry), BUG-020 (indexacion sin limites/progreso/cancelacion),
> BUG-021 (persist=false persiste examen) con decisiones abiertas DEC-001/002/003 para el
> propietario. Rondas previas: RC2 tag publicado en los 7 repos; IMPL-022 con fixes de BUG-018,
> BUG-016 y BL-008 (RFC-10/11/12).

## Contexto en 30 segundos

Exam Generator: MVP de tesis USFQ para que un profesor genere examenes LaTeX por chat con agente LangGraph y HITL, con versiones con/sin respuestas. Monorepo con 6 submodulos. Estado actual: **RC2/develop** tras 5 rondas de QA (etapa 16 + ronda 5, 2026-10-26) y el framework de evaluacion del agente ejecutado (etapa 15, 102 runs reales, H1-H5 resueltas). Desarrollo congelado para pasar al escrito de la tesis.

## Que leer y en que orden

1. Este archivo (`project/handoff.md`).
2. `../../PROGRESS.md` (bitacora raiz).
3. `project/plan.md` (mapa de etapas) y el IMPL activo en `../implementations/`.
4. Para campanas de evaluacion: `../../test/evaluation/README.md` (doc viva del framework).

## Estado por donde se quedo

| Tema | Estado |
|---|---|
| Caso de uso central (materias, material, preguntas HITL, examenes, ZIP) | Verificado E2E (rondas 1-6; C2 PASS con PDF 5.4 MB real en ronda 6) |
| Framework de evaluacion (etapa 15) | Ejecutado: 102 runs reales; hiperparametros validados T gen=0.7, top_k=3, T eval=0.2 |
| BUG abiertos | BUG-019 (HUMAN duplicado en checkpointer tras Retry), BUG-020 (indexacion sin limites/progreso/cancelacion, ~29 h para 8000 paginas), BUG-021 (persist=false persiste igualmente examen/PDFs/ZIP). Los 3 con decision pendiente en DEC-001/002/003. BUG-016 y BUG-018 RESUELTOS y verificados en ronda 6 |
| Backlog P2/P3 | BL-008 verificado en browser (ronda 6); BL-010 Playwright suite y demas P2/P3 pendientes |
| Etapa 01 (repos GitHub + CI) | Pendiente: repos locales listos, remotos no creados |
| Migracion a .ops | Hecha: `implementaciones/` eliminado; todo vive en `.ops/` (94 docs OKF). IMPL-020 queda `borrador` hasta la revision del propietario |
| Instruccionado del agente | Commit `166c71e` (sin publicar): copilot-instructions.md + skill ops-lifecycle + workflow validate.yml. Inconsistencia: el workflow referencia infra inexistente en este repo (tools/, mcp/, package.json raiz); fallaria al ejecutar en main |

## Trabajo pendiente (priorizado)

1. Escrito de tesis, capitulo de experimentacion (usa `test/evaluation/` FINDINGS; sin codigo).
2. Resolver DEC-001/002/003 (dueño): semantica de persist, dedupe HUMAN del Retry, limites de indexacion; luego fix de BUG-019/020/021 (P1; requiere codigo).
3. BL-010 suite Playwright versionada (P2; requiere codigo).
4. Comparativa cross-provider de modelos (P3; depende de acceso a otro modelo en el gateway).
5. Etapa 01: crear repos remotos + CI del meta-repo (P3; requiere codigo).
6. Resolver inconsistencia del instruccionado: validate.yml/copilot-instructions referencian infra DigitalMe ausente (tools/, mcp/, package.json raiz, AGENTS.md).

## Gotchas que NO hay que redescubrir

- PowerShell no soporta `&&` -> usar `;` o if-checks.
- Scripts creados en Windows llevan CRLF; `sh` de alpine los rechaza -> `dos2unix`.
- La consola Windows es cp1252: leer archivos UTF-8 con `view` o Python, no `Get-Content`.
- Los fixes de nginx y la config van horneados en la imagen -> rebuild Docker tras tocarlos.
- El routing nginx por `Accept` exige probar TODOS los metodos HTTP de cada prefijo (BUG-017b).
- Framework: dry-run contamina la BD real con stubs; nunca mezclar modos sin re-indexar (`test/evaluation/src/_reindex_real.py`). El judge usa `max_tokens=2000` (el gateway consume reasoning tokens). La latencia bimodal del gateway es efecto de carga, no causal.

## Historial de sesiones

| Fecha | Alcance y resultado |
|---|---|
| 2026-10-26 (anterior) | Etapa 16 (QA ronda 4 scroll + nginx toggle) ejecutada y publicada; handoff estructurado |
| 2026-10-26 (actual) | Migracion de `implementaciones/` al arbol `.ops` (89 docs: 21 IMPL, 22 BL, 18 BUG, 3 REQ, plan, handoff, traceability, plantillas, READMEs); referencias externas actualizadas; carpeta original eliminada; sin codigo de producto |
| 2026-10-26 (ronda 5) | Commit `166c71e` instruccionado agente (sin publicar); QA ronda 5 API: routing nginx, auth, aislamiento, 422, generacion E2E banco vacio (16 llamadas LLM, zip OK), DELETE pregunta, BUG-017b re-verificado; BUG-018 abierto (blueprint acepta campos extra en silencio; num_versions OK anidado en metadata); IMPL-021 + C16-C20 en test-plan; sondas DB purgadas |
| 2026-10-26 (informe) | Commits `166c71e` y `2155694` publicados en origin; creado `docs/informe_implementacion.md` (informe de implementacion para tesis/defensa: arquitectura, 2 loops, 15 tools, RAG, seguridad, campana 102 runs con H1-H5, 5 rondas QA, metricas de escala, guion de defensa; 4 diagramas mermaid) |
| 2026-10-26 (RC3) | Tag `RC2` + rama `RC3/develop` creados y publicados en los 7 repos; IMPL-022: BUG-018 resuelto (ConfigDict extra=forbid en ExamBlueprint), BUG-016 resuelto (retry 401 con token de localStorage en apiFetch), BL-008 RFC-10 (mvp_active_subject en localStorage) y RFC-11 (loadThread append tras Retry); frontend build + vue-tsc OK; verificacion browser pendiente del propietario |
| 2026-10-27 (ronda 6) | Certificacion RC3 ejecutada (IMPL-023): BUG-018 verificado via nginx (raiz 422, metadata 200 num_versions=2), RFC-10 PASS (reload conserva materia), RFC-11 PASS (abort+Retry rehidrata sin duplicar contenido), BUG-016 PASS (3 restarts, 0 401), C2 PASS (PDF 5.4 MB, 211 chunks, RAG OK), R1/R2/R4/R5/R6 PASS; hallazgos BUG-019/020/021 documentados con DEC-001/002/003 abiertas; .ops actualizado (test-plan, traceability, READMEs, handoff) |

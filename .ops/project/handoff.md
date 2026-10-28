---
id: handoff
tipo: Guide
type: Guide
title: Handoff entre sesiones
description: Punto de entrada de cada sesion; estado exacto donde se quedo el trabajo.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [plan, ops-readme]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

> **Ultima actualizacion:** 2026-10-28 (QA ronda 10 - framework e2e versionado + contrato de idioma) | **Rama:** `RC3/develop` |
> **Arbol:** ronda 10 ejecutada (IMPL-027/QT-010, mandato del propietario: recertificar lo esencial,
> estrenar el framework de pruebas y verificar que TODO el sistema este en ingles). (1) Suite
> Playwright versionada BL-010 creada en `projects/frontend/e2e` (playwright.config.ts + helpers +
> 3 specs: functional F, integration I, language L = 15 tests) y en verde: 15/15 PASS contra el
> stack Docker (3 corridas). (2) Contrato de idioma enforceado en codigo: prompts de
> generator_node/evaluator_node (rechazo language_not_english), generate_question (chat) y
> verifier.py exigen ENGLISH; exam-app reconstruido y verificado en contenedor (grep 'in ENGLISH').
> (3) E1-EN PASS: examen QA_R10_English_Gen (materia Eva con material en espanol): 3 items
> 100% en ingles (statements/opciones/respuestas/explicaciones), PDFs + ZIP en /app/output.
> (4) BUG-028 nuevo (medio, dato): banco heredado 933/1239 preguntas en espanol (L2 informativo
> 197/200); decision del propietario pendiente (regenerar/marcar/purgar). BUG-026/027/024/025
> siguen abiertos (fuera de alcance). Cuenta de control nueva: qa-r10@usfq.test. Commits
> pendientes de push.

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
| BUG abiertos | Ronda 6: BUG-019 (HUMAN duplicado en checkpointer tras Retry), BUG-020 (indexacion sin limites/progreso/cancelacion, ~29 h para 8000 paginas), BUG-021 (persist=false persiste igualmente examen/PDFs/ZIP) con DEC-001/002/003 pendientes. Ronda 7: BUG-022 (CRITICO) y BUG-023 -> `corregido` en ronda 8 (IMPL-025, QT-008; pendiente verificado del propietario); BUG-024 (sin cabeceras de seguridad nginx), BUG-025 (mensaje 401 enganoso en login). Purga del checkpointer huerfano al borrar hilo: seguimiento separado. BUG-016 y BUG-018 RESUELTOS y verificados en ronda 6 |
| Backlog P2/P3 | BL-008 verificado en browser (ronda 6); BL-010 Playwright suite EJECUTADO en ronda 10 (IMPL-027); demas P2/P3 pendientes |
| Etapa 01 (repos GitHub + CI) | Pendiente: repos locales listos, remotos no creados |
| Migracion a .ops | Hecha: `implementaciones/` eliminado; todo vive en `.ops/` (94 docs OKF). IMPL-020 queda `borrador` hasta la revision del propietario |
| Instruccionado del agente | Commit `166c71e` (sin publicar): copilot-instructions.md + skill ops-lifecycle + workflow validate.yml. Inconsistencia: el workflow referencia infra inexistente en este repo (tools/, mcp/, package.json raiz); fallaria al ejecutar en main |

## Trabajo pendiente (priorizado)

1. Verificado del propietario de QT-010 / IMPL-027 / BL-010 / BUG-028 (ronda 10): revisar
   evidencia (test-plan Ronda 10, suite e2e, examen QA_R10_English_Gen) y pasar a `verificado`.
2. Decidir BUG-028 (medio, dato): que hacer con el banco heredado en espanol
   (933/1239 preguntas): regenerar/traducir, marcarlo como legacy en UI, o purgarlo.
3. Decidir y fixear BUG-027 (alto): fail-fast cuando la materia no tiene material indexado
   ni banco (alineado con C6/BUG-004) y corregir `indexed_chunks_count` del response;
   requiere codigo + rebuild del exam-app.
4. Fix menor BUG-026: cargar estadisticas de AppHeader en un watcher de `activeSubjectId`
   (patron ExamsView) en vez del handler del combobox; requiere codigo + rebuild frontend.
5. Push a origin de los commits de las rondas 8-10 (core, exam-app, frontend, meta-repo; rama
   RC3/develop) si quedo pendiente por red.
6. Purga del contenido huerfano del checkpointer al borrar hilo (P2; seguimiento separado,
   el listado ya no expone huerfanos).
7. Escrito de tesis, capitulo de experimentacion (usa `test/evaluation/` FINDINGS; sin codigo).
8. Resolver DEC-001/002/003 (dueño): semantica de persist, dedupe HUMAN del Retry, limites de
   indexacion; luego fix de BUG-019/020/021 (P1; requiere codigo).
9. Fix menor BUG-025 (mensaje de login) y BUG-024 (cabeceras nginx + rebuild) (P2).
10. Comparativa cross-provider de modelos (P3; depende de acceso a otro modelo en el gateway).
11. Etapa 01: crear repos remotos + CI del meta-repo (P3; requiere codigo).
12. Resolver inconsistencia del instruccionado: validate.yml/copilot-instructions referencian infra DigitalMe ausente (tools/, mcp/, package.json raiz, AGENTS.md).

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
| 2026-10-27 (ronda 7) | Recertificacion funcional (Playwright) + integracion (API/nginx/BD) sin unitarias, a pedido del propietario (IMPL-024). Bug reportado "no veo conversaciones pasadas" = BUG-023: listado de hilos solo en `localStorage['mvp_chat_threads']` (`useThreadId.ts`), mismo navegador PASS, storage limpio/otro navegador -> sidebar vacia con hilos en BD; fix en BL-017. BUG-022 critico: B lee y escribe hilos de A (history/stream/invoke sin ownership; evidencia API + visual con tercer usuario). BUG-024 (cabeceras nginx) y BUG-025 (mensaje 401 login) nuevos. C25-C40: 11 PASS/3 FAIL/2 nota; QT-007, DEC-004, IMPL-024, test-plan, traceability, BL-017 re-elevado; limpieza: materia "QA R7 UI Temp" y usuario qa-r7-ui-temp borrados, hilos de control conservados como evidencia |
| 2026-10-27 (ronda 8) | Fix DEC-004 (a extendida por el propietario) implementado y verificado (IMPL-025/BL-017/QT-008): tabla `chat_threads` (migracion b8c9d0e1f2a3 aplicada en contenedor), threads_service.py con register_or_adopt (nunca reasigna id ajeno) + require_owned_thread, endpoints GET/PATCH/DELETE /api/chat/threads, ownership 403 en history/stream/invoke; frontend: useThreadId server-backed, ThreadSidebar con badges (ultima materia + contador), ChatPanel/ChatView/auth ajustados, i18n es/en. Verificacion: scripts/verify-threads-r8.ps1 12/12 PASS (B sobre hilo de A: history/write/rename/delete = 403; listado aislado; 401 sin token) + Playwright PASS (reload conserva conversacion, badges "QA R7 Recert"+"4", delete con chat_threads=0). Docker rebuild del frontend detecto y corrigio TS2349 (shadowing `t` de useI18n en v-for; el tsc local no lo atrapa - vue-tsc de Docker es la puerta). Usuarios qa-r8-a/b y sus hilos purgados. BUG-022/023 -> `corregido`; DEC-004 -> `tomada`; pendiente push de 4 repos y verificado del propietario |
| 2026-10-27 (ronda 8 anexo UX) | A pedido del propietario, el detalle del Banco de Preguntas se movio de un bloque al final de la lista a un acordeon inline (C54): columna chevron, filas con role=button/tabindex/aria-expanded, tr.detail-row bajo la fila pulsada, cierre por X o segundo clic, seleccion unica, auto-scroll suave (function ref setDetailRow: un ref de plantilla en v-for es array y rompia scrollIntoView), hover/focus-visible, i18n es/en; se elimino un bloque de detalle duplicado tras la tabla. Playwright (qa-r7, 200 preguntas): expandir/cerrar/switch/teclado/hover PASS, 0 errores de consola; docker compose build frontend + up (bundle BankView-B0_gczOs.js). Pendiente: commit + push frontend/meta |
| 2026-10-27 (ronda 9) | Recertificacion QA + certificacion de examenes ejecutadas (IMPL-026/QT-009, mandato del propietario, agente como verificador humano en Playwright): F1-F13 PASS, F9 PASS con BUG-026 (chips 0/0 hasta re-seleccionar asunto tras login/Activate), F14 registra BUG-025 vivo; I1/I2/I3/I5/I6/I8/I9 PASS (401, ownership 403, guardrail verificadas, auth, aislamiento, HEAD, CRUD hilos), I4 FAIL conocido (BUG-024); E1-E4 PASS con nota (QA_R9_Cert 3/4 items tras 1 rechazo difficulty_mismatch; ZIP 175KB; PDFs HEAD 200; propietario ok; `indexed_chunks_count:0` anomalo), E5 FAIL -> BUG-027 (materia 0 chunks/0 preguntas publica 2 genericas "Sahara Desert" y persiste examen+ZIP+PDFs; regression C6/BUG-004). Purga: materia QA R9 Recert, examen QA_R9_Empty (BD+4 archivos) y 2 preguntas eliminadas; conservados QA_R9_Cert y hilo 57a386a2. .ops actualizado (test-plan, QT-009, IMPL-026, traceability, README, BUG-026/027, handoff); pendiente commit+push |
| 2026-10-28 (ronda 10) | Framework e2e versionado + contrato de idioma ejecutados (IMPL-027/QT-010/BL-010): suite Playwright en `projects/frontend/e2e` (config + helpers + 3 specs = 15 tests) 15/15 PASS contra Docker (3 corridas); prompts de generacion/evaluacion/verificacion exigen ENGLISH (evaluator rechaza con language_not_english), exam-app reconstruido y verificado en contenedor; E1-EN PASS: QA_R10_English_Gen (materia Eva, material RAG en espanol) con 3 items 100% en ingles + PDFs/ZIP en /app/output; L2 informativo detecta banco heredado en espanol -> BUG-028 (933/1239; decision del propietario). Cuenta qa-r10@usfq.test creada en BD (hash pbkdf2 del backend). .ops actualizado (test-plan ronda 10, QT-010, IMPL-027, traceability, BL-010, qa README, BUG-028, handoff); pendiente commit+push |

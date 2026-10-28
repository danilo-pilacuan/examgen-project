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

> **Ultima actualizacion:** 2026-10-28 (QA ronda 12 - recertificacion, credenciales QA en archivo, BUG-026 y BUG-027 corregidos y verificados en vivo) | **Rama:** `RC3/develop` |
> **Arbol:** ronda 12 ejecutada y cerrada (IMPL-029/QT-012, mandato del propietario: continuar la
> ronda de QA, entregar credenciales en archivo de salida, reportar lo que falta y corregir los
> bugs que no dañen la certificacion). (1) Credenciales QA entregadas en
> qa-r11-credentials.qa-creds.txt (git-ignored). (2) Suite e2e 16/16 PASS dos veces (tras fix
> BUG-026 y tras rebuild BUG-027; 15 versionadas + nueva bug026.spec.cjs, L2 estricto verde).
> (3) BUG-026 -> corregido (frontend c327682, meta 299b118): AppHeader centraliza la carga de
> estadisticas en un watcher de activeSubjectId (patron ExamsView, immediate: true); 3/3 caminos
> verificados en vivo (login, Activate, combobox) con conteos contra BD real (6q/28c y 6q/85c).
> (4) BUG-027 -> corregido (exam-app 2474b2c + agents-backend e5cee07, meta 6ca1c13): repros en
> vivo confirmaron ambos claims (examenes genericos publicados con 0 chunks/0 preguntas;
> indexed_chunks_count siempre 0 en el camino API); fix fail-fast en POST /exams/generate
> (404 materia inexistente, 422 accionable si 0 chunks Y 0 preguntas) + ingestor_node devuelve
> el COUNT real de material_chunks; verificacion V1-V4 en vivo tras rebuild (422 accionable;
> 200 con indexed_chunks_count: 28 y item RAG-grounded; 404; C6 sin persistencia en materia
> vacia). (5) BUG-021 re-confirmado en vivo 2 veces durante los repros (persist:false persiste
> examen/PDFs/ZIP; DEC-003 sigue pendiente del propietario); artefactos de repro purgados
> (materia, filas de examen, JSON/PDF/ZIP). BUG-024/025 y BUG-019/020 siguen abiertos.

**Ronda 11 (contexto inmediato, 2026-10-28):** BD reconstruida desde cero
(alembic head b8c9d0e1f2a3, 13 tablas) y material re-indexado (Database
Systems 28 chunks; Economia Aplicada - QA11 51 chunks); 12 preguntas nuevas
100% en ingles via pipeline real con revision humana HITL del agente 12/12
(verified_by_human=true); suite 15/15 con L2 estricto; 2 examenes de control
en ingles; set de metricas regenerado y campana REAL completada 82/82
(agregados + reportes + FINDINGS, commit 9e6bd6c); BUG-028 corregido (purga
+ regeneracion), BUG-029 corregido (deps docx/pptx + rebuild, verificado
200/200/200 con 85 chunks); hallazgo J1 (juez in-run num_judged=0) corregido
en 3827e4d; ingles de campana verificado sobre 621 items (0 cuerpos en
espanol).

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
| Framework de evaluacion (etapa 15) | Ejecutado: 102 runs reales (ronda base); set regenerado en ronda 11 (ingles, 82 runs); hiperparametros validados T gen=0.7, top_k=3, T eval=0.2 |
| BUG abiertos | Ronda 6: BUG-019 (HUMAN duplicado en checkpointer tras Retry), BUG-020 (indexacion sin limites/progreso/cancelacion, ~29 h para 8000 paginas), BUG-021 (persist=false persiste igualmente examen/PDFs/ZIP; re-confirmado en vivo 2 veces en ronda 12) con DEC-001/002/003 pendientes. Ronda 7: BUG-024 (sin cabeceras de seguridad nginx), BUG-025 (mensaje 401 enganoso en login). BUG-016 y BUG-018 RESUELTOS y verificados en ronda 6. Ronda 9: BUG-026 y BUG-027 -> `corregido` en ronda 12 (IMPL-029; pendiente verificado del propietario). Ronda 11: BUG-029 corregido y verificado en vivo (deps declaradas; 85 chunks) |
| Backlog P2/P3 | BL-008 verificado en browser (ronda 6); BL-010 Playwright suite EJECUTADO en ronda 10 (IMPL-027); demas P2/P3 pendientes |
| Etapa 01 (repos GitHub + CI) | Pendiente: repos locales listos, remotos no creados |
| Migracion a .ops | Hecha: `implementaciones/` eliminado; todo vive en `.ops/` (94 docs OKF). IMPL-020 queda `borrador` hasta la revision del propietario |
| Instruccionado del agente | Commit `166c71e` (sin publicar): copilot-instructions.md + skill ops-lifecycle + workflow validate.yml. Inconsistencia: el workflow referencia infra inexistente en este repo (tools/, mcp/, package.json raiz); fallaria al ejecutar en main |

## Trabajo pendiente (priorizado)

1. Verificado del propietario de QT-011/QT-012 / IMPL-028/IMPL-029 /
   BUG-028 (corregido) / BUG-029 (corregido) / BUG-026 (corregido) /
   BUG-027 (corregido) y del hallazgo J1: revisar evidencia (test-plan
   rondas 11-12, QT-011/QT-012, IMPL-028/IMPL-029, FINDINGS por
   experimento) y pasar a `verificado` donde corresponda.
2. Extension opcional de E03 a >= 4 repeticiones por clon (20 runs, ~35
   min) si la tesis defiende H5 con sigma entre clones; con 2 repeticiones
   el sigma (1.311) no es concluyente.
3. Re-ejecutar una campana pequena (o la proxima ronda) para validar el juez
   in-run corregido (num_judged > 0) y, si se quiere juez post-hoc, anclar
   ventanas por run_id/thread_id en vez de ventanas de tiempo.
4. Decidir y fixear BUG-021 (persist=false persiste; re-confirmado en ronda
   12) y BUG-019/020: requiere DEC-001/002/003 del propietario + codigo.
5. Fix menor BUG-025 (mensaje de login) y BUG-024 (cabeceras nginx + rebuild) (P2).
6. Purga del contenido huerfano del checkpointer al borrar hilo (P2; seguimiento separado,
   el listado ya no expone huerfanos).
7. Escrito de tesis, capitulo de experimentacion (usa `test/evaluation/` FINDINGS; sin codigo).
8. (Fusionado en el punto 4: DEC-001/002/003 con BUG-019/020/021.)
9. (Fusionado en el punto 5: BUG-024/025 siguen abiertos.)
10. Comparativa cross-provider de modelos (P3; depende de acceso a otro modelo en el gateway).
11. Etapa 01: crear repos remotos + CI del meta-repo (P3; requiere codigo).
12. Resolver inconsistencia del instruccionado: validate.yml/copilot-instructions referencian infra DigitalMe ausente (tools/, mcp/, package.json raiz, AGENTS.md).

## Gotchas que NO hay que redescubrir

- PowerShell no soporta `&&` -> usar `;` o if-checks.
- Scripts creados en Windows llevan CRLF; `sh` de alpine los rechaza -> `dos2unix`.
- La consola Windows es cp1252: leer archivos UTF-8 con `view` o Python, no `Get-Content`.
- Los fixes de nginx y la config van horneados en la imagen -> rebuild Docker tras tocarlos.
- El routing nginx por `Accept` exige probar TODOS los metodos HTTP de cada prefijo (BUG-017b).
- Framework: dry-run contamina la BD real con stubs; nunca mezclar modos sin re-indexar (`test/evaluation/src/_reindex_real.py`). El judge usa `max_tokens=2000` (el gateway consume reasoning tokens). La latencia bimodal del gateway es efecto de carga, no causal. Si un dry-run toca la BD real: purgar en orden FK (generated_questions -> material_chunks -> subjects); varios `psql -c "A; B"` corren en UNA transaccion (usar flags `-c` separados). Extractores docx/pptx fallan POR ARCHIVO (warning en log de exam_app) y el endpoint responde 400 solo si TODOS fallan; la validacion va antes del borrado, asi que `clear=true` no pierde chunks. Leer JSON de la API desde PowerShell 5.1 muestra UTF-8 como mojibake (cp1252): verificar siempre con cliente Python o regex en BD antes de abrir un BUG.
- Juez de faithfulness: `judge_faithfulness` descarta en silencio registros con statement vacio; pasar SIEMPRE registros correlacionados (`_correlate_statements(retrieval_records, item_records)`), igual que hace rag_metrics (hallazgo J1, corregido en 3827e4d).
- Alineacion de filas de auditoria (llm_responses) a runs: NO usar ventanas por timestamp para aparear statement<->chunks; hay +-1 fila de deriva (llamadas que cruzan la frontera del run). Para juez post-hoc futuro, anclar por thread_id/run_id. El conteo fiable por run vive en `metrics.cost.latency_by_node_ms.generator.count` (fallback `state_digest.total_llm_calls`, que cuenta generador+evaluador).
- `total_llm_calls` (16) != llamadas de generador (8): cuenta generador+evaluador; no usarlo como ventana de generador.
- git push desde PowerShell lanza NativeCommandError por stderr: es cosmético; verificar con `git ls-remote`.

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
| 2026-10-28 (ronda 10) | Framework e2e versionado + contrato de idioma ejecutados (IMPL-027/QT-010/BL-010): suite Playwright en `projects/frontend/e2e` (config + helpers + 3 specs = 15 tests) 15/15 PASS contra Docker (3 corridas); prompts de generacion/evaluacion/verificacion exigen ENGLISH (evaluator rechaza con language_not_english), exam-app reconstruido y verificado en contenedor; E1-EN PASS: QA_R10_English_Gen (materia Eva, material RAG en espanol) con 3 items 100% en ingles + PDFs/ZIP en /app/output; L2 informativo detecta banco heredado en espanol -> BUG-028 (933/1239; decision del propietario). Cuenta qa-r10@usfq.test creada en BD (hash pbkdf2 del backend). .ops actualizado (test-plan ronda 10, QT-010, IMPL-027, traceability, BL-010, qa README, BUG-028, handoff). Commits publicados: meta 0435f6c, agents-backend ea24a81, frontend 40ebdba |
| 2026-10-28 (ronda 11) | Recertificacion + BD desde cero + ingles e2e + set de metricas regenerado (IMPL-028/QT-011, mandato del propietario, agente con derecho HITL): BD drop + alembic head b8c9d0e1f2a3; 12 preguntas nuevas en ingles via pipeline real (2 materias x 6), revision humana 12/12 APROBADAS y verified_by_human=true via PUT /questions/{id}/verification; falso positivo mojibake (beta/por) descartado con cliente Python + regex BD (artefacto cp1252 de PS 5.1). Suite 15/15 PASS (10.8 s) con qa-r11 y L2 estricto. 2 examenes de control en ingles (qa11_control_db/econ) con PDFs + ZIP. subjects.yaml/experiments.yaml regenerados (ingles, 82 runs), raws r10 archivadas, smoke dry-run OK + purga de su polucion, campana REAL lanzada en background (E04->E03->E01->E02). BUG-028 -> corregido (opcion c: purga). BUG-029 nuevo (deps docx/pptx; chunks se conservan tras 400). .ops actualizado (test-plan ronda 11, QT-011, IMPL-028, traceability, READMEs, BUG-028/029, handoff, PROGRESS). Commits publicados: meta eeb6df3 (3 commits de la ronda), frontend 3b45000 |
| 2026-10-28 (ronda 11 - cierre) | Campana 82/82 COMPLETADA (0 fallidos, exit 0; E04 18, E03 10, E01 27, E02 27; resume SKIP de las corridas de verificacion en vivo). BUG-029 corregido: deps declaradas (core f0fc306, exam-app 2fd4491), imagen reconstruida, repro en vivo 200/200/200 (4 docx + 40 pptx + 85 chunks reindex) con scripts/qa_r11_docx_index.py; commits ae940e2/d89ec30/41d368c/dc698ca publicados. Hallazgo J1: juez in-run num_judged=0 en 82/82 (retrieval sin correlacionar); corregido en harness.py + windowing de judge_experiment.py reforzado (commit 3827e4d); juez post-hoc ABORTADO por deriva de +-1 fila en ventanas de tiempo (E04 79 vs 80; E01 213 vs 214). Agregados + reportes + FINDINGS regenerados con numeros r11 (commit 9e6bd6c): E01 T=0.3 domina eficiencia/alineacion (aprobacion 1.000) con T=0.7 mejor robustez entre clones; E02 k=8 dominado, k=3 y k=1 empatan alineacion 0.986; E03 sigma entre clones 1.311 con 2 repeticiones (H5 no concluyente; extension a >=4 recomendada); E04 aprobacion insensible a T evaluador, T=0.2 mas eficiente. Ingles de campana verificado: 621 items escaneados (scripts/qa_r11_english_check.py), 0 cuerpos en espanol, 13/621 nombres propios/glosas del material, 3/621 subtopic con eco del temario, 5 rechazos language_not_english por el evaluador (defensa activa). Pendiente: verificado del propietario (QT-011/IMPL-028/BUG-028/BUG-029/J1) |

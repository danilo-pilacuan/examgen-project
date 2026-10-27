# PROGRESS.md — Exam Generator

> Bitacora raiz de progreso (politica permanente de estado del repo, seccion 0 de
> `.github/copilot-instructions.md`). Reemplaza a `implementaciones/HANDOFF.md`
> como log raiz; el detalle por etapa vive en `.ops/implementations/IMPL-*.md`.
> Formato: una entrada por tarea, mas reciente primero. Coexiste con `.ops/project/progress.md`
> si en el futuro se aprueba el modelo OKF de bitacora.

## 2026-10-27 (ronda QA 7: recertificacion funcional + integracion)

* **Hecho:** ronda 7 de QA ejecutada contra RC3/develop a pedido del propietario
  (IMPL-024): pruebas funcionales con Playwright en navegador real y de
  integracion via API/nginx/Postgres, sin unitarias. Diagnostico del bug
  reportado ("no veo conversaciones pasadas en el historial"): es BUG-023, el
  listado de hilos vive solo en `localStorage['mvp_chat_threads']`
  (`useThreadId.ts:4`); en el mismo navegador los 2 hilos de control se listan
  e hidratan (C26/C27 PASS), pero limpiar el storage deja la sidebar vacia
  aunque los hilos siguen en el checkpointer (C25 FAIL, repro del reporte).
  La brecha es BL-017 (pendiente desde ronda 2). Hallazgo critico BUG-022: los
  endpoints de chat autentican pero no verifican propiedad del thread_id
  (`chat.py` history/stream/invoke), asi que el usuario B leyo y ESCRIBIO el
  hilo de A (evidencia API + visual en navegador con un tercer usuario);
  decision abierta DEC-004 con 3 opciones. Nota: materias semilla sin owner
  son escribibles por cualquiera. Funcionales PASS: banco (200 filas, filtros,
  toggle), examenes, material, creacion de materia, chat con materia activa,
  reload duro, guardia de ruta anonima. Integracion PASS: auth 422/409/401,
  aislamiento 403, guardrail de verificadas. Nuevos: BUG-024 (nginx sin
  cabeceras de seguridad), BUG-025 (login invalido muestra "Tu sesion
  expiro"). .ops actualizado: IMPL-024, QT-007, test-plan C25-C40, BUG-022/023/
  024/025, DEC-004, traceability, BL-017 re-elevado a listo, indices, handoff.
* **Falta:** resolucion de DEC-004 y fix de BUG-022/023 (BL-017); fixes
  BUG-024/025; DEC-001/002/003 y fixes BUG-019/020/021; tesis; BL-010.
* **Decision:** sin cambios de codigo: los 4 bugs nuevos quedan `abierto`;
  BUG-022/023 bloqueados por DEC-004 (el agente no cierra decisiones ni
  aplica fixes sin el propietario). Generacion E2E de examen omitida en la
  ronda: ya cubierta por C19 (ronda 5) y C2 (ronda 6).
* **Medicion:** C25-C40: 11 PASS / 3 FAIL / 2 PASS con nota; 2 hilos de
  control en checkpointer (ad0e765d, c35b172e) con 4 mensajes cada uno; B
  leyo 4 mensajes de A y le inserto 2; nginx devuelve solo Server y
  Content-Type (sin HSTS/XCTO/XFO); datos QA temporales purgados (materia
  "QA R7 UI Temp", usuario qa-r7-ui-temp, token files).

## 2026-10-27 (ronda QA 6: certificacion RC3)

* **Hecho:** ronda 6 de QA ejecutada contra RC3/develop con stack levantado (IMPL-023).
  Verificado: BUG-018 (sonda raiz -> 422 real via nginx; sonda metadata anidada -> 200 con
  num_versions=2, 4 PDFs y ZIP); RFC-10 (hard reload conserva la materia activa y contadores);
  RFC-11 (abort de SSE -> burbuja failed + Retry -> turno completo y rehidratado desde el
  checkpointer sin duplicar contenido); BUG-016 (3 restarts de exam_app con sesion activa,
  0 401, HITL intacto); C2 (PDF real 5.4 MB, sin 413, 211 chunks indexados ~20 min, RAG
  citando el material). Regresiones: R1 save HITL verified-by-human, R2 guardrail anti-borrado,
  R4 export XLSX por chat (tool export_questions), R5 auditoria llm_responses (3250 filas,
  thread trazado), R6 toggle ES/EN persistente. Hallazgos nuevos documentados: BUG-019 (el
  mensaje HUMAN se duplica en el checkpointer tras Retry: `_initial_state` reinserta el user
  y `add_messages` anade), BUG-020 (indexacion de material grande sin limites/progreso/
  cancelacion: 8000 paginas ~29 h de embeddings, satura exam_embedding_service y bloquea
  uploads), BUG-021 (persist=false de /exams/generate persiste igualmente fila+PDFs+ZIP,
  `nodes.py` ~627 incondicional). Decisiones abiertas para el propietario: DEC-001 (semantica
  de persist), DEC-002 (dedupe HUMAN), DEC-003 (limites de indexacion). .ops actualizado:
  IMPL-023, test-plan (C21-C24 + resultados ronda 6), traceability, READMEs qa/decisions,
  BUG-016/018 cerrados con evidencia, handoff.
* **Falta:** fixes de BUG-019/020/021 tras las DEC-001/002/003; escritura de la tesis;
  BL-010 Playwright suite; etapa 01 (repos remotos + CI); inconsistencia validate.yml.
* **Decision:** los 3 bugs nuevos quedan `abierto` con DEC abierta: el agente no cierra
  decisiones ni inventa fixes sin decision del propietario (regla .ops). La sonda 2 de
  BUG-018 dejo el examen "SondaR6Anidada" en la lista Exams: es consecuencia de BUG-021,
  no regresion de BUG-018.
* **Medicion:** 3 restarts/0 401; PDF 5.4 MB -> 211 chunks / ~20 min; caso extremo 6.86 MB
  -> ~41,500 chunks / ~29 h estimadas de embeddings (CPU, batch 16 @ ~90 s); llm_responses
  3250 filas; export XLSX con 1 pregunta; 0 DELETEs del guardrail; toggle idioma persistente
  tras reload.

## 2026-10-26 (RC2 tag + rama RC3/develop)

* **Hecho:** commit de docs pendientes (`5d5a6f3`); tag `RC2` anotado y publicado en los 7
  repos (meta + 6 submodulos); rama `RC3/develop` creada y publicada en los 7 repos. Fixes de
  bugs conocidos (IMPL-022): BUG-018 `ConfigDict(extra="forbid")` en `ExamBlueprint` (core,
  verificado con script desechable: raiz invalida -> 422, metadata anidada OK, tool del agente
  OK, round-trip DB OK); BUG-016 retry unico de 401 re-leyendo `mvp_auth` con chequeo de `exp`
  (`http.ts`); BL-008 RFC-10 persistencia de materia activa (`mvp_active_subject`,
  `stores/subjects.ts`) y RFC-11 rehidratacion de la burbuja tras Retry (`loadThread(id, false)`
  + watch en `ChatPanel.vue`). Frontend build (178 modulos) y vue-tsc OK. Docs .ops
  actualizados (IMPL-022 + indices + BUG/BL + traceability + handoff).
* **Falta:** verificacion en navegador del propietario (C8 retry 401, F5 materia activa,
  reinicio exam_app, sondas HTTP del BUG-018); escritura de la tesis; C2 con PDF grande;
  BL-010 Playwright; inconsistencia validate.yml (infra DigitalMe ausente).
* **Decision:** todos los repos trabajan en `RC3/develop`; `RC2` queda como tag de linea
  base. Los BUG pasan a `resuelto` con fix aplicado; el estado `verified` sigue reservado
  al propietario.
* **Medicion:** build del frontend 178 modulos / 5.50 s; vue-tsc sin errores; 4 sondas de
  BUG-018 OK; tag y rama presentes en origin en los 7 repos.

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

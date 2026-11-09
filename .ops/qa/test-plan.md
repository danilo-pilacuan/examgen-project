---
id: qa-test-plan
tipo: Guide
type: Guide
title: Plan de pruebas y matriz de certificacion
description: Checks C1-C54, F1-F14, I1-I8, E1-E5 (P0-P2) y regresion R1-R7 con estado de certificacion por ronda; ronda 10 usa la suite Playwright versionada BL-010.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [qa-strategy, REQ-001]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

Matriz de certificacion E2E. Rondas: 1=2026-10-19 (IMPL-013), 2=2026-10-23 (IMPL-015), 3=2026-10-23 (IMPL-016), 4=2026-10-26 (IMPL-019), 5=2026-10-26 (IMPL-021), 6=2026-10-27 (IMPL-023).

## P0 - caso de uso central

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C1 | Login multi-profesor + registro de materia | 1, 2, 3 | QT-001 |
| C2 | Subida material >= 5 MB sin 413 | pendiente re-test PDF grande real | BUG-005/QT-001 |
| C3 | Examen por chat completo con ZIP de 2 versiones | 1, 3 | BUG-003/007/QT-001 |
| C4 | El examen aparece solo en la vista de esa materia | 2 | BUG-008/BUG-014/QT-002 |
| C5 | Formulario Exams genera y refresca | 1, 3 | BUG-002/QT-001 |
| C6 | Pipeline sin items aprobados no publica | 1, 3 | BUG-004/QT-001 |

## P1 - HITL y consistencia

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C7 | QuestionCard Save / Save & verify | 3 | BUG-001/QT-001 |
| C8 | Stream muerto -> aviso + Retry | 3 | BUG-006/007/QT-001 |
| C9 | Guardado HITL idempotente tras stream muerto | 3 | BUG-010/QT-001 |
| C10 | Contadores de contexto al cambiar materia | 3 | BUG-009/QT-001 |

## P2 - calidad

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C11 | HEAD /output + Content-Disposition | 3 | BUG-011/QT-001 |
| C12 | Errores accionables (413/401/403, banner) | 3 | BUG-012/QT-001 |
| C13 | Tablas markdown scrollean en la burbuja | 3 | QT-001 (ISS-10) |

## P2 - ronda 4 (navegacion y scroll)

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C14 | Scroll completo en Exams/Bank/Subjects/Material | 4 | BUG-017/QT-004 |
| C15 | Toggle verificacion via nginx (PUT) | 4, 5 | BUG-017b/QT-004 |

## P2 - ronda 5 (regresion API tras instruccionado)

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C16 | Routing nginx Accept json + SPA fallback + OPTIONS/HEAD + /output 404 | 5 | IMPL-021 |
| C17 | Auth 401 sin token + aislamiento multi-tenant del sonda | 5 | IMPL-021 |
| C18 | Validacion 422 accionable en POST /exams/generate | 5 | IMPL-021/C12 |
| C19 | Generacion E2E banco vacio: LLM, PDFs, zip, /output, BD | 5 | IMPL-021 |
| C20 | DELETE /questions/{id} borra y persiste | 5 | IMPL-021 |

## Ronda 6 (certificacion RC3, 2026-10-27, IMPL-023)

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| C21 | BUG-018: sondas HTTP raiz 422 / metadata anidada 200+num_versions=2 | 6 | BUG-018/IMPL-022 |
| C22 | RFC-10: materia activa persiste tras hard reload | 6 | BL-008/IMPL-022 |
| C23 | RFC-11: abort stream -> Retry -> rehidratacion sin duplicar contenido | 6 | BL-008/C8 |
| C24 | BUG-016: 3 restarts exam_app con sesion activa, 0 401 | 6 | BUG-016/RFC-12 |
| C2 | PDF grande real 5.4 MB: sin 413, 211 chunks, RAG con el material | 6 | BUG-005/QT-001 |

Resultado ronda 6: C21 PASS, C22 PASS, C23 PASS, C24 PASS (3/3 restarts),
C2 PASS nominal (5.4 MB); caso extremo 6.86 MB destapo BUG-020 (29 h de
embeddings, sin progreso/cancelacion). Hallazgos nuevos: BUG-019 (HUMAN
duplicado en checkpointer tras Retry), BUG-021 (persist=false persiste
examen); decisiones abiertas DEC-001/002/003.

## Ronda 7 (recertificacion QA 2026-10-27, IMPL-024)

Mandato del propietario: recertificacion con pruebas funcionales
(Playwright, navegador real) y de integracion (API/nginx/BD), sin
unitarias. Bug reportado: "no veo conversaciones pasadas en el historial".

| Check | Tipo | Descripcion | Resultado | Bug/QT |
|---|---|---|---|---|
| C25 | Funcional | Repro del reporte: limpiar `mvp_chat_threads` + reload -> sidebar 0 con hilos en BD | FAIL -> BUG-023 | BUG-023/QT-007 |
| C26 | Funcional | Mismo navegador: 2 hilos listados e hidratados al hacer click (contenido completo) | PASS | QT-007 |
| C27 | Funcional | Logout/login conserva e hidrata los hilos (mismo navegador) | PASS | QT-007 |
| C28 | Funcional | Banco: 200 filas scrollable, filtros dificultad/verificacion, toggle Pending->Human->Pending | PASS | QT-007 |
| C29 | Funcional | Examenes: listado con enlaces Download ZIP/PDF | PASS | QT-007 |
| C30 | Funcional | Material: chunks visibles, botones Delete/Delete-all | PASS | QT-007 |
| C31 | Funcional | Materias: crear via UI (sin delete en UI ni API) | PASS (nota) | QT-007 |
| C32 | Funcional | Chat con materia activa: indicador Context + respuesta que usa el asunto | PASS | QT-007 |
| C33 | Funcional | Reload duro conserva sesion, materia activa y hilos | PASS | QT-007 |
| C34 | Funcional | Guardia de ruta anonima -> /login?redirect=/; login invalido muestra mensaje (texto enganoso) | PASS (nota) | BUG-025/QT-007 |
| C35 | Integracion | BUG-022: usuario B lee (200) y escribe (POST agrega mensajes) el hilo de A | FAIL -> BUG-022 | BUG-022/QT-007 |
| C36 | Integracion | Aislamiento materias: B -> preguntas/examenes/material de A -> 403 | PASS (nota semillas) | QT-007 |
| C37 | Integracion | Auth: 422 password debil, 409 email duplicado, 401 password invalida, /auth/me correcto | PASS | QT-007 |
| C38 | Integracion | Toggle verificacion PUT via nginx + guardrail DELETE de verificada -> 403 | PASS | QT-007 |
| C39 | Integracion | nginx: sin HSTS/X-Content-Type-Options/X-Frame-Options | FAIL -> BUG-024 | BUG-024/QT-007 |
| C40 | Integracion | BUG-019 matizado: hilo nuevo por stream con roles limpios user,assistant (sin HUMAN doble); duplicado solo en Retry | PASS (nota) | BUG-019/QT-007 |

Resultado ronda 7: 11 PASS, 3 FAIL (BUG-022 critico, BUG-023 alto -el bug
reportado-, BUG-024 low/medium), 2 PASS con nota (BUG-025 menor; semillas
sin owner escribibles por cualquiera). Generacion E2E de examen omitida:
cubo LLM largo ya certificado en C19 (ronda 5) y C2 (ronda 6).

## Ronda 8 (fix hilos chat 2026-10-27, IMPL-025)

Fix de DEC-004 (a extendida): hilos de chat server-side con owner, listado
server-side con badges (ultima materia + contador de mensajes) y titulo
fijado al primer mensaje. Ejecucion: scripts/verify-threads-r8.ps1 (API
directa, qa-r8-a/qa-r8-b) + Playwright (qa-r7, navegador real).

| Check | Tipo | Descripcion | Resultado | Bug/QT |
|---|---|---|---|---|
| C41 | Integracion | Login A/B; listas iniciales vacias por usuario (A=0, B=0) | PASS | QT-008 |
| C42 | Integracion | Primer turno de A registra fila en chat_threads con titulo fijado (primer mensaje, 200 chars) y message_count=2 | PASS | QT-008 |
| C43 | Integracion | BUG-022 fix: B lee history del hilo de A -> 403 (antes 200) | PASS | BUG-022/QT-008 |
| C44 | Integracion | BUG-022 fix: B escribe en el hilo de A (POST /api/chat) -> 403 | PASS | BUG-022/QT-008 |
| C45 | Integracion | BUG-022 fix: B renombra (PATCH) el hilo de A -> 403 | PASS | BUG-022/QT-008 |
| C46 | Integracion | BUG-022 fix: B borra (DELETE) el hilo de A -> 403 | PASS | BUG-022/QT-008 |
| C47 | Integracion | Aislamiento de listado: GET /api/chat/threads de B no contiene hilos de A | PASS | BUG-022/QT-008 |
| C48 | Integracion | Sin token -> GET /api/chat/threads 401 | PASS | QT-008 |
| C49 | Integracion | Segundo turno: titulo sigue fijado, message_count=4, last_subject_name actualizado | PASS | QT-008 |
| C50 | Integracion | Operaciones propias: A renombra (200) y borra su hilo (fila fuera del listado y de la BD) | PASS | QT-008 |
| C51 | Funcional | BUG-023 fix (Playwright): reload del navegador conserva la conversacion en la sidebar; click hidrata desde el checkpointer | PASS | BUG-023/QT-008 |
| C52 | Funcional | Badges (Playwright): chip de ultima materia usada ("QA R7 Recert") + contador de mensajes ("4") visibles en el listado | PASS | QT-008 |
| C53 | Funcional | Delete en la sidebar elimina la entrada; chat_threads count=0 en BD (contenido del checkpointer se conserva, purga fuera de alcance) | PASS (nota) | QT-008 |
| C54 | Funcional (UX) | Banco: filas expandibles inline — click/Enter expande el detalle justo bajo la fila (tr.detail-row), chevron rota 90 grados, cierra por X o segundo clic, switch de fila mantiene una sola seleccion, hover/focus affordance, 0 errores de consola | PASS | QT-008 |

Resultado ronda 8: 12 PASS + 1 PASS con nota (purga del checkpointer
pendiente como seguimiento) + 1 PASS UX (C54, anexo del mismo dia: detalle
del Banco expandible inline). BUG-022 y BUG-023 corregidos; verificacion
final pendiente del propietario (QT-008).

## Ronda 9 (recertificacion QA 2026-10-27, IMPL-026)

Mandato del propietario: recertificacion de nuevo con pruebas funcionales
(Playwright, navegador real, el agente actua como humano verificador) y de
integracion (API/nginx/BD), sin unitarias; ademas certificar el caso de uso
de examenes que la ronda 7 omitio. Cuentas de control: qa-r7 (A) y
qa-r7-b (B), contrasenas restablecidas en la sesion. Datos semilla heredados
(Economia Aplicada Eva/Lucia: 497 preguntas, 82 chunks) visibles por el
fallback legacy (owner NULL) para ambos usuarios.

| Check | Tipo | Descripcion | Resultado | Bug/QT |
|---|---|---|---|---|
| F1 | Funcional | Login A -> / con nombre del profesor visible | PASS (sesion persistente valida; "QA Round 7" en header) | QT-009 |
| F2 | Funcional | Bancos: materias semilla listan preguntas; 200+ filas scrolleables; filtros dificultad/verificacion | PASS (Eva 200 preguntas API-limit; filtro hard 49/49; scrollHeight 10387 > clientHeight 515) | QT-009 |
| F3 | Funcional | Detalle expandible inline (chevron, X, una sola seleccion) - anexo UX ronda 8 | PASS (tr.detail-row, cierre por click/X, expandedRows=1) | QT-009 |
| F4 | Funcional | Toggle verificacion Pending->Human->Pending desde la UI | PASS (PUT 200 verificado; nota: la celda in-place queda desactualizada por re-orden de la lista) | QT-009 |
| F5 | Funcional | Examenes: listado con enlaces Download ZIP/PDF funcionales | PASS (ZIP GET 200 128KB cd=attachment; PDF GET 200 41KB; HEAD 200) | QT-009 |
| F6 | Funcional | Material: chunks visibles, Delete/Delete-all presentes | PASS (evaluation 41 chunks expandibles, botones Delete y Delete all) | QT-009 |
| F7 | Funcional | Materias: crear via UI y queda activa | PASS ("QA R9 Recert" creada, activa y en combobox; API no expone DELETE de materias, limpieza via BD) | QT-009 |
| F8 | Funcional | Chat con materia activa: indicador Context + respuesta usa el asunto | PASS ("Context: Eva" + respuesta cita archivo evaluation 41 chunks) | QT-009 |
| F9 | Funcional | Sidebar hilos server-side: badges, click hidrata, reload duro conserva | PASS con BUG (hidratacion e historial OK tras reload; al restaurar el asunto activo las estadisticas 0/0 hasta re-seleccion manual) | BUG-026 |
| F10 | Funcional | Logout/login conserva e hidrata los hilos | PASS (tras re-login el hilo aparece con badge de materia y 6 mensajes) | QT-009 |
| F11 | Funcional (re) | Ruta anonima -> /login?redirect=/ | PASS (/bank anonimo redirige a /login) | QT-007/009 |
| F12 | Funcional (re) | Guardrail anti-borrado de verificadas (API 403 + agente se niega) | PASS (DELETE 403; agente se niega en chat y la pregunta sigue en BD) | R2/QT-009 |
| F13 | Funcional (re) | Aislamiento de materias e hilos entre A y B | PASS (B solo ve 5 semillas; hilo de A invisible para B en UI) | QT-007/009 |
| I1 | Integracion | GET /api/chat/threads sin token -> 401 | PASS (threads/subjects/auth/me -> 401 via nginx) | QT-008/009 |
| I2 | Integracion | B: history/write/rename/delete del hilo de A -> 403 (BUG-022 fix) | PASS (403 "Thread belongs to another user" en GET/PATCH/DELETE; hilo intacto) | BUG-022/QT-009 |
| I3 | Integracion | Toggle verificacion PUT via nginx + guardrail DELETE verificada -> 403 | PASS (PUT verified=true 200; DELETE 403; restore ok; nota: campo del body es "verified") | QT-007/009 |
| I4 | Integracion | nginx cabeceras de seguridad (BUG-024 conocido, sin fix planificado) | FAIL conocido (sin X-Frame-Options, X-Content-Type-Options, CSP, HSTS, Referrer-Policy) | BUG-024/QT-009 |
| I5 | Integracion | Auth: 422 password debil, 409 email duplicado, 401 password invalida, /auth/me | PASS (422 cuerpo invalido, 422 duplicado, 401 credenciales, /auth/me 200, token invalido 401; nota BUG-025: mensaje de error enganoso) | BUG-025/QT-009 |
| I6 | Integracion | Aislamiento materias: A -> preguntas/examenes de B; legacy visible (nota) | PASS (403 en preguntas/examenes/material cruzados; legacy legible por ambos por diseno) | QT-009 |
| E1 | Funcional | Examen via formulario Exams (materia semilla B): POST /exams/generate 200 | PASS con nota (QA_R9_Cert: POST 200, 8 llamadas LLM, 1 rechazo por difficulty_mismatch, 3/4 items publicados; "indexed_chunks_count:0" en respuesta pese a 41 chunks en BD - ver E5) | BUG-027/QT-009 |
| E2 | Funcional | ZIP con 2 versiones (con/sin respuestas) descargable | PASS (QA_R9_Cert.zip 175KB con A/B + A/B_respondido; Content-Disposition attachment) | QT-009 |
| E3 | Funcional | PDFs en /output con Content-Disposition; HEAD no 405 | PASS (A.pdf 39425 B, CT application/pdf, CD attachment; HEAD 200) | QT-009 |
| E4 | Funcional | Examen nuevo aparece solo en la vista de su materia (propietario) | PASS con nota (materia propietaria lo lista; B bloqueado 403 en materias propias de A; seeds legacy visibles a ambos por diseno) | QT-009 |
| E5 | Funcional | Pipeline sin items aprobados no publica examen | FAIL (materia con 0 chunks y 0 preguntas genero 2 preguntas genericas fuera de tema ("Sahara Desert") y las publico con ZIP/PDF) | BUG-027/QT-009 |

Resultado ronda 9: 22 PASS / 2 FAIL (I4 conocido BUG-024 sin fix planificado;
E5/F12-chat -> BUG-027 nuevo: el pipeline publica examenes sin material
indexado y sin banco, con preguntas genericas fuera de tema; E1 detecta
ademas "indexed_chunks_count:0" en la respuesta pese a tener 41 chunks).
BUG-026 nuevo (menor): estadisticas de cabecera 0/0 hasta re-seleccion manual
del asunto tras restauracion.

## Ronda 10 (recertificacion QA 2026-10-28, IMPL-027, QT-010)

Mandato del propietario: recertificar lo esencial Y estrenar el framework de
pruebas versionado BL-010 (Playwright e2e en projects/frontend/e2e); ademas
verificar el contrato de idioma: TODO el sistema en ingles (UI, preguntas y
respuestas generadas). Cuenta de control nueva: qa-r10 (creada en BD con hash
pbkdf2 del backend). La suite queda versionada: `npx playwright test` en
projects/frontend (15 tests: functional F, integration I, language L).

Framework BL-010 (QT-010): playwright.config.ts (baseURL E2E_BASE_URL,
1 worker, trace/screenshot on failure), e2e/helpers.ts (login UI + fixture
authedPage), e2e/tests/functional.spec.ts (F1/F1b/F2/F3/F4/F5/F11/F12),
e2e/tests/integration.spec.ts (I1/I5/I8/I-bonus), e2e/tests/language.spec.ts
(L1/L1b/L2). Credenciales via E2E_EMAIL/E2E_PASSWORD (ver e2e/.env.example).

| Check | Tipo | Descripcion | Resultado | Bug/QT |
|---|---|---|---|---|
| F1 | Funcional | Login UI en ingles: titulo, boton Sign in, html lang=en | PASS (292ms) | QT-010 |
| F1b | Funcional | Login aterriza en chat con nombre del profesor | PASS ("QA Round 10" en header) | QT-010 |
| F2 | Funcional | Banco: seleccion de materia, tabla, filtros | PASS (Eva: tabla visible, filtro easy reacciona) | QT-010 |
| F3 | Funcional | Detalle inline expandible/cerrable | PASS (tr.detail-row abre y cierra) | QT-010 |
| F4 | Funcional | Toggle verificacion desde fila | PASS (cambia a estado verificado) | QT-010 |
| F5 | Funcional | Examenes: listado y boton ZIP habilitado | PASS (.exam-list con button.zip) | QT-010 |
| F11 | Funcional (re) | Ruta anonima -> /login?redirect= | PASS (211ms) | QT-010 |
| F12 | Funcional (re) | Guardrail DELETE pregunta inexistente -> 403/404 | PASS (404; guardrail de verificadas re-testeado en ronda 9) | QT-010 |
| I1 | Integracion | API sin token -> 401 (/api/chat/threads, /subjects, /auth/me via nginx) | PASS (3/3 -> 401) | QT-010 |
| I5 | Integracion | Auth: 422 password debil, 401 credenciales invalidas | PASS (422/401) | QT-010 |
| I8 | Integracion | HEAD /output/ -> 200/404, nunca 405 | PASS (200) | QT-010 |
| I-bonus | Integracion | Token de localStorage valido en /auth/me | PASS (200 + email correcto) | QT-010 |
| L1 | Idioma | Perfil limpio: UI en ingles (html lang=en, textos EN) | PASS | QT-010 |
| L1b | Idioma | Nav principal en ingles (Chat/Bank/Exams/Material/Subjects) | PASS | QT-010 |
| L2 | Idioma | Informe idioma del banco (informativo, no falla) | INFORMATIVO (muestra=200, en espanol=197: banco heredado pre-contracto, ver BUG-028) | BUG-028/QT-010 |
| E1-EN | Funcional | Generacion examen con prompts en ingles (backend reconstruido): POST /exams/generate | PASS (QA_R10_English_Gen: 3 items generados; statements, opciones, respuestas y explicaciones 100% en ingles; 2 PDFs + ZIP en /output; pipeline aprobo los 3 items sin rechazo de idioma) | QT-010 |

Resultado ronda 10: 15/15 PASS en la suite Playwright versionada + E1-EN PASS.
El contrato de idioma queda enforceado en codigo (prompts de generacion,
evaluador y verificador exigen ingles; el evaluador rechaza items en otro
idioma con rejection_reason=language_not_english). El banco heredado
(933/1239 preguntas en espanol) queda registrado como BUG-028: dato semilla
anterior al contrato, no defecto de codigo; decision pendiente del propietario
(remediar/traducir o dejar como legado).

## Ronda 11 (recertificacion QA 2026-10-28, IMPL-028, QT-011)

Mandato del propietario: recertificar lo primordial, regenerar el framework
de pruebas, asegurar ingles en TODO el sistema (preguntas y respuestas
incluidas), regenerar el set completo de metricas de medicion y reconstruir
la BD desde cero. El agente actua como verificador humano (derecho HITL
otorgado explicitamente). Cuenta de control: qa-r11@usfq.test. Decision
BUG-028 ejecutada: opcion (c) purga + regeneracion.

| Check | Tipo | Descripcion | Resultado | Bug/QT |
|---|---|---|---|---|
| DB-1 | Datos | BD desde cero: drop + alembic upgrade head (b8c9d0e1f2a3, 13 tablas), 0 registros heredados | PASS | QT-011 |
| DB-2 | Datos | Material re-indexado: Database Systems 28 chunks, Economia Aplicada - QA11 51 chunks (79 total) | PASS | QT-011 |
| DB-3 | Datos | 12 preguntas nuevas (6 por materia) generadas via pipeline real, source=pipeline, 100% en ingles (statements, opciones, respuestas, explicaciones) | PASS | QT-011 |
| HITL-1 | Humana (agente) | Revision docente de las 12 preguntas (exactitud, distractores, dificultad, redaccion) | PASS 12/12 APROBADAS | QT-011 |
| HITL-2 | Humana (agente) | 2 sospechas de mojibake (beta U+03B2, por U+00D7) investigadas: UTF-8 real en BD y API; artefacto de consola cp1252 de PowerShell 5.1 (simbolos matematicos, no espanol) | PASS (falso positivo descartado) | QT-011 |
| HITL-3 | Humana (agente) | Marcado verified_by_human=true en 12/12 via PUT /questions/{id}/verification {"verified":true} | PASS (12/12=t en BD) | QT-011 |
| F-serie | Funcional | Suite Playwright versionada ronda 11 (helpers + specs actualizados a qa-r11) | PASS 15/15 (10.8 s) | QT-011 |
| L2 | Idioma | Prueba de idioma del banco endurecida de informativa a asercion estricta (0 preguntas con espanol en la muestra) | PASS (toHaveLength(0)) | BUG-028/QT-011 |
| E1-EN | Funcional | 2 examenes de control en ingles compilan (qa11_control_db, qa11_control_econ) con PDFs con/sin respuestas + ZIP en data/agent_outputs | PASS | QT-011 |
| EVAL-1 | Evaluacion | subjects.yaml regenerado: 5 clones en ingles adam/bella/carlos/diana/esteban ("Applied Economics - X"), mismo material_glob | PASS | QT-011 |
| EVAL-2 | Evaluacion | experiments.yaml regenerado: topics_weight en ingles (Market Study 0.3, Financial Flows 0.3, Economic and Financial Analysis 0.25, Pricing 0.15; suma 1.0); 82 runs validados (E01=27, E02=27, E03=10, E04=18) | PASS | QT-011 |
| EVAL-3 | Evaluacion | Smoke dry-run: 6 familias de metricas computadas, nombres en ingles; polucion del smoke purgada (FK-order) | PASS | QT-011 |
| EVAL-4 | Evaluacion | Campana REAL 82 runs completada (E04 18, E03 10, E01 27, E02 27; 0 fallidos, exit 0). BUG-029 corregido (docx/pptx indexan 200, 85 chunks). Defecto nuevo en el juez: num_judged=0 en las 82 corridas (juez recibia registros sin correlacionar); correlacion corregida en harness.py para futuras corridas. Agregados + reportes generados para E01-E04. Spot-check ingles (HITL): 621 items escaneados, 0 en espanol en cuerpo; 13/621 con nombres propios o glosas del material (Maria, Cafe Aroma, "(Estudio de Mercado)"), 3/621 subtopic con eco del temario; evaluador rechazo 5 items language_not_english | DONE (juez post-hoc abortado por ventana +-1 fila: ver hallazgo J1) | QT-011 |
| ADV-1 | Adversarial | Indexar solo docx (Economia Aplicada) con clear=true: debe fallar y NO perder chunks | 400 "Could not extract text" + chunks intactos 51/51 -> BUG-029 (No module named 'docx'; python-docx/python-pptx no declarados) | BUG-029/QT-011 |

Resultado ronda 11: certificacion funcional PASS (DB + HITL + suite 15/15 +
examenes de control en ingles); BUG-028 -> corregido (purga y regeneracion
verificadas: 0 preguntas en espanol en BD); BUG-029 -> corregido (deps
declaradas, imagen reconstruida, indexacion docx/pptx verificada en vivo
200/200/200 con 85 chunks). Campana 82/82 completada; agregados e informes
por experimento generados; defecto del juez in-run (num_judged=0) corregido
en harness; ingles verificado por escaneo (621 items) y lectura HITL.

## Regresion

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| R1 | HITL textual (guardar + verificar por chat) | 1, 2, 3 | QT-001 |
| R2 | Guardrail anti-borrado de preguntas verificadas | 1, 3, 7 | QT-001, QT-007 |
| R3 | Selector de materia sincronizado | 1, 2 | QT-001 |
| R4 | Banco: filtros, detalle, toggle | 1, 3 | QT-001 |
| R5 | Exportaciones CSV/XLSX/JSON | 1, 3, 6 | QT-001 |
| R6 | Auditoria LLM filas nuevas | 1, 3, 6 | QT-001 |
| R7 | Idioma: prompt espanol -> respuesta ingles | 1, 3 | QT-001 |

Resultados ronda 6 (regresion):

- R1 HITL textual PASS: "yes" guardo la pregunta de pilas/colas como
  verified-by-human (id `a8571657-6a54-4b02-a178-a76f2b75a82f`), widget
  QuestionCard, verificacion IA "approved (high priority)".
- R2 Guardrail PASS: "Borra todas las preguntas" -> el agente se nego
  (proteccion verified-by-human), ningun DELETE emitido, BD conserva la
  pregunta.
- R4 Exportaciones PASS via chat (tool `export_questions`, no hay botones
  de UI): "Exporta en Excel" -> `questions_20261027_172726.xlsx` con la
  1 pregunta del banco y link de descarga funcional. Hallazgo menor: la
  auto-adjuncion al chat fallo ("the file could not be auto-attached") y
  cayo al link; el artifact card inicial mostro el link pero sin emoji
  correcto hasta el segundo intento del agente.
- R5 Auditoria LLM PASS: `llm_responses` con 3250 filas; el thread de la
  ronda registro cada llamada con context `chat:model`, model
  `zai-org/GLM-5.3-Flash`, latencia y timestamp (18+ filas del turno).
- R6 Idioma PASS: toggle EN/ES en el header cambia nav, titulo y textos
  (Banco/Examenes/Materias), persiste en localStorage (`mvp_locale`) tras
  reload y se restauro a EN al final. Nota menor: tras reload,
  `document.documentElement.lang` queda "en" aunque la UI este en ES (el
  atributo solo se re-sincroniza al click; RFC-10 usa su propia key).
- R3/R7 omitidos esta ronda: R3 (selector sincronizado) cubierto por
  C22/RFC-10; R7 requiere LLM en ingles, cubierto indirectamente por el
  agente respondiendo en el idioma del prompt durante R1/R2.

Conversion futura de esta matriz a suite versionada: BL-010 (Playwright e2e).
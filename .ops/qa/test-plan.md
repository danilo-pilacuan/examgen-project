---
id: qa-test-plan
tipo: Guide
type: Guide
title: Plan de pruebas y matriz de certificacion
description: Checks C1-C20 (P0-P2) y regresion R1-R7 con estado de certificacion por ronda.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-27
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

Resultado ronda 8: 12 PASS + 1 PASS con nota (purga del checkpointer
pendiente como seguimiento). BUG-022 y BUG-023 corregidos; verificacion
final pendiente del propietario (QT-008).

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
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

## Regresion

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| R1 | HITL textual (guardar + verificar por chat) | 1, 2, 3 | QT-001 |
| R2 | Guardrail anti-borrado de preguntas verificadas | 1, 3 | QT-001 |
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
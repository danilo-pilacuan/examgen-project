---
id: qa-test-plan
tipo: Guide
type: Guide
title: Plan de pruebas y matriz de certificacion
description: Checks C1-C13 (P0-P2) y regresion R1-R7 con estado de certificacion por ronda.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [qa-strategy, REQ-001]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

Matriz de certificacion E2E. Rondas: 1=2026-10-19 (IMPL-013), 2=2026-10-23 (IMPL-015), 3=2026-10-23 (IMPL-016), 4=2026-10-26 (IMPL-019), 5=2026-10-26 (IMPL-021).

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

## Regresion

| Check | Descripcion | Round | Bug/QT |
|---|---|---|---|
| R1 | HITL textual (guardar + verificar por chat) | 1, 2, 3 | QT-001 |
| R2 | Guardrail anti-borrado de preguntas verificadas | 1, 3 | QT-001 |
| R3 | Selector de materia sincronizado | 1, 2 | QT-001 |
| R4 | Banco: filtros, detalle, toggle | 1, 3 | QT-001 |
| R5 | Exportaciones CSV/XLSX/JSON | 1, 3 | QT-001 |
| R6 | Auditoria LLM filas nuevas | 1, 3 | QT-001 |
| R7 | Idioma: prompt espanol -> respuesta ingles | 1, 3 | QT-001 |

Conversion futura de esta matriz a suite versionada: BL-010 (Playwright e2e).
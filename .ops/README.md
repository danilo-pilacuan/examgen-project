---
id: ops-readme
tipo: Guide
type: Guide
title: Indice raiz del arbol .ops de Exam Generator
description: Mapa del ciclo de vida del proyecto y punto de entrada de la gobernanza.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [templates-base]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

Arbol de ciclo de vida de Exam Generator (tesis USFQ, MVP de generacion de examenes con
agente conversacional HITL). Sustituye a la antigua carpeta `implementaciones/`.
Politica de proceso: seccion 1 de `.github/copilot-instructions.md`. Reglas duras: ids
unicos globales; documentos de contenido menores a ~40 lineas; READMEs de carpeta de
maximo 15 lineas; el agente nunca escribe `verified`; sin diacriticos.

| Direccion | Contenido |
|---|---|
| `product/` | REQ-001 mvp-flujo-profesor (aprobado), REQ-002 evaluacion-agente (aprobado), REQ-003 repos-y-ci (propuesto) |
| `project/` | plan.md (mapa de etapas y estados), handoff.md (entrada de sesion), backlog/ BL-001..BL-021 |
| `architecture/` | (vacio) NFR y threat model pendientes |
| `decisions/` | (vacio) registro DEC sin abiertas; decisiones historicas viven en los IMPL |
| `governance/` | (vacio) charter y RACI pendientes |
| `qa/` | BUG-001..BUG-017b (rondas 1-4), traceability.md (REQ-BL-IMPL-QT) |
| `implementations/` | IMPL-000..IMPL-020 (etapas 00-16 + migracion) |
| `ux-and-interfaces/` | (vacio) convenciones CLI/UX pendientes |
| `templates/` | base.md (contrato OKF 0.2 intacto) + plantillas por tipo |

Entrada de sesion: `project/handoff.md` -> `../../PROGRESS.md` -> `project/plan.md` ->
el IMPL activo. Progreso diario: `../../PROGRESS.md` (fuente unica de verdad).
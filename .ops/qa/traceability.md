---
id: traceability
tipo: Guide
type: Guide
title: Matriz de trazabilidad REQ -> BL -> IMPL -> QT
description: Cobertura con estado y evidencia; la fuente de la cadena de trazabilidad.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [qa-test-plan, templates-base]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

| REQ | BL | IMPL | QT | Estado y evidencia |
|---|---|---|---|---|
| REQ-001 | BL-001 | IMPL-000 | QT-001 | ejecutado; monorepo operante, informes RC1 |
| REQ-001 | BL-002 | IMPL-002, 003, 004, 012 | QT-001 | ejecutado; backend+SSE+pipeline certificados (rondas 1-3) |
| REQ-001 | BL-003 | IMPL-005, 006, 007 | QT-001 | ejecutado; UI completa, R1-R7 |
| REQ-001 | BL-004 | IMPL-008 | QT-001 | ejecutado; stack 6/6 healthy en 4 rondas |
| REQ-001 | BL-005 | IMPL-009 | QT-001 | ejecutado; R7 en rondas 1 y 3 |
| REQ-001 | BL-006 | IMPL-010 | QT-001 | ejecutado; mapa de dependencias |
| REQ-001 | BL-007 | IMPL-011 | QT-001 | ejecutado; C1/R1/R3 (Tag_V1.0.0) |
| REQ-001 | BL-008 | IMPL-013 | QT-001 | ejecutado; 12 bugs detectados (ronda 1) |
| REQ-001 | BL-009 | IMPL-014 | QT-001 | ejecutado; fixes 11.1-11.6 certificados |
| REQ-001 | BL-011 | IMPL-015 | QT-002 | ejecutado; BUG-013/014 verificados (P1-P9) |
| REQ-001 | BL-012 | IMPL-016 | QT-003 | ejecutado; C1, C5-C13, R1-R7 certificados |
| REQ-001 | BL-015 | IMPL-017 | QT-003 | ejecutado; informe RC1 15/16 bugs corregidos |
| REQ-001 | BL-013 | IMPL-019 | QT-004 | ejecutado; matriz 10 casos ronda 4 |
| REQ-001 | BL-013 | IMPL-021 | QT-004 | ejecutado; ronda 5 regresion API, BUG-017b verificado |
| REQ-002 | BL-019, 020, 021 | IMPL-018 | QT-005 | ejecutado; 102 runs, H1-H5, FINDINGS.md |
| REQ-003 | BL-001 | IMPL-001 | QT-006 | borrador; remotos y CI pendientes |
| REQ-001 | BL-008 | IMPL-022 | QT-003 | en_curso; BUG-016 fix + RFC-10/11 en RC3/develop (browser pending) |
| REQ-001 | BL-008 | IMPL-022 | QT-005 | resuelto; BUG-018 extra=forbid en RC3/develop (sondas script OK) |

## QT y su estado

| QT | Titulo | estado | Evidencia |
|---|---|---|---|
| QT-001 | Matriz C1-C13 + R1-R7 (rondas 1-3) | aprobada | `.ops/qa/test-plan.md`; bug fixes verificados |
| QT-002 | P1-P9 + R1-R3 ronda 2 (persistencia, registros) | aprobada | BUG-013/BUG-014 |
| QT-003 | Certificacion ronda 3 (checklist etapa 11) | aprobada | IMPL-016, BUG-015 |
| QT-004 | Matriz 10 casos ronda 4 (scroll + toggle) | aprobada | BUG-017/BUG-017b |
| QT-005 | Campana evaluacion E01-E04 (H1-H5) | aprobada | `test/evaluation/` FINDINGS + agregados |
| QT-006 | Clon fresco + CI submodulos | pendiente | no ejecutable aun (IMPL-001) |

Pendientes conocidos: C2 con PDF grande real; verificacion en navegador de BUG-016
y RFC-10/11 (BL-008, IMPL-022); suite versionada BL-010. BUG-016 y BUG-018 quedan
resueltos (fix aplicado en RC3/develop) pendiente verificacion del owner.
---
id: traceability
tipo: Guide
type: Guide
title: Matriz de trazabilidad REQ -> BL -> IMPL -> QT
description: Cobertura con estado y evidencia; la fuente de la cadena de trazabilidad.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-27
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
| REQ-001 | BL-008 | IMPL-022 | QT-003 | resuelto; BUG-016 verificado en navegador ronda 6 (3 restarts, 0 401) + RFC-10/11 PASS (C22/C23) |
| REQ-001 | BL-008 | IMPL-022 | QT-005 | resuelto; BUG-018 sondas HTTP reales ronda 6: raiz 422, metadata 200 num_versions=2 (C21) |
| REQ-001 | BL-008 | IMPL-023 | QT-004 | ejecutado; ronda 6 certificacion RC3: C2 PDF 5.4 MB PASS, R1/R2/R4/R5/R6 PASS, hallazgos BUG-019/020/021 + DEC-001/002/003 |
| REQ-001 | BL-017 | IMPL-024 | QT-007 | ejecutado; ronda 7 recertificacion funcional+integracion: BUG-023 confirmado (listado localStorage, reporte del propietario), BUG-022 critico (hilos sin propiedad, DEC-004), BUG-024/025 nuevos; C25-C40 11 PASS/3 FAIL/2 nota |
| REQ-001 | BL-017 | IMPL-025 | QT-008 | ejecutado; ronda 8 fix DEC-004(a): chat_threads + ownership 403 + listado server-side con badges; API 12/12 PASS (scripts/verify-threads-r8.ps1) + Playwright PASS; BUG-022/023 corregidos (verificado final pendiente del propietario) |

## QT y su estado

| QT | Titulo | estado | Evidencia |
|---|---|---|---|
| QT-001 | Matriz C1-C13 + R1-R7 (rondas 1-3) | aprobada | `.ops/qa/test-plan.md`; bug fixes verificados |
| QT-002 | P1-P9 + R1-R3 ronda 2 (persistencia, registros) | aprobada | BUG-013/BUG-014 |
| QT-003 | Certificacion ronda 3 (checklist etapa 11) | aprobada | IMPL-016, BUG-015 |
| QT-004 | Matriz 10 casos ronda 4 (scroll + toggle) | aprobada | BUG-017/BUG-017b |
| QT-005 | Campana evaluacion E01-E04 (H1-H5) | aprobada | `test/evaluation/` FINDINGS + agregados |
| QT-006 | Clon fresco + CI submodulos | pendiente | no ejecutable aun (IMPL-001) |
| QT-007 | Recertificacion ronda 7 (funcionales Playwright + integracion) | pendiente | test-plan ronda 7; BUG-022/023/024/025; pendiente del propietario |
| QT-008 | Hilos server-side con ownership y badges (ronda 8) | pendiente | IMPL-025; 12/12 API PASS + Playwright PASS; pendiente del propietario |

Pendientes conocidos: suite versionada BL-010 (Playwright e2e); BUG-019/020/021
abiertos (hallazgos ronda 6) con decisiones DEC-001/002/003 pendientes del owner;
C2 caso extremo (>100 paginas reales) bloqueado por BUG-020. BUG-016 y BUG-018
verificados en ronda 6 (navegador + sondas HTTP); quedan resueltos. Ronda 7 anade
BUG-022 (critico, DEC-004), BUG-023 (bug reportado del historial, fix en BL-017),
BUG-024 y BUG-025. Ronda 8 (IMPL-025): BUG-022/023 corregidos via BL-017
(DEC-004 a); QT-008 pendiente de verificacion del propietario; purga del
checkpointer huerfano queda como seguimiento.
---
id: plan
tipo: Guide
type: Guide
title: Plan de etapas y mapa de estados del proyecto
description: Sucesor del README de etapas de implementaciones; estados verificados.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001, ops-readme]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

Mapa de etapas (sucesor de `implementaciones/README.md`). Estados: ejecutado =
completada y verificada E2E en navegador; borrador = pendiente o parcial. Orden de
lectura de etapas QA: 13 -> 14 -> 15 -> 16 -> 17 -> 19.

| Etapa | IMPL | Titulo | Estado |
|---|---|---|---|
| 00 | IMPL-000 | Reestructuracion monorepo | ejecutado |
| 01 | IMPL-001 | Repos y submodulos + CI | borrador (remotos/CI pendientes) |
| 02 | IMPL-002 | Backend reactivo exam-app | ejecutado (token streaming en BL-021) |
| 02b | IMPL-003 | Arquitectura limpia exam-app | ejecutado |
| 02c | IMPL-004 | Arquitectura limpia agents-backend core | ejecutado |
| 03 | IMPL-005 | Frontend base | ejecutado |
| 04 | IMPL-006 | Widgets de chat | ejecutado |
| 05 | IMPL-007 | Pantallas | ejecutado |
| 06 | IMPL-008 | Docker pulido | ejecutado |
| 07 | IMPL-009 | Traduccion a ingles | ejecutado |
| 07a | IMPL-010 | Mapa de dependencias | ejecutado |
| 08 | IMPL-011 | Auth multitenant + navbar reactivo (Tag_V1.0.0) | ejecutado |
| 09 | IMPL-012 | Auditoria raw LLM + JSON en ingles | ejecutado |
| 10 | IMPL-013 | QA ronda 1 flujo completo navegador | ejecutado |
| 11 | IMPL-014 | Correcciones ronda 1 + certificacion | ejecutado |
| 12 | IMPL-015 | QA ronda 2 (persistencia + registros) | ejecutado |
| 13 | IMPL-016 | QA ronda 3 navegador | ejecutado |
| 14 | IMPL-017 | Informe de estado RC1 (Tag_RC1) | ejecutado |
| 15 | IMPL-018 | Framework de evaluacion del agente (RC2) | ejecutado |
| 16 | IMPL-019 | QA ronda 4 scroll + Playwright | ejecutado |

Progreso global: 19 de 20 etapas ejecutadas; abiertos 1 BUG (BUG-016, menor) y el
backlog BL-001..BL-021. La migracion a `.ops` es IMPL-020 (borrador). Detalle en
`../../PROGRESS.md` y `../qa/traceability.md`.
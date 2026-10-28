---
id: implementations-readme
tipo: Guide
type: Guide
title: Implementations index
description: Especificaciones IMPL por fase y convenciones de la fase activa.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [templates-implementation]
status: stable
---

## Index

| IMPL | Title | estado |
|---|---|---|
| IMPL-000 | Reestructuracion del monorepo | ejecutado |
| IMPL-001 | Repos y submodulos + CI | borrador |
| IMPL-002 | Backend reactivo exam-app | ejecutado |
| IMPL-003 | Arquitectura limpia exam-app | ejecutado |
| IMPL-004 | Arquitectura limpia agents-backend | ejecutado |
| IMPL-005 | Frontend base | ejecutado |
| IMPL-006 | Widgets de chat | ejecutado |
| IMPL-007 | Pantallas | ejecutado |
| IMPL-008 | Docker pulido | ejecutado |
| IMPL-009 | Traduccion a ingles | ejecutado |
| IMPL-010 | Mapa de dependencias | ejecutado |
| IMPL-011 | Auth multitenant (Tag_V1.0.0) | ejecutado |
| IMPL-012 | Auditoria raw LLM | ejecutado |
| IMPL-013 | QA ronda 1 | ejecutado |
| IMPL-014 | Correcciones ronda 1 + certificacion | ejecutado |
| IMPL-015 | QA ronda 2 | ejecutado |
| IMPL-016 | QA ronda 3 (certificacion central) | ejecutado |
| IMPL-017 | Informe RC1 (Tag_RC1) | ejecutado |
| IMPL-018 | Framework de evaluacion RC2 | ejecutado |
| IMPL-019 | QA ronda 4 | ejecutado |
| IMPL-020 | Migracion .ops | borrador |
| IMPL-021 | Ronda QA 5 - verificaciones API tras nuevo instruccionado | ejecutado |
| IMPL-022 | RC3 - fixes de bugs conocidos | borrador |
| IMPL-023 | QA ronda 6 (certificacion RC3) | ejecutado |
| IMPL-024 | QA ronda 7 - recertificacion funcional e integracion | ejecutado |
| IMPL-025 | Hilos de chat server-side con ownership y badges | ejecutado |
| IMPL-026 | QA ronda 9 - recertificacion funcional e integracion | ejecutado |
| IMPL-027 | QA ronda 10 - framework e2e versionado (BL-010) y contrato de idioma | ejecutado |
| IMPL-028 | QA ronda 11 - recertificacion, BD desde cero, ingles e2e y set de metricas | ejecutado |
| IMPL-029 | QA ronda 12 - recertificacion funcional, credenciales, BUG-026/027 corregidos | ejecutado |

Naming `IMPL-NNN-slug.md`; global numbering; one file per spec. The active phase
spec is the one linked from `project/handoff.md`. The agent updates estado to the
real verified state (never "I think it works"); only the owner sets `verified`.
---
id: product-readme
tipo: Guide
type: Guide
title: Product - requerimientos y vision
description: REQ aprobados con criterio de aceptacion y no objetivos; fuente la seccion 1 y la 11 de AGENTS.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [ops-readme]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

- **Proposito:** traducir la vision (seccion 1) en requerimientos con criterio de aceptacion trazable.
- **Escribe:** rol:agente (propone) · **Aprueba:** rol:propietario (estado `aprobado`).
- **Cuando:** al derivar un requerimiento nuevo de la seccion 1 o al cerrar una fase que lo materializa.

## Indice de requerimientos

| Id | Titulo | Estado | Fuente de aceptacion |
|---|---|---|---|
| [REQ-001](requirements/REQ-001.md) | Validacion contra schemas y estructura | aprobado | [qa/traceability.md](../qa/traceability.md) QT-001..QT-019 |
| [REQ-002](requirements/REQ-002.md) | Aislamiento multi-tenant L0-L4 | aprobado | [qa/traceability.md](../qa/traceability.md) QT-001..QT-007 |
| [REQ-003](requirements/REQ-003.md) | Integridad epistemica (cita y contra-evidencia) | aprobado | [qa/traceability.md](../qa/traceability.md) QT-008..QT-018 |
| [REQ-004](requirements/REQ-004.md) | Contra-evidencia por dominio (Fase 5) | propuesto | [qa/traceability.md](../qa/traceability.md) QT-018..QT-019 |
| [REQ-005](requirements/REQ-005.md) | Plataforma HTTP de producto | propuesto | [qa/traceability.md](../qa/traceability.md) QT-020 |
| [REQ-006](requirements/REQ-006.md) | Autenticacion multi-org con JWT | propuesto | [qa/traceability.md](../qa/traceability.md) QT-021 |
| [REQ-007](requirements/REQ-007.md) | Agente conversacional con HITL | propuesto | [qa/traceability.md](../qa/traceability.md) QT-022 |
| [REQ-008](requirements/REQ-008.md) | Servicio de embeddings y reindexado | propuesto | [qa/traceability.md](../qa/traceability.md) QT-023 |
| [REQ-009](requirements/REQ-009.md) | Frontend Vue 3 del producto | propuesto | [qa/traceability.md](../qa/traceability.md) QT-024 |

Regla: el titulo, el estado y la cobertura de este indice se mantienen en sincronia con [qa/traceability.md](../qa/traceability.md) y [../project/plan.md](../project/plan.md).

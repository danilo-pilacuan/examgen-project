---
id: implementations-readme
tipo: Guide
type: Guide
title: Implementations - especificaciones por fase
description: Especificaciones fase-0..fase-10 con estado de verificacion y convenciones de implementacion.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [impl-conventions, proj-plan]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

- **Proposito:** especificacion por fase (alcance, tareas, criterio de salida, decisiones) y convenciones transversales de implementacion.
- **Escribe:** rol:agente (redacta y ejecuta) · **Aprueba:** rol:propietario (pasa la especificacion a `verificado` tras ver la evidencia).
- **Cuando:** al iniciar una fase se redacta/actualiza la especificacion; al cerrarla se marca `verificado` con el checklist del DoD.

## Especificaciones por fase

| Fase | Especificacion | Estado |
|---|---|---|
| 0 - Estandar y validador | [fase-0.md](fase-0.md) | verificado |
| 1 - Conocimiento sintetico | [fase-1.md](fase-1.md) | verificado |
| 2 - Indexado, RLS y MCP de lectura | [fase-2.md](fase-2.md) | verificado |
| 3 - Escritura controlada y CI | [fase-3.md](fase-3.md) | verificado |
| 4 - Skills y agentes | [fase-4.md](fase-4.md) | verificado |
| 5 - Promocion E2E y UAT | [fase-5.md](fase-5.md) | verificado |
| 6 - Gobernanza y fundacion de producto | [fase-6.md](fase-6.md) | borrador |
| 7 - MCP HTTP y embeddings bge-m3 | [fase-7.md](fase-7.md) | borrador |
| 8 - BFF FastAPI y agente HITL | [fase-8.md](fase-8.md) | borrador |
| 9 - Frontend Vue 3 | [fase-9.md](fase-9.md) | borrador |
| 10 - Integracion docker y cierre | [fase-10.md](fase-10.md) | borrador |

**Convenciones transversales:** [conventions.md](conventions.md) · **Plantilla:** [../templates/implementation.md](../templates/implementation.md) · **Plan:** [../project/plan.md](../project/plan.md).

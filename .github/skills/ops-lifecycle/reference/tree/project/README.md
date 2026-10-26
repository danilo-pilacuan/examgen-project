---
id: project-readme
tipo: Guide
type: Guide
title: Project - plan, backlog y avance
description: Plan de fases reajustado, backlog de epicas y resumen de avance; el log dia a dia vive en PROGRESS.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [ops-readme, proj-plan, proj-backlog]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

- **Proposito:** planificar las fases (seccion 11), mantener el backlog de epicas y resumir el avance por fase.
- **Escribe:** rol:agente · **Aprueba:** rol:propietario (cambios de plan o alcance).
- **Cuando:** al iniciar una fase, al desglosar una epica y al cerrar una fase (checklist en [../governance/definition-of-done.md](../governance/definition-of-done.md)).

## Documentos

- [plan.md](plan.md) - fases reajustadas al estado real de ejecucion; fases 0-9 verificadas, Fase 10 pendiente.
- [backlog/index.md](backlog/index.md) - epicas por fase; los BL se desglosan al entrar en la fase.
- [handoff.md](handoff.md) - contexto de arranque para nuevas sesiones: estado del producto, entorno, comandos y mapa de documentos.
- Avance: el log tarea a tarea vive en [../../PROGRESS.md](../../PROGRESS.md) (regla 7, DEC-001 rechazada); este arbol no lo duplica.

---
id: decisions-readme
tipo: Guide
type: Guide
title: Decisions - registro de decisiones
description: Espejo OKF de la seccion 12 de AGENTS.md; una DEC por archivo, D1-D8 cerradas, D3 reabierta y DEC-011..013 del producto pendientes de verificacion.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [ops-readme]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

- **Proposito:** registrar el ciclo de vida de las decisiones de la seccion 12: abierta -> tomada/rechazada, con resolucion verificada por humano.
- **Escribe:** rol:agente (propone, documenta la resolucion) · **Aprueba:** rol:propietario (toma la decision; el agente nunca cierra una DEC por si mismo, regla 6).
- **Cuando:** al abrir una decision antes de la fase que la requiera y al cerrarla con la respuesta del propietario.

## Indice

| DEC | Decision AGENTS.md | Pregunta | Estado |
|---|---|---|---|
| [DEC-001](DEC-001.md) | - | Log de avance en raiz vs mudar a .ops | tomada (permanece en raiz) |
| [DEC-002](DEC-002.md) | - | Anadir .ops/ a la estructura de la seccion 4 | tomada (incluido en v3) |
| [DEC-003](DEC-003.md) | D1 | Entorno de Postgres para desarrollo y CI | tomada (Docker Compose + pgvector) |
| [DEC-004](DEC-004.md) | D2 | Modelo de embeddings y dimension | tomada (multilingual-e5-small, 384 dims) |
| [DEC-005](DEC-005.md) | D3 | Autenticacion para pasar de stdio a HTTP | abierta (resolucion propuesta JWT + MCP interno, pendiente verificacion) |
| [DEC-006](DEC-006.md) | D4 | Creacion de ramas/MR y aprobacion de excepciones | tomada (parcial, Git local) |
| [DEC-007](DEC-007.md) | D5 | Escaner de secretos | tomada (gitleaks en CI) |
| [DEC-008](DEC-008.md) | D6 | Vocabulario controlado de dominio | tomada (15 dominios en el schema) |
| [DEC-009](DEC-009.md) | D7 | Repositorio unico vs por organizacion | tomada (repo por org con core compartido) |
| [DEC-010](DEC-010.md) | D8 | MCP directo vs Code Mode | tomada (MCP directo, opcion 1a) |
| [DEC-011](DEC-011.md) | D2 (revision) | Revision de embeddings para producto | abierta (propuesto bge-m3 1024, pendiente verificacion) |
| [DEC-012](DEC-012.md) | - | Stack de producto (BFF, agentes, frontend) | abierta (propuesto FastAPI+LangGraph+Vue3, pendiente verificacion) |
| [DEC-013](DEC-013.md) | - | Modelo de datos de producto y fronteras | abierta (propuesto esquema app + membership, pendiente verificacion) |
| [DEC-014](DEC-014.md) | - | Ampliar .ops con arboles de disciplinas tecnicas | abierta (propuestos security/, operations/, data/, development/, pendiente verificacion) |

Regla: el indice refleja el frontmatter de cada DEC; la narrativa de cuando y como se decidio cada una vive en [../../PROGRESS.md](../../PROGRESS.md).

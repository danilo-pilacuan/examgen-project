---
id: project-handoff
tipo: Guide
type: Guide
title: Handoff - contexto de continuidad entre sesiones
description: Documento de soporte para pasar contexto completo a una sesion nueva; el agente lo actualiza al cierre de cada tarea y una sesion nueva arranca leyendolo.
estado: vigente
dueno: rol:agente
fecha: 2026-10-26
relaciona: [ops-readme, proj-plan, proj-readme]
status: stable
verified: 2026-10-26T00:00:00Z
---

Documento de soporte (no es codigo): condensa el estado del producto, el
entorno local, los comandos de verificacion y el trabajo pendiente para que
una sesion nueva del agente retome el desarrollo sin reexplorar el repositorio.
La politica de mantenimiento vive en [.github/copilot-instructions.md](../../.github/copilot-instructions.md)
(seccion "Implementation status and handoff policy").

## Como usar este documento

1. **Sesion nueva:** leer primero este documento, despues [../../PROGRESS.md](../../PROGRESS.md)
   (log dia a dia) y el doc de la fase activa en [../implementations/](../implementations/).
2. **Cierre de tarea:** el agente actualiza las secciones "Estado del producto"
   y "Trabajo en curso" y agrega una fila al historial de sesiones.
3. **Plantilla para otros proyectos:** copiar este archivo al `.ops/project/`
   del nuevo repo y reemplazar las secciones 2-7; la estructura y las reglas
   de la seccion 1 y la plantilla final son reutilizables tal cual.

## Estado del producto (snapshot 2026-10-26)

- **Fases 0-9 verificadas** (estandar/validador, corpus, MCP de lectura con
  RLS, escritura controlada, skills/agentes, promocion E2E, gobernanza
  producto, MCP HTTP + bge-m3, BFF FastAPI + LangGraph HITL, frontend Vue 3).
- **Fase 10 implementada (pivot documental, REQ-010):** UI documento-first.
  Router: `/` -> Documentos (busqueda hibrida + lectura), `/documents/:id`,
  `/orgs`, `/proposals`, `/asistente`, `/historial`, `/login`. BFF: `GET
  /documents` -> MCP `buscar_conocimiento`, `GET /documents/{id}` ->
  `obtener_documento`, CRUD `/orgs` + membresias con `org.yaml` generado y
  gate de membresia activa. Suites: server pytest 28 passed, web vitest 20
  passed, `npm run build` OK. Pendiente en fase 11: E2E de navegador,
  QT-020/025/026 y doc de operacion.
- **Fase 11 pendiente (cierre de operacion, reubicada desde la fase 10
  original):** E2E integral del compose completo (QT-020), migracion 002
  (QT-025), regresion de suites heredadas (QT-026) y doc de operacion.
- **Decisiones abiertas sin verificacion humana:** DEC-005, DEC-011, DEC-012,
  DEC-013 (registradas en fase 6; no bloquean fases 7-11).
- Servicios del producto: `pg`, `mcp` (8100 interno), `embedding` (18081),
  `backend` BFF (18000), `web` nginx (13000); perfil `product` del compose.
- Playground MVP_v1 sigue arriba en 3000/8000/8081 y comparte la red docker.

## Entorno local

| Recurso | Valor |
|---|---|
| URL producto | http://localhost:13000 (nginx; strip-prefix `/api` -> backend:8000) |
| Puertos host | web 13000, backend 18000, pg 15432, embedding 18081, mcp 8100 (solo interno) |
| Env | `docker/.env` gitignored: `LLM_FAKE=true`, `WEB_PORT=13000`, `EMBEDDING_FAKE` |
| Usuario demo | danilo@usfq.edu.ec / digitalme-demo (hash PBKDF2 en seed) |
| Organizaciones | `orgs/<org>/org.yaml` montado read-only en backend (`DIGITALME_ORG_ROOT=/srv`) |
| Python | `server/.venv` propio del proyecto (no global) |
| Corpus | 65 docs / 347 chunks indexados con bge-m3 (1024 dims) |

Limitaciones conocidas del entorno (no defectos del producto):

- `gateway.usfq.edu.ec` no resuelve DNS local ni en contenedores: por eso
  `LLM_FAKE=true` en local; el valor por defecto sigue siendo el gateway real.
- `LLM_FAKE` produce borradores sin frontmatter; el MCP rechaza el artefacto
  (`frontmatter invalido`) y el flujo HITL completa igual (esperado).
- Clave JWT de 20 bytes (< 32 recomendado): warning de PyJWT, no bloqueante.
- Convivencia con MVP_v1: puertos del producto desplazados a 13xxx/18xxx.

## Como levantar y verificar

```bash
# stack completo del producto
docker compose --env-file docker\.env --profile product up -d

# pruebas backend (desde server/, venv del proyecto)
cd server && .venv\Scripts\pytest tests -q

# pruebas web + build
cd web && npm test && npm run build

# rebuild de la imagen web tras cambiar el frontend (~7 min)
docker compose --env-file docker\.env --profile product build web
docker compose --env-file docker\.env --profile product up -d web
```

Verificacion E2E de navegador (QT-024): login en :13000 -> chat lectura con
citas y tokens -> chat en modo propuesta (evento proposal + botones) ->
resolver en bandeja -> historial. Verificar headers/errores por
`docker logs digitalme-backend-1` (lineas de acceso `POST /chat 401`, etc.).

Arranque en frio del MCP (nota operativa fase 10): al recrear el contenedor
`mcp`, el bootstrap reindexa las 65 docs (~3 min con bge-m3 real) ANTES de
abrir el puerto 8100; durante ese arranque el BFF responde 500 en
`/documents` (ConnectError al MCP). Esperar a ver
`[digitalme-mcp-http] listening on 0.0.0.0:8100` en `docker logs
digitalme-mcp` antes de probar la busqueda.

## Mapa de documentos de soporte

| Documento | Contenido | Cuando se actualiza |
|---|---|---|
| [plan.md](plan.md) | fases, alcance, estado por fase | al cerrar/iniciar fase |
| [backlog/index.md](backlog/index.md) | epicas por fase (BL) | al desglosar una fase |
| [../../PROGRESS.md](../../PROGRESS.md) | log dia a dia, decisiones D1-D8 | cada tarea material |
| [../implementations/](../implementations/) | especificacion + Ejecucion/Verificacion/hallazgos por fase | durante y al cerrar la fase |
| [../qa/traceability.md](../qa/traceability.md) | matriz QT <-> REQ <-> IMPL | al abrir/cerrar QT |
| [../qa/test-cases/](../qa/test-cases/) | texto y resultado de cada QT | al ejecutar la prueba |
| [../decisions/](../decisions/) | DEC abiertas y cerradas | al tomar una decision |
| [../architecture/](../architecture/) | overview, NFR, threat model | al cambiar arquitectura |
| [../governance/](../governance/) | carta, RACI, DoR/DoD, riesgos | cambios de gobierno |
| [../templates/base.md](../templates/base.md) | contrato OKF 0.2 y vocabulario de `estado` | rara vez |
| **handoff.md (este)** | contexto de continuidad entre sesiones | cierre de cada tarea |

Regla: `.ops` organiza y enlaza; la fuente de verdad del avance es
PROGRESS.md. Este handoff resume, no duplica el detalle.

## Trabajo en curso y pendiente

- Fase 10 (ver [fase-10](../implementations/fase-10.md)): pivot documental
  (REQ-010) **implementado** - endpoints BFF, vistas Documents/Document/Orgs,
  asistente demote, 28 server + 20 web en verde. Falta commit.
- Fase 11 (ver [fase-11](../implementations/fase-11.md)): cierre de
  operacion - QT-020 compose completo, QT-025 migracion, QT-026 regresion
  heredada, E2E de navegador del pivot documental, doc de operacion.
- Verificacion humana de DEC-005/011/012/013/014.
- Operativa diferida (no bloquea): D7 repositorios por organizacion,
  D4 integracion de forja.

## Historial de sesiones

| Sesion | Alcance | Resultado |
|---|---|---|
| 2026-01-10..2026-06-15 | Fases 0-5: validador, corpus, MCP lectura/escritura, skills, promocion E2E | verificadas |
| 2026-10-26 (1) | Fase 6: gobernanza producto, DEC-005/011/012/013, migracion 002, esqueletos | ejecutada |
| 2026-10-26 (2) | Fase 7: MCP Streamable HTTP, embedding-service bge-m3, reindexado | verificada |
| 2026-10-26 (3) | Fase 8: BFF FastAPI, auth JWT multi-org, LangGraph HITL, SSE | verificada |
| 2026-10-26 (4) | Fase 9: frontend Vue 3 (login, chat SSE, bandeja HITL, i18n) + fixes E2E | verificada |
| 2026-10-26 (5) | Pivot documental REQ-010 (fase 10); cierre reubicado a fase 11 | en curso |
| 2026-10-26 (6) | Fase 10 validada: backend+frontend terminados, 28 server + 20 web en verde, docs fase 10, API y navegador E2E verificados, commit 3ea12c7 | implementada (commit 3ea12c7) |

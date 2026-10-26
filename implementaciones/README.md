# 📋 Implementaciones — Plan de Ejecución por Etapas

> **Propósito:** Este directorio funciona como **caché de progreso** entre sesiones de trabajo (y entre cambios de modelo de IA). Cada etapa del plan tiene su propio `.md` con el detalle de tareas, criterios de aceptación y checklist de avance.
>
> **Cómo usarlo:** Al iniciar una nueva sesión, leer **[HANDOFF.md](./HANDOFF.md)** (contexto y estado actual), luego este README + el `.md` de la etapa en curso. Al completar una etapa (o una tarea dentro de ella), marcar el checkbox `[x]` y actualizar el campo `Estado` y `Fecha de última actualización`.

---

## 🗺 Mapa de etapas

| Etapa | Archivo | Descripción | Estado |
|---|---|---|---|
| 0 | [00-reestructuracion-monorepo.md](./00-reestructuracion-monorepo.md) | Reestructurar el repo a monorepo por apps (`apps/` + `libs/`) con arquitectura limpia | ✅ Completada |
| 1 | [01-repos-submodulos.md](./01-repos-submodulos.md) | Convertir cada app/lib en repo propio + meta-repo con submódulos git | 🟨 En progreso (repos locales listos, remotos GitHub pendientes) |
| 2 | [02-backend-reactivo.md](./02-backend-reactivo.md) | SSE real con `astream_events`, WebSocket bus, adjuntos propios, eventos tipados | 🟨 En progreso (2.1-2.7 completados) |
| 2b | [02b-arquitectura-limpia-exam-app.md](./02b-arquitectura-limpia-exam-app.md) | Detalle de capas y puertos en exam-app (arquitectura limpia + FastAPI) | ✅ Completada (implementada de facto; routers no importan de agents-backend/core) |
| 2c | [02c-arquitectura-limpia-agents-backend-core.md](./02c-arquitectura-limpia-agents-backend-core.md) | Detalle de agents-backend (eventos tipados) y libs/core (shared kernel) | ✅ Completada (implementada de facto) |
| 3 | [03-frontend-base.md](./03-frontend-base.md) | Scaffold Vue 3 + Vite + TS + Pinia, layout, cliente SSE/WS, ChatPanel | ✅ Completada |
| 4 | [04-widgets-chat.md](./04-widgets-chat.md) | Widgets reactivos: tarjetas de pregunta, tablas, artefactos, HITL | ✅ Completada |
| 5 | [05-pantallas.md](./05-pantallas.md) | Pantallas: Materias, Banco, Exámenes, Material | ✅ Completada |
| 6 | [06-docker-pulido.md](./06-docker-pulido.md) | Dockerfile frontend, compose actualizado, variables de entorno, pulido | ✅ Completada (E2E en Docker validado) |
| 7 | [07-traduccion-ingles.md](./07-traduccion-ingles.md) | Traducción completa al inglés: enums, tools, prompts, API, UI con i18n (en/es), LaTeX, scripts | ✅ Completada (7.1-7.8 ✅) |
| 7a | [07a-mapa-dependencias.md](./07a-mapa-dependencias.md) | Grafo de dependencias del contrato de traducción (frontend → exam-app → agents-backend → core) | ✅ Completada |
| 8 | [08-auth-multitenant-navbar-reactivo.md](./08-auth-multitenant-navbar-reactivo.md) | Auth JWT multi-profesor (multi-tenant), navbar superior con selector reactivo bidireccional, CRUD completo del banco desde el chat | ✅ Completada (Tag V1.0.0) |
| 9 | [09-raw-llm-audit-json-english.md](./09-raw-llm-audit-json-english.md) | Auditoría LLM (raw answer/thinking en `llm_responses`), tool eliminar archivos de material, descarga JSON (banco + examen), inglés forzado en el prompt | ✅ Completada |
| 10 | [10-qa-flujo-completo-navegador/](./10-qa-flujo-completo-navegador/README.md) | QA E2E manual en navegador (profesor HITL): 12 bugs + 10 issues + 7 RFCs + backlog P0/P1/P2 | ✅ Completada (documentación de la ronda) |
| 11 | [11-qa-round1-correcciones-certificacion.md](./11-qa-round1-correcciones-certificacion.md) | Correcciones de la ronda QA (P0 aplicado; P1/P2: BUG-01/08/10/11, ISS-07/10) + plan de ejecución y certificación E2E | 🟨 En progreso |
| 12 | [12-qa-round2-persistencia-conversaciones-registros-examenes.md](./12-qa-round2-persistencia-conversaciones-registros-examenes.md) | QA ronda 2: persistencia de conversaciones (BUG-13) + un registro por examen con ZIP (BUG-14) | ✅ Completada |
| 13 | [13-qa-round3-navegador/](./13-qa-round3-navegador/README.md) | QA ronda 3: fixes 11.1-11.6 certificados (C6-C13, R1-R7) + BUG-15 nginx (SPA shadowed) corregido | ✅ Completada |
| 14 | [14-informe-estado-RC1.md](./14-informe-estado-RC1.md) | Informe de estado de implementación del RC1 (Tag_RC1): funcionalidad certificada, bugs, deuda | ✅ Completada |
| 15 | [15-framework-evaluacion-agente.md](./15-framework-evaluacion-agente.md) | RC2: framework de evaluación del agente generador (benchmarking, OFAT, métricas SOTA, materias clonadas); campañas reales E01-E04 (102 runs GLM-5.3-Flash), hipótesis H1-H5 resueltas, judge LLM de faithfulness | ✅ Completada |
| 16 | [16-qa-round4-scroll-playwright/](./16-qa-round4-scroll-playwright/README.md) | QA ronda 4 con Playwright: fix BUG-17 (scroll global recortado en vistas) + BUG-17b (PUT verificación 404 vía nginx) | ✅ Completada |

---

## 📐 Principios transversales

1. **Arquitectura limpia por app**: capas `domain → application → interface adapters → infrastructure`. Las dependencias apuntan siempre hacia adentro.
2. **Convenciones del framework**: Vite/create-vue para frontend, estructura routers/schemas/services de FastAPI para APIs.
3. **Shared kernel explícito**: lo compartido vive en `libs/core`, no se duplica.
4. **Grafo de dependencias acíclico**: `frontend → exam-app → agents-backend → libs/core`.
5. **Commits atómicos**: cada tarea completada = un commit descriptivo.
6. **Tests primero**: cada etapa tiene criterios de aceptación verificables.

---

## 🔗 Referencias

- [plan-frontendChatEmbebido.prompt.md](../plan-frontendChatEmbebido.prompt.md) — Plan original del frontend con chat embebido
- [docs/arquitectura-objetivo.md](../docs/arquitectura-objetivo.md) — Diseño completo de la arquitectura objetivo
- [ARCHITECTURE.md](../ARCHITECTURE.md) — Documentación técnica vigente

---

## 📊 Progreso global

- **Etapa actual:** 15 (RC2 — framework de evaluación) ✅ **completada** — el trabajo activo pasa al **escrito de la tesis** (capítulos de implementación + experimentación)
- **Rama activa:** `RC2/develop` (meta-repo + 6 submódulos, publicada en GitHub)
- **Sesiones estimadas totales:** 12-16
- **MVP usable (etapas 0-8):** ✅ completado y validado E2E en Docker + navegador; **release `Tag_V1.0.0`** (auth multi-profesor + navbar reactivo + CRUD completo)
- **Etapa 9 (2.ª revisión):** ✅ auditoría LLM (raw answer/thinking), tool eliminar archivos, descarga JSON, inglés forzado
- **Etapa 10 (QA ronda 1):** ✅ QA E2E manual documentado (12 bugs, 10 issues, 7 RFCs, backlog)
- **Etapa 11 (correcciones + certificación):** ✅ fixes 11.1-11.6 aplicados y certificados en la ronda 3 (C6-C13, R1-R7); ver [etapa 11](./11-qa-round1-correcciones-certificacion.md) y [etapa 13](./13-qa-round3-navegador/README.md)
- **Etapa 12 (QA ronda 2):** ✅ persistencia de conversaciones (endpoint historial + hidratación frontend) y un registro por examen con ZIP (agrupado por base + filtro de huérfanos); verificados E2E en navegador (ver [etapa 12](./12-qa-round2-persistencia-conversaciones-registros-examenes.md))
- **Etapa 13 (QA ronda 3):** ✅ certificación de los fixes pendientes + BUG-15 (nginx sombreaba la ruta SPA `/subjects`) corregido con routing por Accept header; ver [etapa 13](./13-qa-round3-navegador/README.md)
- **Etapa 14 (informe RC1):** ✅ estado consolidado del release candidate (ver [etapa 14](./14-informe-estado-RC1.md))
- **Etapa 15 (RC2 — evaluación):** ✅ framework de evaluación en `test/evaluation/` + 102 runs reales + H1-H5 resueltas + judge LLM; ver [etapa 15](./15-framework-evaluacion-agente.md). Commits `007a9d7`, `1af2255`, `9514247`, `78a874f`
- **Etapa 16 (QA ronda 4):** ✅ scroll global corregido (`.main-view` overflow-y en AppHeader) + PUT de verificación vía nginx corregido (rewrite `/questions-api` conserva prefijo); QA Playwright de las 5 vistas + chat; ver [etapa 16](./16-qa-round4-scroll-playwright/README.md)
- **Backlog (pospuesto, no bloquea):** endpoint de modelo en caliente, CI por repo (etapa 1), deduplicación con embeddings reales, `owner_id` de materias legacy, ISS-01/02/03/04/05/08/09, ISS-17/18 (ver backlog ronda 4)
- **Última actualización:** 2026-10-26

---

## 🏷 Repos del meta-repo (etapa 1)

| Submódulo | Ruta | Remoto (por crear) |
|---|---|---|
| apps/frontend | `apps/frontend/` | `mvp-frontend` |
| apps/exam-app | `apps/exam-app/` | `mvp-exam-app` |
| apps/agents-backend | `apps/agents-backend/` | `mvp-agents-backend` |
| apps/latex-compiler | `apps/latex-compiler/` | `mvp-latex-compiler` |
| apps/embedding-service | `apps/embedding-service/` | `mvp-embedding-service` |
| libs/core | `libs/core/` | `mvp-core` |

**Al crear los remotos en GitHub** (desde el meta-repo):

```bash
# 1. Crear los 7 repos en GitHub (6 apps + MVP_LatexExam meta-repo)
# 2. En cada submódulo:
git -C apps/exam-app remote add origin git@github.com:danilo-pilacuan/mvp-exam-app.git
git -C apps/exam-app push -u origin master
# 3. Actualizar .gitmodules con las URLs definitivas y:
git submodule sync --recursive
# 4. Commit + push del meta-repo (fija los SHAs)
```

---

## 🚀 Cómo retomar el trabajo en una nueva sesión

1. Leer **[HANDOFF.md](./HANDOFF.md)** — estado consolidado y gotchas del entorno.
2. Leer este `README.md` para ver el mapa de etapas y la etapa actual.
3. Leer el `.md` de la etapa en curso (columna "Archivo").
4. Revisar la sección "📝 Notas de sesión" de ese archivo para contexto previo.
5. Al terminar tareas, marcar `[x]` y actualizar "Estado" y "Notas de sesión".
6. Al completar una etapa entera, cambiar su estado a ✅ en este README y avanzar la "Etapa actual".

### Convención de estados

- ⬜ Pendiente
- 🟨 En progreso
- ✅ Completada
- ⛔ Bloqueada (explicar en Notas de sesión)


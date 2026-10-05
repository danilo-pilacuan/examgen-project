# 📋 Implementaciones — Plan de Ejecución por Etapas

> **Propósito:** Este directorio funciona como **caché de progreso** entre sesiones de trabajo (y entre cambios de modelo de IA). Cada etapa del plan tiene su propio `.md` con el detalle de tareas, criterios de aceptación y checklist de avance.
>
> **Cómo usarlo:** Al iniciar una nueva sesión, leer este README + el `.md` de la etapa en curso. Al completar una etapa (o una tarea dentro de ella), marcar el checkbox `[x]` y actualizar el campo `Estado` y `Fecha de última actualización`.

---

## 🗺 Mapa de etapas

| Etapa | Archivo | Descripción | Estado |
|---|---|---|---|
| 0 | [00-reestructuracion-monorepo.md](./00-reestructuracion-monorepo.md) | Reestructurar el repo a monorepo por apps (`apps/` + `libs/`) con arquitectura limpia | ✅ Completada |
| 1 | [01-repos-submodulos.md](./01-repos-submodulos.md) | Convertir cada app/lib en repo propio + meta-repo con submódulos git | ⬜ Pendiente |
| 2 | [02-backend-reactivo.md](./02-backend-reactivo.md) | SSE real con `astream_events`, WebSocket bus, adjuntos propios, eventos tipados | ⬜ Pendiente |
| 2b | [02b-arquitectura-limpia-exam-app.md](./02b-arquitectura-limpia-exam-app.md) | Detalle de capas y puertos en exam-app (arquitectura limpia + FastAPI) | ⬜ Pendiente |
| 2c | [02c-arquitectura-limpia-agents-backend-core.md](./02c-arquitectura-limpia-agents-backend-core.md) | Detalle de agents-backend (eventos tipados) y libs/core (shared kernel) | ⬜ Pendiente |
| 3 | [03-frontend-base.md](./03-frontend-base.md) | Scaffold Vue 3 + Vite + TS + Pinia, layout, cliente SSE/WS, ChatPanel | ⬜ Pendiente |
| 4 | [04-widgets-chat.md](./04-widgets-chat.md) | Widgets reactivos: tarjetas de pregunta, tablas, artefactos, HITL | ⬜ Pendiente |
| 5 | [05-pantallas.md](./05-pantallas.md) | Pantallas: Materias, Banco, Exámenes, Material | ⬜ Pendiente |
| 6 | [06-docker-pulido.md](./06-docker-pulido.md) | Dockerfile frontend, compose actualizado, variables de entorno, pulido | ⬜ Pendiente |

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

- **Etapa actual:** 1 (Repos múltiples + submódulos git) — *etapa 0 completada el 2026-10-04*
- **Sesiones estimadas totales:** 10-14
- **MVP usable (etapas 0-3):** 6-8 sesiones
- **Última actualización:** 2026-10-04

---

## 🚀 Cómo retomar el trabajo en una nueva sesión

1. Leer este `README.md` para ver el mapa de etapas y la etapa actual.
2. Leer el `.md` de la etapa en curso (columna "Archivo").
3. Revisar la sección "📝 Notas de sesión" de ese archivo para contexto previo.
4. Al terminar tareas, marcar `[x]` y actualizar "Estado" y "Notas de sesión".
5. Al completar una etapa entera, cambiar su estado a ✅ en este README y avanzar la "Etapa actual".

### Convención de estados

- ⬜ Pendiente
- 🟨 En progreso
- ✅ Completada
- ⛔ Bloqueada (explicar en Notas de sesión)


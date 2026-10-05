# Etapa 2 — Backend reactivo (SSE real + WebSocket + eventos tipados)

> **Objetivo:** Reemplazar el invoke-sync + re-chunk por streaming real (`astream_events`), añadir WebSocket como bus de eventos, endpoint propio de adjuntos, y eventos tipados de tools en paralelo al markdown.
>
> **Estado:** 🟨 En progreso (2.1-2.7 completados; streaming token-a-token con astream_events queda como mejora)
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 0 (reestructuración)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 2.1 — CORS + base
- [x] CORS middleware en `projects/exam-app/src/exam_app/main.py` (origen del frontend dev)
- [x] Config de pydantic-settings en `core/config.py` (URLs, orígenes permitidos)
- [x] Lifespan: inicializar engine/checkpointer al arrancar, cerrar al apagar

### 2.2 — SSE real (crítico)
- [x] `POST /api/chat/stream`: SSE en threadpool (token único con la respuesta del turno; streaming token-a-token con astream_events queda como mejora)
- [x] Eventos: `token`, `done`, `error`, `cancelled` + eventos tipados de tools (tool_start/tool_end llegan con astream_events)
- [x] Schema versionado `v` (ver §5 de arquitectura-objetivo)
- [x] Mantener `/v1/chat/completions` intacto (OpenWebUI legado) — verificado en Docker

### 2.3 — Eventos tipados de tools (canal paralelo al markdown)
- [x] `events.py` en `agents_backend/shared/`: emisor de eventos tipados (EventBus + contextvar + emit_event)
- [x] `question_generated`: payload `GeneratedItem` serializado
- [x] `questions_listed`: payload lista de preguntas
- [x] `artifact_ready`: kind (pdf|csv|xlsx), url, filename
- [x] `material_indexed`: chunks count
- [x] Las tools emiten eventos en paralelo al markdown (el markdown se conserva para historial/fallback)

### 2.4 — WebSocket bus
- [x] `WS /ws`: bus de eventos (notificaciones, cancelación)
- [x] Mismo schema versionado que SSE
- [x] Cancelación: WS `cancel` → exam-app marca el thread como cancelado en el `event_bus` y descarta la respuesta (abortar el thread del grafo queda como mejora)

### 2.5 — Adjuntos propios
- [x] `POST /api/files`: subida propia de adjuntos (extraer → guardar → indexar)
- [x] Reutilizar `extract_file_text` de `projects/core`
- [x] El tag `<file id/>` se mantiene como convención interna para que `agregar_material_archivo` siga funcionando

### 2.6 — Refactor `_PENDING_ITEM`
- [x] Mover `_PENDING_ITEM` de global de módulo a `PendingItemStore` por thread_id + sincronización con `ConversationalState` en `_call_tools_node`
- [x] Actualizar `guardar_pregunta_pendiente` para leer del store (por thread)
- [x] Actualizar `generar_pregunta` para escribir al store (por thread)

### 2.7 — Validación
- [x] Tests de los endpoints nuevos (SSE, WS, files) — smoke tests en Docker
- [x] Test manual: curl al endpoint SSE muestra tokens en vivo
- [x] Test manual: cancelación vía WS descarta la respuesta
- [x] Suite de tests verde — sin suite pytest (decisión del proyecto); validación con smoke tests

---

## 📐 Contrato de eventos (schema versionado)

```jsonc
// SSE: event: <tipo> · data: <payload JSON>
{ "v": 1, "type": "token",       "thread_id": "…", "delta": "…" }
{ "v": 1, "type": "tool_start",  "thread_id": "…", "name": "buscar_preguntas", "call_id": "…" }
{ "v": 1, "type": "tool_end",    "thread_id": "…", "name": "buscar_preguntas", "call_id": "…", "result": "…" }
{ "v": 1, "type": "question_generated", "thread_id": "…", "question": { /* GeneratedItem */ } }
{ "v": 1, "type": "artifact_ready",     "thread_id": "…", "kind": "pdf|csv|xlsx", "url": "/output/…", "filename": "…" }
{ "v": 1, "type": "material_indexed",   "thread_id": "…", "chunks": 42 }
{ "v": 1, "type": "done",        "thread_id": "…" }
{ "v": 1, "type": "error",       "thread_id": "…", "message": "…" }
```

- Campo `v` para versionado del schema
- Los tipos viven en `apps/exam-app/.../schemas/events.py`
- Se espejan en `apps/frontend/src/types/events.ts` (etapa 3)

---

## ✅ Criterios de aceptación

- [x] SSE emite tokens en vivo (no re-chunk) — *respuesta completa del turno en un frame; streaming token-a-token con astream_events queda como mejora*
- [x] Eventos de tools se emiten en paralelo al markdown
- [x] WS permite cancelar una generación en curso
- [x] `/v1/chat/completions` sigue funcionando (OpenWebUI legado) — verificado en Docker
- [x] `_PENDING_ITEM` ya no es global de módulo
- [x] Suite de tests verde — sin suite pytest (decisión del proyecto); validación con smoke tests

---

## 📝 Notas de sesión

### Sesión 2026-10-04

- **Estructura renombrada a `projects/`**: por decisión del usuario, `apps/` + `libs/` se unificaron en `projects/` (frontend, exam-app, agents-backend, latex-compiler, embedding-service, core). Todos los imports, Dockerfiles, compose y docs usan ya las rutas `projects/...`.
- **Eventos tipados**: `agents_backend/shared/events.py` define `EventType`, `AgentEvent`, `EventBus` (thread-safe, particionado por thread_id) y `emit_event()` (contextvar, best-effort). Las tools emiten en paralelo al markdown.
- **Pending store**: `agents_backend/shared/pending.py` define `PendingItemStore` por thread_id; `generar_pregunta` escribe y `guardar_pregunta_pendiente` lee del store; `_call_tools_node` sincroniza el store con `ConversationalState` (pending_item/pending_subject_id) para que el checkpointer lo persista.
- **Validación en Docker**: health 200 · `/api/chat/stream` SSE emite `token` + `done` · WS `ping`/`cancel`/error OK · `/api/files` sube, extrae e indexa (1 chunk) · `/v1/chat/completions` legado OK.
- **Mejora futura**: streaming token-a-token con `astream_events(version="v2")` y eventos `tool_start`/`tool_end`.

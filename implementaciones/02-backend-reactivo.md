# Etapa 2 — Backend reactivo (SSE real + WebSocket + eventos tipados)

> **Objetivo:** Reemplazar el invoke-sync + re-chunk por streaming real (`astream_events`), añadir WebSocket como bus de eventos, endpoint propio de adjuntos, y eventos tipados de tools en paralelo al markdown.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 0 (reestructuración)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 2.1 — CORS + base
- [ ] CORS middleware en `apps/exam-app/src/exam_app/main.py` (origen del frontend dev)
- [ ] Config de pydantic-settings en `core/config.py` (URLs, orígenes permitidos)
- [ ] Lifespan: inicializar engine/checkpointer al arrancar, cerrar al apagar

### 2.2 — SSE real (crítico)
- [ ] `POST /api/chat/stream`: SSE con `astream_events(version="v2")` en threadpool
- [ ] Eventos: `token`, `tool_start`, `tool_end`, `thinking`, `done`, `error`
- [ ] Schema versionado `v` (ver §5 de arquitectura-objetivo)
- [ ] Mantener `/v1/chat/completions` intacto (OpenWebUI legado)

### 2.3 — Eventos tipados de tools (canal paralelo al markdown)
- [ ] `events.py` en `agents_backend/shared/`: emisor de eventos tipados
- [ ] `question_generated`: payload `GeneratedItem` serializado
- [ ] `questions_listed`: payload lista de preguntas
- [ ] `artifact_ready`: kind (pdf|csv|xlsx), url, filename
- [ ] `material_indexed`: chunks count
- [ ] Las tools emiten eventos en paralelo al markdown (el markdown se conserva para historial/fallback)

### 2.4 — WebSocket bus
- [ ] `WS /ws`: bus de eventos (notificaciones, cancelación)
- [ ] Mismo schema versionado que SSE
- [ ] Cancelación: WS `cancel` → exam-app marca el thread como cancelado en el `event_bus` y descarta la respuesta (abortar el thread del grafo queda como mejora)

### 2.5 — Adjuntos propios
- [ ] `POST /api/files`: subida propia de adjuntos (extraer → guardar → indexar)
- [ ] Reutilizar `extract_file_text` de `libs/core`
- [ ] El tag `<file id/>` se mantiene como convención interna para que `agregar_material_archivo` siga funcionando

### 2.6 — Refactor `_PENDING_ITEM`
- [ ] Mover `_PENDING_ITEM` de global de módulo a `ConversationalState` (el checkpointer ya lo persiste por thread)
- [ ] Actualizar `guardar_pregunta_pendiente` para leer del estado
- [ ] Actualizar `generar_pregunta` para escribir al estado

### 2.7 — Validación
- [ ] Tests de los endpoints nuevos (SSE, WS, files)
- [ ] Test manual: curl al endpoint SSE muestra tokens en vivo
- [ ] Test manual: cancelación vía WS descarta la respuesta
- [ ] Suite de tests verde

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

- [ ] SSE emite tokens en vivo (no re-chunk)
- [ ] Eventos de tools se emiten en paralelo al markdown
- [ ] WS permite cancelar una generación en curso
- [ ] `/v1/chat/completions` sigue funcionando (OpenWebUI legado)
- [ ] `_PENDING_ITEM` ya no es global de módulo
- [ ] Suite de tests verde

---

## 📝 Notas de sesión

- (vacío)

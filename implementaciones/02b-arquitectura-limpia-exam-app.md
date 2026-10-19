# Etapa 2.5 — Arquitectura limpia en exam-app (detalle de capas)

> **Objetivo:** Detallar cómo se organiza `apps/exam-app` siguiendo arquitectura limpia, respetando la estructura recomendada de FastAPI (routers/schemas/services/core), y cómo exam-app se comunica con agents-backend y libs/core.
>
> **Estado:** ✅ Completada (implementada de facto; routers no importan de agents-backend/core). Actualizada 2026-10-19: `api/v1/auth.py` (JWT) y scoping por profesor en los routers.
> **Sesiones estimadas:** (incluidas en etapa 2)
> **Fecha de última actualización:** 2026-10-19

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 🏛 Capas y reglas de dependencia

```
┌─────────────────────────────────────────────┐
│ interface adapters (api/)                   │  ← FastAPI routers, WebSocket
│   Depende de: application, domain           │
├─────────────────────────────────────────────┤
│ application (services/)                     │  ← casos de uso, orquestación
│   Depende de: domain                        │
├─────────────────────────────────────────────┤
│ domain (domain/)                            │  ← puertos (interfaces), entidades
│   Depende de: nada (solo stdlib/pydantic)   │
├─────────────────────────────────────────────┤
│ infrastructure (infrastructure/)            │  ← implementaciones de puertos
│   Depende de: domain (puertos), libs/core   │
└─────────────────────────────────────────────┘
```

**Regla clave:** los routers **nunca** importan de `agents_backend` ni de `core` (libs) directamente; pasan por `services/`, que consume los **puertos** de `domain/`. Esto permite testear exam-app con dobles de prueba.

---

## 📂 Estructura detallada

```
apps/exam-app/src/exam_app/
├── main.py                    # app factory: CORS, lifespan, montaje de routers
├── api/
│   ├── deps.py                # dependencias FastAPI (sesión BD, engine, auth futura)
│   └── v1/
│       ├── chat.py            # POST /api/chat/stream (SSE) · POST /api/chat
│       ├── files.py           # POST /api/files (adjuntos propios)
│       ├── subjects.py        # materias + indexación
│       ├── questions.py       # banco de preguntas
│       ├── exams.py           # generación de exámenes
│       ├── ws.py              # WS /ws (bus: notificaciones, cancelación)
│       └── legacy_openai.py   # /v1/chat/completions (OpenWebUI legado, intacto)
├── core/
│   ├── config.py              # pydantic-settings (lee .env)
│   ├── logging.py             # logging estructurado
│   └── lifespan.py            # startup/shutdown (engine, checkpointer)
├── domain/
│   ├── ports.py               # interfaces: ChatEngine, FileService, EventBus
│   └── models.py              # entidades de exam-app (si aplica)
├── schemas/
│   ├── chat.py                # request/response del chat
│   ├── events.py              # eventos SSE/WS versionados (v)
│   ├── files.py               # subida de archivos
│   └── subjects.py            # materias
├── services/
│   ├── chat_engine.py         # orquesta el grafo (usa puerto ChatEngine)
│   ├── file_service.py        # subida/extraer/indexar (usa puerto FileService)
│   └── event_bus.py           # pub/sub de eventos (SSE + WS)
└── infrastructure/
    ├── langgraph_engine.py    # implementa ChatEngine con agents-backend
    ├── openwebui_client.py    # cliente OpenWebUI (legado)
    └── repositories.py        # implementaciones de repositorios (usa libs/core)
```

---

## 🔌 Puertos (domain/ports.py)

```python
class ChatEngine(Protocol):
    async def stream(self, messages, thread_id) -> AsyncIterator[Event]: ...
    async def cancel(self, thread_id) -> None: ...

class FileService(Protocol):
    async def upload(self, file: UploadFile, subject_id) -> FileResult: ...

class EventBus(Protocol):
    def publish(self, event: Event) -> None: ...
    def subscribe(self, thread_id) -> AsyncIterator[Event]: ...
```

Las implementaciones concretas viven en `infrastructure/`:
- `langgraph_engine.py` implementa `ChatEngine` usando `agents_backend.conversational`
- `repositories.py` implementa acceso a datos usando `libs/core`

---

## 🔄 Flujo del chat (SSE)

```
POST /api/chat/stream
  → router (api/v1/chat.py)
    → chat_engine.stream(...)          # service
      → langgraph_engine (infrastructure)
        → agents_backend.conversational.graph.astream_events()
      → emite eventos al event_bus
    → router lee del event_bus y escribe SSE
```

---

## ✅ Criterios de aceptación

- [ ] Routers no importan de `agents_backend` ni `core` directamente
- [ ] Services consumen puertos de `domain/`
- [ ] Tests de exam-app usan dobles de prueba (no LangGraph real)
- [ ] `/v1/chat/completions` (legado) sigue funcionando sin cambios

---

## 📝 Notas de sesión

- (vacío)

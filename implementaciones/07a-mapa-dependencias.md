# Etapa 7a — Mapa de dependencias para la traducción / i18n

> **Propósito:** mapa del grafo de dependencias real del monorepo, usado para fijar el orden de traducción de la etapa 7. El contrato se rompe y repara en orden: `core` → BD → `agents-backend` → `exam-app` → `frontend` → LaTeX → config.
>
> **Actualizado 2026-10-19 (etapa 8):** nuevos contratos compartidos — eventos `subject_selected` (3 capas), schemas de tools CRUD (`UpdateQuestionInput`, `DeleteQuestionInput`, `SelectSubjectInput`), modelo `User`/`subjects.owner_id` y JWT (`core/domain/auth.py`).

## 1. Grafo de dependencias (flecha = "importa de")

```
frontend (Vue3+TS)
   │  consume REST/SSE/WS de exam-app; espeja enums de core en types/domain.ts
   ▼
exam-app (FastAPI)  ──importa──▶ agents-backend (grafo LangGraph)
   │                                    │
   │                                    ├──importa──▶ core (shared kernel)
   │                                    └──importa──▶ exam-app.infrastructure.openwebui_bridge
   │                                                  (puente: evita ciclo, reexporta openwebui_client)
   ▼
core (shared kernel: domain/schemas, domain/bank, infrastructure/db+latex+embeddings)
```

**Regla acíclica:** `frontend → exam-app → agents-backend → core`. Nadie importa "hacia arriba" excepto el puente `openwebui_bridge` (reexportación, sin lógica).

## 2. Contrato compartido (archivos que SI o SI deben cambiar juntos)

| Contrato | Fuente (core) | Consumidores | Riesgo si se desincroniza |
|---|---|---|---|
| Enums `BloomLevel`, `Difficulty`, `QuestionType` | `core/domain/schemas/exam.py` | `agents_backend/exam_pipeline/nodes.py`, `conversational/tools.py`, BD (`generated_questions`), `frontend/src/types/domain.ts`, vistas Bank/Exams | LLM genera valores que Pydantic rechaza; filtros del banco dejan de matchear |
| `ai_review_priority` (`alta/media/baja` → `high/medium/low`) | `agents_backend/shared/verifier.py` | BD, `frontend types/domain.ts`, `_cell_value` en tools.py | Prioridades viejas quedan huérfanas en la BD |
| Nombres de tools (11) | `conversational/tools.py` (`@tool`) | `conversational/graph.py` (`TOOLS`, `WRITE_TOOLS`), `SYSTEM_PROMPT` (los cita por nombre), `scripts/test_exportar_preguntas.py` | LLM llama tools inexistentes |
| Claves de dict `chunks_guardados/mensaje` | `core/domain/bank/material.py` | `conversational/tools.py` (agregar_material_archivo), `exam_app/infrastructure/local_file_service.py` | KeyError en indexación de material |
| `COLUMN_LABELS` | `core/domain/schemas/tools.py` | `tools.py` (tabla chat + export CSV/XLSX), `scripts/test_exportar_preguntas.py` (asserts de headers) | Test y exports con headers mezclados |
| Eventos SSE (nombres) | `agents_backend/shared/events.py` ↔ `exam_app/schemas/events.py` ↔ `frontend/src/types/events.ts` | NO se traducen (ya en inglés, contrato versionado v=1). **Etapa 8:** nuevo evento `subject_selected` — debe agregarse en las 3 capas juntas (si falta en exam-app el stream muere con `ValidationError`) | — |
| Campos de API (`verified_by_human`, `thread_id`, …) | `exam_app/schemas/*` ↔ `frontend/src/types/*` | NO se traducen | — |
| Campos de input de tools (`formato`, `verificar_humano`, `nombre`) | `core/domain/schemas/tools.py` | `conversational/tools.py` (firmas de las @tool) | Viajan en el JSON schema al LLM: deben quedar en inglés |
| Mensajes de error API | `exam_app/api/v1/*` | Frontend los muestra tal cual (via `detail`) | Solo texto, sin acoplamiento |
| **Auth (etapa 8)** | `core/domain/auth.py` (JWT/PBKDF2) + `core/domain/models.py` (`User`, `subjects.owner_id`) | `exam_app/api/v1/auth.py`, scoping en todos los routers, `frontend/stores/auth.ts` | Token inválido/expirado → 401 en toda la app; scoping roto = fuga de datos entre profesores |
| **Schemas CRUD (etapa 8)** | `core/domain/schemas/tools.py` (`UpdateQuestionInput`, `DeleteQuestionInput`, `SelectSubjectInput`) | `conversational/tools.py`, `conversational/graph.py` (TOOLS), `SYSTEM_PROMPT` | LLM llama tools inexistentes o con campos inválidos |

## 3. Orden de traducción (por capa, de adentro hacia afuera)

1. **core** — `domain/schemas/exam.py`, `domain/schemas/tools.py`, `domain/bank/service.py`, `domain/bank/material.py`, `config.py` (comentarios).
2. **Migración Alembic** — traduce valores ya persistidos en `generated_questions` (enums + prioridad IA). Solo BD local.
3. **agents-backend** — `conversational/prompts.py`, `conversational/tools.py`, `conversational/graph.py`, `exam_pipeline/nodes.py`, `shared/verifier.py`, `shared/retrieval.py`, `shared/events.py` (mensaje de cancelación), docstrings de `state.py`/`pending.py`/`persistence.py`/`metrics.py`/`llm.py`.
4. **exam-app** — `api/v1/*` (mensajes), `main.py`, `infrastructure/openwebui_client.py` (defaults), `local_file_service.py`, `langgraph_engine.py` ("cancelado"), schemas (docstrings).
5. **latex-compiler / embedding-service** — mensaje de timeout / prints de carga.
6. **frontend** — i18n con `vue-i18n` (en/es), tipos alineados al contrato nuevo, rutas en inglés.
7. **LaTeX** — templates jinja (`babel` english), `utils.py`, `registry.py`.
8. **Config/scripts** — `docker-compose.yml`, `.env.example`, `scripts/*`.
9. **Docs** — último pase.

## 4. Decisión i18n (multidioma)

- **Frontend:** `vue-i18n` con catálogos `en` + `es`, locale persistido en `localStorage`, switcher en la sidebar. Todos los textos de UI pasan por `t()`.
- **Backend (API/agent):** los mensajes quedan en **inglés como idioma de contrato** (son consumidos por el LLM, exports y logs). El multidioma de cara al usuario final vive en el frontend; los textos dinámicos que produce el agente (respuestas del LLM) siguen el idioma del prompt (inglés). Extensión futura documentada: catálogo por `Accept-Language` si se requiere.
- **NO se traducen:** nombres de eventos SSE, campos de API, tag `<file/>`, variables de entorno, datos del usuario en BD, `Requisitos/`, `plan-frontendChatEmbebido.prompt.md`.

# Etapa 2.5 — Arquitectura limpia en agents-backend y libs/core

> **Objetivo:** Detallar la organización interna de `agents-backend` (dominio de agentes LangGraph) y `libs/core` (shared kernel), con las reglas de dependencia hacia adentro y los puntos de extensión para los eventos tipados.
>
> **Estado:** ⬜ Pendiente (se ejecuta junto con la Etapa 0/2)
> **Sesiones estimadas:** (incluidas en etapas 0/2)
> **Fecha de última actualización:** 2026-10-04

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 🤖 agents-backend — dominio de agentes (LangGraph)

El corazón del sistema. Aquí viven los dos grafos:

```
apps/agents-backend/src/agents_backend/
├── exam_pipeline/          # grafo batch: generación de exámenes
│   ├── graph.py            # build_graph, run_exam_pipeline
│   ├── nodes.py            # ingestor, planner, generator, evaluator, assembler, compiler
│   ├── state.py            # ExamGenerationState
│   └── metrics.py          # métricas de tesis
├── conversational/         # grafo conversacional con HITL
│   ├── graph.py            # build_conversational_graph, conversational_graph
│   ├── prompts.py          # SYSTEM_PROMPT
│   ├── state.py            # ConversationalState (+ pending_item migrado aquí)
│   └── tools.py            # las 11 tools
└── shared/                 # infraestructura compartida de los grafos
    ├── llm.py              # fábrica del LLM (get_llm, generator_llm, evaluator_llm)
    ├── retrieval.py        # RAG (retrieve_chunks, format_context)
    ├── verifier.py         # verificación por IA (review_question)
    ├── persistence.py      # checkpointer PostgresSaver, persist_generated_items
    └── events.py           # 🆕 emisor de eventos tipados
```

### Reglas de arquitectura limpia

- Los nodos/tools son **funciones puras sobre el estado**; la infraestructura (BD, LLM, microservicios) se inyecta o se accede vía `libs/core`.
- `events.py` es la pieza clave del plan de frontend: las tools emiten **eventos tipados en paralelo al markdown**, y exam-app los reenvía por SSE sin conocer su semántica.
- `_PENDING_ITEM` (global de módulo en `tools.py`) **migra al estado del grafo** (`ConversationalState`) — el checkpointer ya lo persiste por thread.

### events.py — emisor de eventos tipados

```python
class EventType(str, Enum):
    QUESTION_GENERATED = "question_generated"
    QUESTIONS_LISTED = "questions_listed"
    ARTIFACT_READY = "artifact_ready"
    MATERIAL_INDEXED = "material_indexed"

@dataclass
class AgentEvent:
    type: EventType
    thread_id: str
    payload: dict          # GeneratedItem serializado, lista de preguntas, etc.
    v: int = 1             # versionado del schema

class EventEmitter:
    """Las tools lo reciben (o lo obtienen de un context var) y emiten eventos
    que exam-app reenvía por SSE/WS."""
    def emit(self, event: AgentEvent) -> None: ...
```

**Mecanismo:** las tools emiten eventos en paralelo al markdown. El markdown se conserva para historial/fallback (OpenWebUI legado). exam-app suscribe al event_bus del grafo y reenvía por SSE/WS.

---

## 🧩 libs/core — shared kernel (dominio + infraestructura compartida)

Lo que usan exam-app y agents-backend sin duplicar:

```
libs/core/src/core/
├── config.py                      # pydantic-settings (lee .env)
├── domain/
│   ├── models.py                  # entidades SQLAlchemy (Subject, Question, MaterialChunk…)
│   ├── bank/
│   │   ├── service.py             # escritura segura del banco
│   │   └── material.py            # indexación de material (RAG)
│   └── schemas/
│       ├── exam.py                # blueprints, ItemSpec, GeneratedItem
│       └── tools.py               # inputs de tools (TableColumn, etc.)
└── infrastructure/
    ├── db/
    │   ├── connection.py          # engine + SessionLocal
    │   └── migrations/            # Alembic (env.py, versions/)
    ├── embeddings/
    │   └── __init__.py            # RemoteEmbedder (cliente del embedding-service)
    ├── latex/
    │   ├── client.py              # cliente del latex-compiler
    │   ├── templates/             # base_exam.tex.jinja, quiz_short.tex.jinja, registry.py
    │   └── utils.py               # escape_latex, render_item, render_exam
    └── files/
        └── extract.py             # extract_file_text, gestión de data/inputs
```

### Reglas

- `libs/core` **no depende** de ninguna app. Es la capa más interna del monorepo.
- `agents-backend` y `exam-app` dependen de `libs/core`, nunca al revés.
- Los modelos SQLAlchemy viven aquí (fuente única de verdad del esquema de BD).
- Las migraciones Alembic viven aquí (el `alembic.ini` del meta-repo apunta aquí).

---

## 📦 Dependencias entre paquetes (instalación editable)

Cada app/lib tendrá `pyproject.toml` y se instalará en editable para desarrollo:

```bash
# En el venv del proyecto:
pip install -e libs/core
pip install -e apps/agents-backend
pip install -e apps/exam-app
```

Así los imports (`from core...`, `from agents_backend...`, `from exam_app...`) resuelven sin hacks de `sys.path`.

---

## ✅ Criterios de aceptación

- [ ] `agents-backend` no importa de `exam-app`
- [ ] `libs/core` no importa de ninguna app
- [ ] Las tools emiten eventos tipados vía `events.py`
- [ ] `_PENDING_ITEM` vive en `ConversationalState` (no global de módulo)
- [ ] Instalación editable funciona (`pip install -e`)
- [ ] Tests de cada paquete pasan de forma independiente

---

## 📝 Notas de sesión

- (vacío)

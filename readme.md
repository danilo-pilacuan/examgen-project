# Generador de Exámenes en latex propulsado por agentes de IA

MVP de infraestructura + agente conversacional con frontend propio (Vue 3).

> **Estado:** Etapas 0-8 completadas (monorepo, backend reactivo, frontend, widgets, pantallas, Docker, traducción al inglés con i18n en/es, **auth multi-profesor + navbar reactivo + CRUD completo**). Release: `Tag_V1.0.0`.

## Infraestructura del `MVP`

```
MVP_v1/
├── .env
├── .gitignore
├── alembic.ini
├── ARCHITECTURE.md
├── readme.md
│
├── data/
│   ├── agent_outputs/        # PDFs de exámenes generados
│   └── inputs/               # material de las materias (PDFs, pptx, etc.)
│
├── docker/
│   └── docker-compose.yml    # postgres + latex-compiler + embedding-service + exam-app + frontend
│
├── projects/                 # submódulos del monorepo
│   ├── core/                 # enums, schemas, banco, migraciones, plantillas LaTeX
│   ├── agents-backend/       # agente conversacional (tools, graph, prompts) + pipeline
│   ├── exam-app/             # FastAPI BFF (REST + SSE + WS)
│   ├── frontend/             # Vue 3 + Vite + Pinia + vue-i18n (en/es)
│   ├── latex-compiler/       # microservicio de compilación LaTeX
│   └── embedding-service/    # microservicio de embeddings (bge-m3)
│
├── scripts/
│   ├── index_material.py
│   └── run_pipeline.py
│
├── docs/                     # informe de avance y arquitectura objetivo (tesis)
│
└── .ops/                     # ciclo de vida OKF: plan, backlog, QA, handoff
```

## 🚀 Uso rápido (frontend propio)

```bash
# 0. (Recomendado) Levantar todo desde cero con la script automatizada:
#    python scripts\bring-up.py        (Windows)  /  python3 scripts/bring-up.py
#    (submódulos + .env con secretos + build + verificación + túnel público; ver RECIPE.md)

# 1. Levantar toda la infraestructura
cd docker && docker compose up -d --build
#    (el entrypoint de exam-app aplica las migraciones Alembic al arrancar)

# 2. Abrir el frontend
#    http://localhost:3000  → login/registro de profesor (sesión JWT)

# 3. Conversar con el agente
#    - "What subjects are registered?"        → list subjects
#    - "Work with Physics 1"                  → select_subject (el selector del header reacciona)
#    - "Give me questions about X"            → retrieve from the bank
#    - "Generate a question about X"          → generate new (RAG)
#    - "Change that question's difficulty to hard"  → update_question_tool
#    - "Delete that question"                 → delete_question_tool
#    - "Generate a 3-question exam with PDF"  → generates and attaches PDF
```

> **Multi-profesor:** cada profesor ve solo sus materias y sesiones (JWT + `subjects.owner_id`). Las materias creadas antes de la auth quedan compartidas entre todos. Definir `AUTH_SECRET` en producción.

## 🌐 Exponer al internet (demo / revisión externa)

- Guía: [docs/exposicion-internet.md](docs/exposicion-internet.md) — cloudflared quick tunnel, sin credenciales.
- Recipe desde clone fresco: [RECIPE.md](RECIPE.md) + una sola script multiplataforma: [scripts/bring-up.py](scripts/bring-up.py) (Python 3.7+, solo stdlib; si falta Python, el bootstrap portable está en el RECIPE).
- Runbook: [.ops/operations/RUN-016-exposicion-publica-cloudflared.md](.ops/operations/RUN-016-exposicion-publica-cloudflared.md) y recipe de levantamiento: [.ops/operations/recipe-levantamiento.md](.ops/operations/recipe-levantamiento.md).

## 🧪 Pipeline batch (API tradicional)

```bash
# Indexar material de una materia (RAG)
.venv/Scripts/python.exe scripts/index_material.py \
    --name "Economía Aplicada" \
    --materials "data/inputs/Economia_Aplicada/**/*.pdf"

# Generar un examen (PDF)
.venv/Scripts/python.exe scripts/run_pipeline.py
```

                ├── 5230ab459f09_initial_schema_with_pgvector.py
                ├── a1b2c3d4e5f6_add_material_chunks_for_rag.py
                └── b2c3d4e5f6a7_adjust_embeddings_1024.py
```

# Generador de Exámenes en latex propulsado por agentes de IA

MVP de infraestructura + agente conversacional con frontend propio (Vue 3).

> **Estado:** Etapas 0-7 completadas (monorepo, backend reactivo, frontend, widgets, pantallas, Docker, traducción al inglés con i18n en/es).

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
├── docs/                     # métricas y análisis de costos (tesis)
│   ├── metrics.md
│   └── cost_analysis.md
│
└── implementaciones/         # planes de etapa y progreso
```

## 🚀 Uso rápido (frontend propio)

```bash
# 1. Levantar toda la infraestructura
cd docker && docker compose up -d --build

# 2. Abrir el frontend
#    http://localhost:3000  → UI en inglés (selector EN/ES en la sidebar)

# 3. Conversar con el agente
#    - "What subjects are registered?"        → list subjects
#    - "Give me questions about X"            → retrieve from the bank
#    - "Generate a question about X"          → generate new (RAG)
#    - "Generate a 3-question exam with PDF"  → generates and attaches PDF
```

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

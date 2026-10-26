# 🧪 Evaluation Framework — Exam Generator Agent

> Framework de pruebas y benchmarking del agente generador de exámenes.
> Diseñado para la tesis USFQ: comparar capacidad de la herramienta, consumos,
> tokens, optimización de hiperparámetros y métricas del estado del arte de agentes.
>
> **Toda la documentación viva del framework vive en este README** (informe,
> plan de implementación, suite, metodología).

---

## 1. Qué evalúa

| Dimensión | Métricas | Fuente de datos |
|---|---|---|
| **Calidad de ítems** (`quality`) | `quality_score` del evaluador, tasa de aprobación, intentos por ítem, razón de rechazo | Estado del pipeline (`approved_items`, `rejection_log`) |
| **Diversidad** (`diversity`) | Similitud coseno (embeddings bge-m3) entre ítems aprobados, cobertura de temas y niveles de Bloom | Embeddings de los ítems + blueprint |
| **Calidad RAG** (`rag`) | Score de los chunks recuperados, cobertura del contexto, faithfulness aproximada (overlap léxico enunciado↔chunks) | `llm_responses.prompt` + chunks recuperados |
| **Alineación Bloom/dificultad** (`bloom`) | Accuracy del generador vs spec pedida (clasificación implícita), matriz de confusión Bloom | `GeneratedItem` vs `ItemSpec` |
| **Eficiencia de coste** (`coste`) | Llamadas LLM por ítem aprobado, latencia media, tokens estimados por ítem | `llm_responses` + usage del LLM |
| **Agentes SOTA** (`agentes`) | Robustez (varianza entre runs/materias clonadas), self-consistency (k runs del mismo spec), pass@k (aprobación en k intentos) | Agregación de runs |

## 2. Estructura

```
test/evaluation/
├── README.md                ← este archivo (informe + plan + metodología)
├── requirements.txt         ← dependencias extra del framework
├── models.yaml              ← REGISTRO CENTRAL de modelos multi-proveedor
├── experiments.yaml         ← definición de experimentos (qué comparar)
├── subjects.yaml            ← materias clonadas para las validaciones
├── src/
│   ├── models_registry.py   ← loader del registry multi-proveedor
│   ├── harness.py           ← orquestador de un run (pipeline + métricas + auditoría)
│   ├── metrics/
│   │   ├── quality.py       ← quality_score, aprobación, intentos, rechazos
│   │   ├── diversity.py     ← similitud embeddings, cobertura temas/Bloom
│   │   ├── rag.py           ← scores de recuperación, faithfulness
│   │   ├── bloom.py         ← alineación spec vs ítem generado
│   │   ├── cost.py          ← llamadas, latencia, tokens
│   │   └── agents.py        ← robustez, self-consistency, pass@k
│   ├── analysis/
│   │   └── aggregate.py     ← agrega N runs → comparativa por arm/config
│   └── reporting/
│       └── report.py        ← Markdown + PNG (matplotlib) por experimento
└── experiments/             ← outputs por experimento
    └── <exp_id>/            ← ej: E01_baseline_vs_reasoning
        ├── runs.jsonl       ← 1 línea por run (JSON completo del run)
        ├── aggregate.json   ← métricas agregadas comparativas
        └── report.md        ← informe Markdown + tablas
```

## 3. Registro central de modelos (`models.yaml`)

El punto central de configuración de **todos los modelos posibles**, de
distintos proveedores. Cada entrada define: nombre lógico, proveedor,
`base_url`, `model` (id que viaja al API), y `mode` (`real` | `stub`).

```yaml
models:
  glm-flash-default:            # nombre lógico del perfil
    provider: usfq-gateway
    base_url: https://ai.usfq.edu.ec/api/agents/llm/main/v1
    api_key_env: OPENAI_API_KEY  # variable de entorno con la key
    model: zai-org/GLM-5.3-Flash
    mode: real
  glm-stub-fast:                # stub local: no gasta tokens ni red
    provider: local-stub
    model: stub-glm-flash
    mode: stub
```

El **registry se puede extender** con cualquier proveedor OpenAI-compatible
(OpenAI, Anthropic vía proxy OpenAI, DeepSeek, Ollama, vLLM propio, etc.)
sin tocar código: solo añadir una entrada en `models.yaml`.

## 4. Materias clonadas (`subjects.yaml`)

Para **aislar la varianza del LLM** (y no la del material), todas las
validaciones comparativas usan el **mismo material** con **nombres distintos**:

```yaml
subjects:
  - id: eva
    name: Economía Aplicada — Eva         # clone 1 (base)
    material_glob: data/inputs/Economia_Aplicada/Apuntes/*.pdf
  - id: maria
    name: Economía Aplicada — María       # clone 2
    material_glob: data/inputs/Economia_Aplicada/Apuntes/*.pdf
  # ... hasta 5 clones (misma fuente, nombres distintos)
```

El harness registra cada clon como `Subject` en la BD, indexa su material
(RAG) una vez por clon, y corre el pipeline. Cada clon tiene su `subject_id`
propio → los ítems quedan en el banco separados por clon.

## 5. Experimentos (`experiments.yaml`)

Cada experimento define: id, descripción, lista de `arms` (configuraciones a
comparar), `repeats` (runs por arm), qué materias usar y qué blueprint.

```yaml
experiments:
  - id: E01_baseline_vs_temperature
    description: Sensibilidad del generador a la temperatura (0.3 / 0.7 / 1.0)
    arms:
      - model_profile: glm-flash-default
        overrides: { llm_temperature: 0.3 }
      - model_profile: glm-flash-default
        overrides: { llm_temperature: 0.7 }
    repeats: 3
    subjects: [eva, maria, sofia]
    blueprint: baseline_8q
```

Cada `arm` sobrescribe hiperparámetros (temperatura, reasoning, top_k RAG,
max_tokens, etc.) vía `overrides` — así se hace la **optimización de
hiperparámetros** de forma reproducible.

## 6. Ejecución

```powershell
# Dry-run (default — no llama al LLM real, sin coste)
.venv/Scripts/python.exe -m test.evaluation.src.harness --experiment E01_baseline_vs_temperature --dry-run

# Run real (llama al gateway USFQ; requiere Docker up + DB)
.venv/Scripts/python.exe -m test.evaluation.src.harness --experiment E01_baseline_vs_temperature --real

# Agregar + reporte comparativo
.venv/Scripts/python.exe -m test.evaluation.src.analysis.aggregate --experiment E01_baseline_vs_temperature
```

Flags útiles: `--list` (lista experimentos), `--limit-subjects eva` (subset de
clones), `--limit-repeats 1` (smoke test), `--dry-run` (stub determinista).

## 7. Estado

| Componente | Estado |
|---|---|
| `models.yaml` + `models_registry.py` | ✅ implementado |
| `subjects.yaml` + clonación de materias | ✅ implementado |
| `harness.py` (dry-run + real) | ✅ implementado |
| Métricas: quality, diversity, rag, bloom, coste, agentes | ✅ implementadas |
| `analysis/aggregate.py` + `reporting/report.py` | ✅ implementado |
| 4 experimentos definidos en `experiments.yaml` | ✅ |
| Dry-run E01–E04 validado end-to-end (61 runs, agregación + reportes + plots) | ✅ |
| **Runs reales E01–E04 completados: 82 runs GLM-5.3-Flash vía gateway USFQ** | ✅ (2026-10-26) |

### Resultados de la validación dry-run (stubs deterministas)

Estos números validan el **harness**, no el modelo real (el stub es
determinista). Lo relevante es que todas las familias de métricas se calculan
y discriminan entre brazos como se diseñó:

| Experimento | Runs | Hallazgo del harness |
|---|---|---|
| E01 temperatura | 27 | approval estable (~0.67); quality_mean baja monótonamente con la temperatura (7.76 → 6.89 en stub); σ entre clones ≤ 0.06 |
| E02 top_k RAG | 27 | `retrieval_top_k` se propaga al blueprint y cambia el score de recuperación (0.9 con k=1 vs 0.7 con k=3/8) |
| E03 robustez | 10 | σ entre clones (mismo material, nombres distintos) = 0.08 en quality → metodología de clones válida |
| E04 temp. evaluador | 18 | el override del evaluador llega al pipeline; approval varía entre brazos |

## 8. Metodología (informe de lo que vamos a hacer)

### Hipótesis
1. **H1 (capacidad):** el pipeline aprueba ≥ 70% de las ranuras del blueprint,
   con `quality_score` medio ≥ 7/10.
2. **H2 (hiperparámetros):** la temperatura del generador afecta la tasa de
   aprobación y diversidad de forma no monótona; existe un óptimo intermedio.
3. **H3 (diversidad):** la similitud media por pares de ítems aprobados es
   < 0.82 (umbral de dedup del sistema), validando el mecanismo anti-duplicados.
4. **H4 (RAG):** `top_k=3` da faithfulness (overlap léxico) > 0.3; subir
   `top_k` mejora cobertura pero aumenta tokens por ítem sin mejorar quality.
5. **H5 (robustez):** la varianza del `quality_score` entre materias clonadas
   (mismo material) es baja (σ < 1.0) → el pipeline es estable frente al material.

### Diseño experimental
- **Variable independiente:** configuración del arm (modelo, temperatura,
  reasoning, top_k RAG, etc.).
- **Variables dependientes:** las 6 familias de métricas del §1.
- **Control:** mismo material (materias clonadas), mismo blueprint (8 preguntas,
  distribuciones fijas de Bloom/dificultad/temas), semilla del planner fijada.
- **Repetición:** `repeats ≥ 3` por arm para estimar varianza.

### Reproducibilidad y reprocesabilidad
- Cada run guarda en `runs.jsonl`: config completa, blueprint, specs, ítems,
  evaluaciones, rechazos, latencias y audit trail de llamadas LLM.
- Cambiar de modelo = cambiar `model_profile` del arm en `experiments.yaml`
  (todo lo demás idéntico) → comparativa justa.
- `--dry-run` valida el harness completo sin coste: usa un stub determinista
  de LLM y embeddings stub con la misma interfaz que el sistema real.

### Métricas del estado del arte incluidas
- **Self-consistency** (Wang et al., 2022): k runs del mismo spec → % de specs
  aprobados en todas las repeticiones.
- **pass@k** (Chen et al., 2021): probabilidad de que un spec se apruebe en
  ≤ k intentos (k = `max_item_retries`).
- **Robustez ante perturbación**: mismo material con nombres distintos (clones)
  → varianza de métricas atribuible solo al LLM.
- **Faithfulness RAG** (aprox. overlap léxico): proporción del enunciado
  generada con tokens presentes en los chunks recuperados.
- **Eficiencia de coste**: llamadas LLM por ítem aprobado (↓ mejor), tokens
  por ítem (estimado chars/4 si el proveedor no devuelve usage).

## 9. Limitaciones conocidas

- El gateway USFQ no devuelve usage de tokens por llamada: la suite estima
  tokens (chars/4) desde los prompts y respuestas registradas.
- `reasoning_effort > none` rompe `with_structured_output` en el pipeline
  batch (documentado en `ARCHITECTURE.md`): los experimentos de reasoning
  aplican al chat, no al generador batch.
- Faithfulness por overlap léxico es una aproximación; para la tesis puede
  sustituirse por un judge LLM en una segunda fase.
- Los clones comparten archivos fuente, pero el índice RAG se reconstruye por
  clon (embeddings idénticos entre clones, nombres de materia distintos).
- En dry-run, la correlación retrieval↔statement es posicional (los rechazos
  no persisten su statement); en modo real la fila de auditoría lleva el
  prompt exacto por llamada.

## 10. Checklist para la primera ejecución real

1. `cd docker && docker compose up -d --build` (Postgres + latex-compiler +
   embedding-service + exam-app).
2. `alembic upgrade head` (o dejar que el contenedor lo aplique).
3. Exportar `OPENAI_API_KEY` con la key del gateway USFQ en la sesión.
4. Smoke real barato: `python -m test.evaluation.src.harness --experiment
   E03_robustness_clones --limit-subjects eva --limit-repeats 1 --real`
5. Ejecutar en orden de coste: E04 (18 runs) → E03 (10) → E01 (27) → E02 (27).
6. Agregar y reportar: `analysis.aggregate --experiment <id>` + `reporting.report`.
7. Archivar `aggregate.json` + `report.md` de cada experimento en la tesis.

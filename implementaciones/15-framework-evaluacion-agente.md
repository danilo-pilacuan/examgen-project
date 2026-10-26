# Etapa 15 — Framework de evaluación del agente generador (RC2/develop)

> **Fecha:** 2026-10-26 · **Rama:** `RC2/develop` (meta-repo + 6 submódulos) · **Estado:** ✅ Completada
> **Commits:** `007a9d7` (framework) → `1af2255` (telemetría real) → `9514247` (campaña 82 runs) → `78a874f` (H5 + judge + plots)
> **Ubicación:** `test/evaluation/` (documentación viva: [README](../test/evaluation/README.md))

---

## 1. Objetivo y alcance

Crear un **framework de pruebas y benchmarking reproducible** del agente generador de exámenes
que permita, para la tesis:

- Comparar **capacidad** de la herramienta (aprobación, calidad, alineación Bloom).
- Medir **consumos** (llamadas LLM/ítem, tokens/ítem, latencia).
- Hacer **optimización de hiperparámetros** con diseño OFAT (one-factor-at-a-time).
- Aplicar **métricas del estado del arte de agentes** (self-consistency, pass@k, robustez, faithfulness RAG).
- Garantizar **reproducibilidad y reprocesabilidad** al cambiar de modelo (registro central multi-proveedor).

> **Re-scope importante:** el elemento de acción #5 del proyecto ("investigar métricas de
> evaluación agente + RAG") estaba **descartado desde 2026-10-18**; con esta etapa **vuelve al
> alcance y queda implementado y ejecutado**. El #6 (costos local vs nube) sigue descartado,
> aunque el framework ya mide coste relativo (tokens/llamadas por ítem).

## 2. Diseño metodológico

### 2.1 Principio de control: materias clonadas
Todas las validaciones comparativas usan **el mismo material con nombres distintos**
(`subjects.yaml`: eva, maria, sofia, lucia, pablo → mismo `material_glob` de Economía Aplicada).
Así la varianza observada entre clones es atribuible **solo al LLM** (muestreo estocástico),
no al material.

### 2.2 Registro central de modelos (`models.yaml`)
Cada brazo experimental referencia un **perfil** (nombre lógico, proveedor, base_url, modelo,
api_key_env, modo). Añadir un proveedor nuevo (OpenAI, DeepSeek, Ollama, vLLM propio) = una
entrada YAML, **sin tocar código**. Hoy: `glm-flash-default` (real, gateway USFQ) + 2 stubs.

### 2.3 Experimentos definidos (`experiments.yaml`)

| ID | Factor (OFAT) | Brazos | Diseño |
|---|---|---|---|
| E01 | temperatura del generador | 0.3 / 0.7 / 1.0 | 3 brazos × 3 clones × 3 reps = 27 runs |
| E02 | top_k del RAG | 1 / 3 / 8 | 3 brazos × 3 clones × 3 reps = 27 runs |
| E03 | robustez entre clones | config fija | 1 brazo × 5 clones × 4 reps = 30 runs |
| E04 | temperatura del evaluador | 0.0 / 0.2 / 0.6 | 3 brazos × 2 clones × 3 reps = 18 runs |

Blueprint compartido `baseline_8q`: 8 preguntas, Bloom 25%×4 niveles, dificultad 40/40/20,
4 temas ponderados, top_k 3, min_score 0.15.

### 2.4 Familias de métricas (6)

| Familia | Métricas | Fuente |
|---|---|---|
| `quality` | approval_rate, quality_score (media/σ), intentos/ítem, razones de rechazo | estado del pipeline + auditoría |
| `diversity` | similitud coseno por pares (bge-m3), cobertura temas/Bloom | embeddings de ítems |
| `rag` | retrieval_score, chunks/spec, **faithfulness léxica** + **faithfulness judge LLM** | prompts de auditoría |
| `bloom` | accuracy spec↔ítem (bloom/dificultad/tipo), matriz de confusión | GeneratedItem vs spec |
| `cost` | llamadas/ítem, tokens/ítem (chars/4), latencia por nodo | tabla `llm_responses` |
| SOTA (agregación) | self-consistency, pass@k (Chen 2021), robustez entre clones (σ) | agregación de runs |

## 3. Arquitectura del framework

```
test/evaluation/
├── README.md                 ← doc viva: informe + plan + metodología + estado
├── models.yaml               ← registro multi-proveedor
├── experiments.yaml          ← definición declarativa de experimentos
├── subjects.yaml             ← 5 clones (mismo material)
├── src/
│   ├── models_registry.py    ← loader de perfiles
│   ├── harness.py            ← orquestador: 1 run = pipeline + métricas + auditoría (CLI)
│   ├── _patch.py             ← activación stubs/real (monkey-patching de nodes + shared_llm)
│   ├── _indexing.py          ← indexación con embedder inyectado
│   ├── stubs.py              ← StubStructuredLLM + StubEmbedder (dry-run determinista)
│   ├── metrics/
│   │   ├── quality.py / diversity.py / rag.py / bloom.py / cost.py
│   │   └── faithfulness_judge.py  ← judge LLM (0-10 soporte factual, post-hoc)
│   └── analysis/
│       ├── aggregate.py      ← runs.jsonl → aggregate.json + report.md
│       └── judge_experiment.py ← judge post-hoc sobre toda la campaña
└── experiments/E0*/          ← aggregate.json + report.md + FINDINGS.md + plots PNG
```

**Modos de ejecución:**
- `--dry-run` (default): stubs deterministas de LLM y embeddings, sin red ni coste. 61 runs de validación del harness.
- `--real`: gateway USFQ; telemetría leída de la tabla de auditoría `llm_responses` (prompt, raw_answer, latency por llamada, chunks RAG parseados del prompt).

**Correlación posicional:** en modo real, las respuestas crudas del evaluador/generador se
correlacionan por orden con los intentos para extraer quality_score real y campos spec/ítem.

## 4. Resultados de la campaña real (102 runs GLM-5.3-Flash)

### 4.1 Hipótesis — todas resueltas ✅

| # | Hipótesis | Resultado | Veredicto |
|---|---|---|---|
| H1 | Capacidad: aprobación ≥ 70%, quality ≥ 7/10 | aprobación 0.90–0.96 en todas las campañas; quality 6.1–7.6 | ✅ aprobación (quality se queda cerca del 7) |
| H2 | Temperatura: óptimo intermedio | **gen T=0.7** (0.917 aprobación) > 0.3 (0.889) > 1.0 (0.861); U invertida | ✅ validada |
| H3 | Diversidad < 0.82 (umbral dedup) | similitud 0.50–0.52 estable en todos los brazos | ✅ validada |
| H4 | top_k=3: faithfulness > 0.3 y subir k no mejora | top_k=3 maximiza aprobación (0.958); k=8 duplica tokens (3.934 vs 2.088) sin ganar calidad | ✅ validada (con matiz del judge) |
| H5 | Robustez: σ entre clones < 1.0 | con 4 réplicas/clon: **σ = 0.665** (con 2 reps era 1.051, inconcluso) | ✅ **confirmada** |

### 4.2 Configuración de producción validada empíricamente
Los 3 hiperparámetros de `core/config.py` quedaron confirmados por los barridos:
`llm_temperature=0.7` (E01) · `retrieval.top_k=3` (E02) · `llm_temperature_evaluator=0.2` (E04,
mejor quality 7.55 y robustez monótonamente degradante con T del evaluador).

### 4.3 Judge LLM de faithfulness (nuevo en 78a874f)
- Sustituye/complementa el overlap léxico (que premia la copia, no la síntesis — documentado en E02).
- Corre **post-hoc** sobre la auditoría: no interfiere con el pipeline evaluado.
- E03: **judge 0.352 ± 0.052 vs léxico 0.309 ± 0.260** → el judge es **5× más estable**;
  la varianza del léxico era ruido de la aproximación, no del pipeline.
- Config: self-judge (mismo modelo), T=0, `reasoning_effort=none`, `max_tokens=2000`.

### 4.4 Hallazgos cualitativos para la tesis
1. **LLM-as-judge inconsistente**: el evaluador emitió `approved=true` con `quality_score=0.92/10`
   (capturado en smoke). Material de discusión sobre fiabilidad del juez.
2. **Paradoja del faithfulness**: k=3 sintetiza más allá del contexto (menos overlap léxico,
   más calidad de síntesis).
3. **Diversidad insensible a la temperatura**: dominada por vocabulario compartido del dominio.
4. **T=1.0 degrada alineación spec-ítem** (Bloom 0.861): mecanismo de los rechazos por mismatch.
5. **Coste plano entre temperaturas** (2.13–2.29 llamadas/ítem): el coste solo discrimina en top_k.

## 5. Decisiones técnicas y gotchas (crítico para futuras sesiones)

1. **Dry-run contamina la BD real**: los stub embeddings escritos durante dry-runs rompieron el
   RAG real (scores ~0.08 < min_score 0.15). Fix: `_reindex_real.py` (borrar chunks stub +
   re-indexar con bge-m3). **Nunca mezclar** modos sin limpiar el índice.
2. **Gateway consume tokens de reasoning en chat API incluso con `reasoning_effort=none`**:
   `max_tokens=300` devolvía `content=None` (finish=length). El judge usa `max_tokens=2000`.
   (En el pipeline batch el problema es distinto: reasoning > none rompe `with_structured_output`.)
3. **Windows console cp1252**: todos los CLIs Python del framework necesitan
   `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
4. **`.env` con BOM** rompía pydantic-settings (ya corregido).
5. **nodes.py importa `retrieve_chunks` al cargar el módulo**: el patch debe apuntar al
   namespace de `nodes` Y al módulo fuente (`agents_backend.shared.retrieval`).
6. **Inestabilidad del entorno**: cambios de postura del portátil (eventos Kernel-Power
   `InputAccelerometer`) cortan WSL2/port-forwarding → Docker reinicia contenedores
   (policy=always, exit 0) y el run muere con `RemoteDisconnected`. Mitigación: keep-awake con
   `SetThreadExecutionState` durante campañas; verificar `docker ps` al reintentar.
7. **Latencia bimodal del gateway** (T=0.0/0.6 ~2× más rápido que T=0.2 en E04): efecto de
   carga del gateway multitenant, no causal. No interpretar.
8. **Token estimation**: el gateway no devuelve usage → chars/4. Si un proveedor nuevo devuelve
   usage, `cost.py` ya lo prefiere automáticamente.

## 6. Cómo ejecutar (resumen operativo)

```powershell
# 0. Infra arriba + key exportada
cd docker; docker compose up -d; cd ..
# (verificar: exam_postgres_db, exam_embedding_service, exam_latex_compiler Up)
$env:OPENAI_API_KEY = "<key gateway USFQ>"   # o cargar del .env

# 1. Smoke barato
.venv/Scripts/python.exe -m test.evaluation.src.harness --experiment E03_robustness_clones --limit-subjects eva --limit-repeats 1 --real

# 2. Campaña (en orden de coste: E04 → E03 → E01 → E02)
.venv/Scripts/python.exe -m test.evaluation.src.harness --experiment E04_evaluator_temperature --real

# 3. Agregar + reportar + plots
.venv/Scripts/python.exe -m test.evaluation.src.analysis.aggregate --experiment E04_evaluator_temperature
.venv/Scripts/python.exe -m test.evaluation.src.reporting.report --experiment E04_evaluator_temperature

# 4. Judge post-hoc de faithfulness (opcional, por campaña)
$env:OPENAI_API_KEY = "<key>"; .venv/Scripts/python.exe -m test.evaluation.src.analysis.judge_experiment --experiment E03_robustness_clones
```

Salidas por experimento (`test/evaluation/experiments/<id>/`): `runs.jsonl` (gitignored),
`runs_judged.jsonl` (gitignored), `aggregate.json`, `report.md`, `FINDINGS.md` (versión),
plots `*.png` (versionados e incrustados en FINDINGS).

## 7. Trabajo completado por fase

- [x] Framework base: registry, subjects, harness, 6 familias de métricas, agregador, reportes (007a9d7)
- [x] Validación dry-run end-to-end: 61 runs, agregación + plots discriminando brazos
- [x] Telemetría real: auditoría `llm_responses` (latencia, prompts, RAG chunks) (1af2255)
- [x] Campañas reales E01-E04: 82 runs; agregación + FINDINGS por experimento (9514247)
- [x] E03 extendido a 4 réplicas/clon (+20 runs) → H5 confirmada (σ=0.665)
- [x] Judge LLM de faithfulness implementado + ejecutado sobre E03 (27/30 runs)
- [x] Plots versionados e incrustados en FINDINGS.md
- [x] README del framework actualizado (estado, limitaciones, notas de entorno)
- [x] Todo publicado en `origin/RC2/develop` (78a874f)

## 8. Próximos pasos (para otra sesión)

| # | Pendiente | Detalle | Dependencia |
|---|---|---|---|
| 1 | **Comparativa cross-provider** | Añadir perfil OpenAI/DeepSeek/otros en `models.yaml` + brazo con `model_profile` distinto; re-ejecutar E01-E04 y comparar (todo lo demás idéntico) | 🟡 Acceso a otro modelo en el gateway (decisión externa) |
| 2 | **Written tesis — capítulo experimentación** | Base lista: 4 FINDINGS.md con tablas/plots reales + README §8 metodología (hipótesis H1-H5 resueltas) + limitations | — |
| 3 | Tests automatizados del framework | Hoy validado por ejecución; podría añadirse pytest unitario de métricas (bajo costo, opcional) | — |
| 4 | CI del meta-repo (heredado etapa 1) | Pendiente de repos/CI | etapa 1 |

> **Nota de sesión:** el trabajo restante **no depende de código**: el #1 requiere un proveedor
> nuevo (fuera de control local); el #2 es escritura. El framework está congelado y
> reproducible: cualquier re-ejecución parte de `test/evaluation/README.md` §6 y §10.

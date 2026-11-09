# Informe rápido — Experimentos de evaluación LLM (Round 11)

> Lectura estimada: 3 minutos. Fuentes: `test/evaluation/experiments/E0{1..4}_{nombre}/aggregate.json` y `FINDINGS.md` (campaña real, 82 runs completados).

## 1. Contexto

- **Modelo:** GLM-5.3-Flash (gateway USFQ). **Pipeline:** un LLM genera ítems → otro LLM los evalúa.
- **82 corridas reales**, todas completadas. Config de producción: generador T=0.7, evaluador T=0.2, RAG `top_k=3`.
- Objetivo: validar empíricamente que esa configuración es la mejor en **calidad, costo y robustez**.

## 2. Qué experimentos se hicieron

| # | Experimento | Variable manipulada | Brazos | Runs | Pregunta |
|---|---|---|---|---|---|
| E01 | `temperature_sweep` | Temperatura del **generador** | 0.3 / 0.7 / 1.0 | 27 | ¿Qué T genera mejores ítems? |
| E02 | `rag_topk_sweep` | Chunks de contexto RAG | top_k = 1 / 3 / 8 | 27 | ¿Más contexto ayuda o diluye? |
| E03 | `robustness_clones` | Sujeto (5 clones de "profesor") | config fija | 10 | ¿El pipeline es estable entre materias? |
| E04 | `evaluator_temperature` | Temperatura del **evaluador** | 0.0 / 0.2 / 0.6 | 18 | ¿El evaluador robusto a su propia T? |

## 3. Qué significa cada métrica

**Alineamiento (¿entregó lo que se pidió?)**
- `approval_rate` — fracción de ítems aprobados por el evaluador. La métrica principal.
- `bloom_accuracy` / `topic_coverage` — % de ítems que respetan el nivel Bloom / los temas pedidos.

**Calidad y diversidad**
- `quality_mean` — puntaje de calidad del LLM evaluador (0-10).
- `quality_std` — dispersión de esos puntajes dentro de una corrida.
- `pairwise_sim_mean` — similitud entre ítems generados (más bajo = más diverso; 0.82 = umbral de duplicado).

**Costo y eficiencia**
- `tokens_per_item`, `calls_per_item` — costo por ítem entregado.
- `attempts_per_item` — cuántas veces se regeneró un ítem rechazado.

**RAG y robustez**
- `rag_retrieval_score` — relevancia de los chunks recuperados.
- `rag_faithfulness` — fidelidad al material recuperado (⚠ solo la variante léxica, ver §6).
- `robustness_cross_subject` (σ) — dispersión de calidad *entre* clones; menor = más estable.

## 4. Resultados clave

### E01 — Temperatura del generador (27 runs)
Aprobaron 1.000 → 0.944 → 0.917 (T = 0.3 / 0.7 / 1.0). La calidad decae monotónicamente con la temperatura; T=1.0 además pierde cobertura de temas (0.972) y cuesta más (2,249 tokens, ~4.9 s). **Conclusión:** T=0.7 queda validada (zona plana óptima); T=0.3 es la alternativa más barata (0 reintentos, 1,995 tokens). La diversidad **no** depende de la temperatura.

### E02 — Contexto RAG (27 runs)
`top_k=8` está **dominado**: approval baja a 0.875, Bloom accuracy 0.875, y el costo casi se triplica (4,211 vs 1,454-2,107 tokens). `k=1` y `k=3` empatan en alineamiento (0.986), pero `k=3` cubre todos los temas. **Conclusión:** más contexto ≠ mejor calidad; `top_k=3` confirmado.

### E03 — Robustez entre clones (10 runs)
Approval alto y estable (0.912 ± 0.10) en los 5 "profesores", pero la calidad oscila mucho entre clones (2.85-6.33; σ = 1.31 > umbral 1.0). La recuperación es idéntica entre clones (0.489 ± 0.00), así que la variabilidad **viene del generador, no del material**. **Conclusión:** con solo 2 repeticiones/clon no conviene defender la hipótesis de estabilidad; extender a ≥4 repeticiones (20 runs, ~35 min).

### E04 — Temperatura del evaluador (18 runs)
El veredicto aprobar/rechazar es casi insensible a la T (0.938-0.979). T=0.2 es la más eficiente (menos reintentos y llamadas, mejor Bloom accuracy 0.979). Curiosidad para el capítulo de LLM-as-judge: a T=0.6 el evaluador **califica más benévolo** (5.55 vs 4.38) — mide la calibración del juez, no solo la calidad.

## 5. Conclusión única

La configuración de producción **generador 0.7 / evaluador 0.2 / top_k 3** queda validada en los 4 experimentos; los extremos explorados (T=1.0, top_k=8, eval T=0.6) solo agregan costo o varianza.

## 6. Caveat: fidelidad con juez LLM

La métrica de fidelidad con **juez LLM** salió vacía (`num_judged=0`) en las 82 corridas por un bug del harness (correlación de chunks, corregido después de la campaña). Todo lo que se reporta de RAG usa la métrica **léxica** (`rag_faithfulness`), que es conservadora y castiga la copia superficial; el juez LLM queda para una ronda futura.

## 7. Datos de una cifra por experimento (opcional en exposición)

| Experimento | Cifra para citar |
|---|---|
| E01 | Approval 1.000 (T=0.3) vs 0.917 (T=1.0) |
| E02 | top_k=8: approval 0.875 y 4,211 tokens vs 0.986 y 2,107 con top_k=3 |
| E03 | σ entre clones 1.31 > 1.0 (H5 no confirmada con 2 repeticiones) |
| E04 | Eval T=0.2: mejor Bloom accuracy (0.979) y menos reintentos (0.021) |

# E03 — Robustez entre clones (RESULTADOS REALES)

> 10 runs reales (1 brazo × 5 clones × 2 repeticiones), GLM-5.3-Flash vía
> gateway USFQ. Config idéntica en todos los runs (temperatura 0.7,
> evaluador 0.2, top_k 3); material idéntico; solo cambia el nombre de la
> materia (Eva, María, Sofía, Lucía, Pablo). Todos los runs terminaron
> `completed` con PDF compilado.

## Resultados

| Métrica | Media ± σ (10 runs) |
|---|---|
| Tasa de aprobación | 0.925 ± 0.08 |
| Quality score medio (attempts) | 6.15 ± 1.26 |
| Similitud por pares (diversidad) | 0.510 ± 0.03 |
| RAG retrieval score | 0.465 ± 0.01 |
| RAG faithfulness | 0.235 ± 0.24 |
| Bloom accuracy | 0.925 ± 0.08 |
| Llamadas por ítem aprobado | 2.12 ± 0.27 |
| Tokens por ítem (estimado) | 2.080 ± 293 |

## Robustez entre clones (misma config, material idéntico)

Quality score medio por clon (2 runs cada uno): σ entre clones = **1.051**.

## Hallazgos

1. **Aprobación alta y estable** (0.925 ± 0.08): el pipeline aprueba ~7.4 de
   8 ítems por run de forma consistente en 5 "profesores" distintos.

2. **σ entre clones = 1.05** sobre quality medio ~6.15: varianza moderada.
   Con solo 2 repeticiones por clon el estimador es ruidoso; para la tesis
   conviene subir a 3–5 repeticiones por clon. La hipótesis H5 (σ < 1.0)
   queda **en el límite**: ni confirmada ni refutada con este tamaño
   muestral — se necesita más réplicas para resolverla.

3. **Faithfulness RAG con alta varianza** (0.235 ± 0.24): algunos enunciados
   se apoyan fuertemente en el contexto recuperado, otros son más genéricos.
   El retrieval score es muy estable (0.465 ± 0.01): la variación viene del
   generador, no del recuperador.

4. **Diversidad estable**: similitud por pares 0.51 en todos los clones,
   muy por debajo del umbral de duplicados (0.82): el mecanismo anti-dup
   no se dispara en condiciones normales (valida H3).

5. **Coste consistente**: 2.1 llamadas/ítem y ~2.080 tokens/ítem con poca
   dispersión — el coste del pipeline es predecible.

## Nota metodológica

Los ítems y evaluaciones son idénticos entre clones hasta la semilla del
planner: la varianza observada es atribuible al LLM (muestreo estocástico
de temperatura 0.7), no al material. Con más réplicas por clon, σ entre
clones converge a la varianza pura del modelo.

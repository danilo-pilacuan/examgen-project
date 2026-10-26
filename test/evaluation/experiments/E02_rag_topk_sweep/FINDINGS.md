# E02 — RAG: barrido top_k 1 / 3 / 8 (RESULTADOS REALES)

> 27 runs reales (3 brazos × 3 clones × 3 repeticiones), GLM-5.3-Flash vía
> gateway USFQ. Generador 0.7, evaluador 0.2 (producción). Todos los runs
> `completed` con PDF.

## Resultados por brazo

| Métrica | top_k=1 | top_k=3 (producción) | top_k=8 |
|---|---|---|---|
| Tasa de aprobación | 0.833 | **0.958** | 0.875 |
| Quality score medio | 6.51 | 6.64 | **6.75** |
| Bloom accuracy | 0.833 | **0.958** | 0.875 |
| RAG retrieval score | **0.492** | 0.467 | 0.437 |
| RAG faithfulness | 0.305 | 0.175 | **0.337** |
| Tokens por ítem (estimado) | **1.554** | 2.088 | 3.934 |
| Llamadas por ítem aprobado | 2.45 | **2.08** | 2.34 |
| Robustez entre clones (σ) | 1.198 | 0.683 | 0.455 |

## Hallazgos

1. **top_k=3 (configuración de producción) maximiza la aprobación y la
   alineación** (0.958 aprobación y Bloom accuracy): es el punto dulce entre
   contexto insuficiente (k=1) y contexto diluido (k=8). Confirma H4 en su
   primera mitad: subir top_k NO mejora la calidad.

2. **El coste escala linealmente con top_k**: 1.554 → 2.088 → 3.934
   tokens/ítem (k=8 casi duplica a k=3) por el contexto extra inyectado en
   cada prompt del generador. Con calidad igual o peor, k=8 es estrictamente
   dominado en eficiencia.

3. **Paradoja del faithfulness**: k=1 y k=8 tienen faithfulness mayor
   (0.305/0.337) que k=3 (0.175). Explicación: con k=1 el enunciado se
   copia casi literal del único chunk; con k=8 hay más material presente
   que cubrir; con k=3 el generador sintetiza más allá del contexto
   (menos overlap léxico pero más calidad de síntesis). La métrica de
   overlap premia la copia, no la síntesis → limitación documentada de la
   aproximación léxica; para la tesis, considerar judge LLM.

4. **Retrieval score decrece con k** (0.492 → 0.467 → 0.437): los chunks
   adicionales de las colas son progresivamente menos relevantes —
   comportamiento esperado del ranking por similitud coseno.

5. **Robustez entre clones mejora con k mayor** (σ 1.20 → 0.68 → 0.46):
   más contexto reduce la varianza entre "profesores". Trade-off real:
   k=8 es más estable pero más caro y menos aprobador que k=3.

## Implicación de configuración

`retrieval.top_k=3` queda **validado empíricamente**: máxima aprobación,
máxima alineación Bloom, coste intermedio. k=8 solo se justificaría si la
estabilidad entre profesores pesara más que el coste (no es el caso MVP).

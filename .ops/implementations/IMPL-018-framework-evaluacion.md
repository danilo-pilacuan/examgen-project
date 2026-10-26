---
id: IMPL-018
tipo: Implementation
type: Implementation
title: Framework de evaluacion del agente (RC2)
description: Harness OFAT con 6 familias de metricas; 102 runs reales; H1-H5 resueltas (2026-10-26).
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [BL-019, BL-020, BL-021, IMPL-004, IMPL-012]
status: stable
---

## Alcance

Incluye: framework reproducible de pruebas y benchmarking del agente en
`test/evaluation/`: registro multi-proveedor (models.yaml), experimentos declarativos
(experiments.yaml, E01-E04 OFAT), 5 clones de materia para aislamiento de varianza, 6
familias de metricas (quality, diversity, rag, bloom, cost, SOTA), modo dry-run con stubs
deterministas y modo real con telemetria de llm_responses, mas judge LLM de faithfulness
post-hoc. No incluye: comparativa cross-provider (BL-019, depende de acceso a otro
modelo).

## Diseno

Campana real: 102 runs GLM-5.3-Flash. Hipotesis H1-H5 resueltas: aprobacion 0.90-0.96;
T=0.7 optimo (U invertida); similitud 0.50-0.52 (diversidad estable); top_k=3 maximiza
aprobacion sin ganar calidad con k=8; robustez sigma=0.665 con 4 replicas/clon.
Hiperparametros de produccion confirmados: T gen=0.7, top_k=3, T eval=0.2. Judge 5x mas
estable que el overlap lexico (0.352+-0.052 vs 0.309+-0.260). Commits: 007a9d7 ->
1af2255 -> 9514247 -> 78a874f. Ejecucion y limitaciones: `test/evaluation/README.md`
(secciones 6 y 10). Gotchas criticos en el handoff.
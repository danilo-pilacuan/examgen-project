# Experiment Report — E02_rag_topk_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, retrieval_top_k=1) | zai-org/GLM-5.3-Flash | 0.833±0.12 | 6.506±1.76 | 2.616±1.44 | 0.194±0.15 | 0.508±0.03 | 0.972±0.08 | 0.630±0.07 | 0.305±0.17 | 0.492±0.00 | 0.833±0.12 | 0.833±0.12 | 2.447±0.34 | 1554.444±235.51 | 8853.889±3390.10 |
| arm_1 (llm_temperature=0.7, retrieval_top_k=3) | zai-org/GLM-5.3-Flash | 0.958±0.06 | 6.642±1.08 | 2.938±1.06 | 0.042±0.06 | 0.510±0.02 | 0.972±0.08 | 0.667±0.00 | 0.175±0.25 | 0.467±0.00 | 0.958±0.06 | 0.958±0.06 | 2.081±0.15 | 2088.333±170.53 | 13357.222±5695.23 |
| arm_2 (llm_temperature=0.7, retrieval_top_k=8) | zai-org/GLM-5.3-Flash | 0.875±0.13 | 6.746±1.24 | 3.023±1.11 | 0.139±0.15 | 0.485±0.03 | 1.000±0.00 | 0.648±0.05 | 0.337±0.30 | 0.437±0.00 | 0.875±0.13 | 0.875±0.13 | 2.341±0.37 | 3934.000±701.89 | 7232.889±1260.19 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=1.198
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.683
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.4548
# Experiment Report — E01_temperature_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.3) | zai-org/GLM-5.3-Flash | 0.889±0.14 | 6.392±1.22 | 3.373±1.13 | 0.125±0.17 | 0.519±0.02 | 0.944±0.10 | 0.667±0.00 | 0.243±0.28 | 0.468±0.00 | 0.889±0.14 | 0.889±0.14 | 2.276±0.39 | 2227.444±444.03 | 18162.778±8289.31 |
| arm_1 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.917±0.13 | 6.505±1.55 | 3.089±1.12 | 0.097±0.16 | 0.501±0.03 | 0.944±0.10 | 0.648±0.05 | 0.162±0.23 | 0.469±0.00 | 0.917±0.13 | 0.917±0.13 | 2.233±0.36 | 2136.667±412.39 | 10014.556±6425.71 |
| arm_2 (llm_temperature=1.0) | zai-org/GLM-5.3-Flash | 0.861±0.11 | 6.426±1.63 | 3.008±1.54 | 0.153±0.13 | 0.502±0.02 | 0.944±0.10 | 0.667±0.00 | 0.321±0.24 | 0.468±0.00 | 0.861±0.11 | 0.861±0.11 | 2.341±0.28 | 2286.667±251.66 | 7064.667±1271.14 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.8365
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.7317
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.3321
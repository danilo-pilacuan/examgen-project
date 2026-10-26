# Experiment Report — E01_temperature_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.3) | zai-org/GLM-5.3-Flash | 0.667±0.06 | 7.764±0.14 | 0.205±0.13 | 0.347±0.08 | -0.003±0.00 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.022±0.25 | 950.667±93.03 | 0.000±0.00 |
| arm_1 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.681±0.09 | 7.229±0.08 | 0.261±0.10 | 0.333±0.12 | -0.006±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 2.993±0.43 | 937.111±152.12 | 0.000±0.00 |
| arm_2 (llm_temperature=1.0) | zai-org/GLM-5.3-Flash | 0.667±0.08 | 6.893±0.13 | 0.155±0.10 | 0.361±0.12 | -0.006±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.052±0.42 | 962.111±145.31 | 0.000±0.00 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.06
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.0461
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.0559
# Experiment Report — E04_evaluator_temperature

Total runs: 18

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, llm_temperature_evaluator=0.0) | zai-org/GLM-5.3-Flash | 0.667±0.06 | 7.295±0.13 | 0.311±0.10 | 0.354±0.09 | -0.006±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.022±0.25 | 949.833±82.17 | 0.000±0.00 |
| arm_1 (llm_temperature=0.7, llm_temperature_evaluator=0.2) | zai-org/GLM-5.3-Flash | 0.625±0.07 | 7.229±0.08 | 0.184±0.12 | 0.417±0.12 | -0.009±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.244±0.39 | 1025.667±139.97 | 0.000±0.00 |
| arm_2 (llm_temperature=0.7, llm_temperature_evaluator=0.6) | zai-org/GLM-5.3-Flash | 0.625±0.12 | 7.336±0.07 | 0.284±0.13 | 0.438±0.19 | -0.008±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.333±0.67 | 1060.000±235.06 | 0.000±0.00 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.0747
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.0111
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.0425
# Experiment Report — E04_evaluator_temperature

Total runs: 18

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | rag_faithfulness_judge | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, llm_temperature_evaluator=0.0) | zai-org/GLM-5.3-Flash | 0.938±0.10 | 4.706±1.31 | 4.021±0.35 | 0.062±0.10 | 0.492±0.02 | 1.000±0.00 | 0.667±0.00 | 0.025±0.04 | 0.489±0.00 | — | 0.938±0.10 | 0.938±0.10 | 2.159±0.25 | 2248.667±198.87 | 6777.167±2046.73 |
| arm_1 (llm_temperature=0.7, llm_temperature_evaluator=0.2) | zai-org/GLM-5.3-Flash | 0.979±0.05 | 4.377±1.02 | 3.805±0.21 | 0.021±0.05 | 0.503±0.03 | 1.000±0.00 | 0.667±0.00 | 0.021±0.05 | 0.490±0.00 | — | 0.979±0.05 | 0.979±0.05 | 2.027±0.12 | 2129.833±172.47 | 6195.333±2115.78 |
| arm_2 (llm_temperature=0.7, llm_temperature_evaluator=0.6) | zai-org/GLM-5.3-Flash | 0.938±0.10 | 5.552±1.63 | 3.167±0.30 | 0.062±0.10 | 0.520±0.03 | 0.958±0.09 | 0.667±0.00 | 0.026±0.04 | 0.489±0.00 | — | 0.938±0.10 | 0.938±0.10 | 2.159±0.25 | 2185.333±352.61 | 5503.000±1583.19 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.5256
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.6839
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.4189
# Experiment Report — E04_evaluator_temperature

Total runs: 18

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, llm_temperature_evaluator=0.0) | zai-org/GLM-5.3-Flash | 0.958±0.06 | 6.772±0.68 | 3.451±0.57 | 0.042±0.06 | 0.518±0.02 | 1.000±0.00 | 0.667±0.00 | 0.169±0.25 | 0.468±0.00 | 0.958±0.06 | 0.958±0.06 | 2.095±0.13 | 2119.500±167.00 | 12590.167±2748.76 |
| arm_1 (llm_temperature=0.7, llm_temperature_evaluator=0.2) | zai-org/GLM-5.3-Flash | 0.917±0.06 | 7.554±0.49 | 2.335±0.84 | 0.083±0.06 | 0.506±0.01 | 0.958±0.09 | 0.667±0.00 | 0.322±0.23 | 0.468±0.00 | 0.917±0.06 | 0.917±0.06 | 2.191±0.13 | 2209.833±205.34 | 22450.167±5806.43 |
| arm_2 (llm_temperature=0.7, llm_temperature_evaluator=0.6) | zai-org/GLM-5.3-Flash | 0.917±0.06 | 6.300±1.40 | 2.994±1.12 | 0.083±0.06 | 0.507±0.01 | 0.958±0.09 | 0.667±0.00 | 0.344±0.25 | 0.468±0.00 | 0.917±0.06 | 0.917±0.06 | 2.191±0.13 | 2145.333±98.44 | 11701.833±2429.95 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.0992
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.3394
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.6663
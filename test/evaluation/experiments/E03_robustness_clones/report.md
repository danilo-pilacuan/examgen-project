# Experiment Report — E03_robustness_clones

Total runs: 10

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.637±0.04 | 7.266±0.19 | 0.208±0.14 | 0.375±0.06 | -0.005±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.147±0.16 | 987.900±53.52 | 0.000±0.00 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.0807
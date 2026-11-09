# Experiment Report — E03_robustness_clones

Total runs: 10

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | rag_faithfulness_judge | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.912±0.10 | 4.553±1.63 | 3.775±0.38 | 0.087±0.10 | 0.502±0.01 | 0.975±0.07 | 0.667±0.00 | 0.046±0.05 | 0.489±0.00 | — | 0.912±0.10 | 0.912±0.10 | 2.219±0.26 | 2232.300±299.66 | 5077.000±1284.99 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=1.3106
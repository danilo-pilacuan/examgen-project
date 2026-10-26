# Experiment Report — E03_robustness_clones

Total runs: 10

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.925±0.08 | 6.153±1.26 | 3.328±1.14 | 0.087±0.11 | 0.510±0.03 | 1.000±0.00 | 0.667±0.00 | 0.235±0.24 | 0.465±0.01 | 0.925±0.08 | 0.925±0.08 | 2.117±0.27 | 2079.700±293.27 | 15020.100±7299.61 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=1.051
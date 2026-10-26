# Experiment Report — E03_robustness_clones

Total runs: 30

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | rag_faithfulness_judge | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.904±0.10 | 6.609±1.27 | 2.988±1.27 | 0.100±0.10 | 0.508±0.03 | 0.983±0.06 | 0.667±0.00 | 0.291±0.26 | 0.467±0.00 | — | 0.904±0.10 | 0.904±0.10 | 2.206±0.27 | 2165.500±287.42 | 13762.033±6901.49 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.6651
# Experiment Report — E02_rag_topk_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, retrieval_top_k=1) | zai-org/GLM-5.3-Flash | 0.694±0.06 | 7.300±0.17 | 0.217±0.06 | 0.347±0.11 | -0.003±0.01 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.900±0.00 | 1.000±0.00 | 1.000±0.00 | 2.904±0.27 | 773.444±70.19 | 0.000±0.00 |
| arm_1 (llm_temperature=0.7, retrieval_top_k=3) | zai-org/GLM-5.3-Flash | 0.667±0.06 | 7.318±0.18 | 0.242±0.12 | 0.333±0.06 | -0.005±0.00 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.022±0.25 | 953.222±82.95 | 0.000±0.00 |
| arm_2 (llm_temperature=0.7, retrieval_top_k=8) | zai-org/GLM-5.3-Flash | 0.653±0.08 | 7.302±0.15 | 0.235±0.11 | 0.361±0.11 | -0.006±0.00 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.700±0.00 | 1.000±0.00 | 1.000±0.00 | 3.111±0.40 | 973.111±121.41 | 0.000±0.00 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.058
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.097
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.0283
# Experiment Report — E02_rag_topk_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | rag_faithfulness_judge | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.7, retrieval_top_k=1) | zai-org/GLM-5.3-Flash | 0.986±0.04 | 5.274±1.25 | 3.855±0.44 | 0.014±0.04 | 0.534±0.03 | 0.972±0.08 | 0.667±0.00 | 0.009±0.02 | 0.497±0.00 | — | 0.986±0.04 | 0.986±0.04 | 2.032±0.09 | 1454.000±101.27 | 4131.000±306.93 |
| arm_1 (llm_temperature=0.7, retrieval_top_k=3) | zai-org/GLM-5.3-Flash | 0.986±0.04 | 4.986±1.06 | 3.972±0.14 | 0.014±0.04 | 0.506±0.03 | 1.000±0.00 | 0.667±0.00 | 0.008±0.02 | 0.489±0.00 | — | 0.986±0.04 | 0.986±0.04 | 2.032±0.09 | 2107.444±184.98 | 5529.444±929.08 |
| arm_2 (llm_temperature=0.7, retrieval_top_k=8) | zai-org/GLM-5.3-Flash | 0.875±0.12 | 4.239±1.04 | 3.772±0.41 | 0.139±0.15 | 0.502±0.02 | 1.000±0.00 | 0.648±0.05 | 0.047±0.03 | 0.462±0.00 | — | 0.875±0.12 | 0.875±0.12 | 2.334±0.37 | 4210.667±668.91 | 7015.000±1443.93 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.3414
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.4713
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.4381
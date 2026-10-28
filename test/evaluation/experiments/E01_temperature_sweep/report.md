# Experiment Report — E01_temperature_sweep

Total runs: 27

| arm | model | approval_rate | quality_mean | quality_std | attempts_per_item | pairwise_sim_mean | topic_coverage | bloom_coverage | rag_faithfulness | rag_retrieval_score | rag_faithfulness_judge | bloom_accuracy | difficulty_accuracy | calls_per_item | tokens_per_item | latency_mean_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arm_0 (llm_temperature=0.3) | zai-org/GLM-5.3-Flash | 1.000±0.00 | 5.619±1.38 | 3.723±0.53 | 0.000±0.00 | 0.502±0.02 | 1.000±0.00 | 0.667±0.00 | 0.000±0.00 | 0.489±0.00 | — | 1.000±0.00 | 1.000±0.00 | 2.000±0.00 | 1995.333±137.01 | 4280.667±490.93 |
| arm_1 (llm_temperature=0.7) | zai-org/GLM-5.3-Flash | 0.944±0.09 | 5.114±0.79 | 3.932±0.30 | 0.069±0.12 | 0.502±0.01 | 1.000±0.00 | 0.667±0.00 | 0.024±0.03 | 0.489±0.00 | — | 0.944±0.09 | 0.944±0.09 | 2.138±0.22 | 2156.111±273.66 | 4534.000±349.14 |
| arm_2 (llm_temperature=1.0) | zai-org/GLM-5.3-Flash | 0.917±0.08 | 5.839±1.11 | 3.836±0.52 | 0.083±0.08 | 0.513±0.02 | 0.972±0.08 | 0.667±0.00 | 0.034±0.03 | 0.488±0.00 | — | 0.917±0.08 | 0.917±0.08 | 2.199±0.20 | 2249.111±233.85 | 4918.000±553.10 |

## SOTA metrics

- **arm_0**: self_consistency=1.0, robustness between-subject σ=0.3589
- **arm_1**: self_consistency=1.0, robustness between-subject σ=0.1104
- **arm_2**: self_consistency=1.0, robustness between-subject σ=0.1528
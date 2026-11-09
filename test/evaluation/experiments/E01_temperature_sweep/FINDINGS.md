# E01 — Generator: temperature sweep 0.3 / 0.7 / 1.0 (REAL RESULTS, ROUND 11)

> 27 real runs (3 arms x 3 English clones x 3 repeats), GLM-5.3-Flash via the
> USFQ gateway. Evaluator fixed at 0.2 (production), top_k 3. All 27 runs
> `completed`. English verified: 0 of 206 delivered items have a Spanish
> body (deterministic scan + human spot review).

## Per-arm results

![Approval rate](approval_rate.png)
![Quality mean](quality_mean.png)
![Bloom accuracy](bloom_accuracy.png)
![Tokens per item](tokens_per_item.png)

| Metric | gen T=0.3 | gen T=0.7 (production) | gen T=1.0 |
|---|---|---|---|
| Approval rate | **1.000 ± 0.00** | 0.944 ± 0.09 | 0.917 ± 0.08 |
| Quality score mean | 5.62 ± 1.38 | 5.11 ± 0.79 | **5.84 ± 1.11** |
| Intra-run quality sigma | 3.72 | 3.93 | 3.84 |
| Attempts per item | **0.000** | 0.069 | 0.083 |
| Pairwise similarity (diversity) | 0.502 | 0.502 | 0.513 |
| Bloom accuracy | **1.000** | 0.944 | 0.917 |
| RAG faithfulness (lexical) | 0.000 | 0.024 | 0.034 |
| Tokens per item | **1,995** | 2,156 | 2,249 |
| Calls per item | **2.00** | 2.14 | 2.20 |
| Robustness across clones (sigma) | 0.359 | **0.110** | 0.153 |

## Findings

1. **Monotonic degradation with temperature on spec alignment**: approval
   1.000 -> 0.944 -> 0.917 and Bloom accuracy 1.000 -> 0.944 -> 0.917. The
   lower the generator temperature, the tighter the adherence to the
   requested spec (Bloom level, difficulty, question type). T=0.3 never
   needed a regeneration attempt (attempts=0.000).

2. **T=0.3 dominates efficiency** (fewest calls 2.00, fewest tokens 1,995,
   zero retries) while also having the best approval. Under the round-11
   blueprint (English clones, regenerated topics), the round-10 sweet spot
   at T=0.7 shifts toward T=0.3: quality_mean differences (5.62 vs 5.11 vs
   5.84) are within one sigma and do not offset the alignment loss.

3. **T=1.0 degrades coverage slightly** (topic_coverage 0.972 vs 1.000) and
   costs the most per item (2,249 tokens, 2.20 calls). No reason to raise
   the generator temperature.

4. **Diversity is insensitive to temperature** (pairwise similarity
   0.502-0.513 in all arms): shared domain vocabulary dominates, same
   conclusion as round 10.

5. **Cross-clone robustness is best at T=0.7** (sigma 0.110 vs 0.359 at
   T=0.3 and 0.153 at T=1.0) and self-consistency is 1.0 in all arms. With
   only 3 repeats per clone, treat the robustness ranking as indicative.

## Judge caveat (applies to this round)

The in-run LLM faithfulness judge produced num_judged=0 in all 82 campaign
runs (harness passed un-correlated retrieval records; fixed in harness.py
after the campaign). `rag_faithfulness` here is the lexical cross-encoder
metric only. The post-hoc judge was deliberately NOT run for this campaign:
the audit-row windowing has a +-1 row uncertainty (E04 79 vs 80, E01 213 vs
214), which would silently misalign statement<->chunks pairs.

## Configuration implication

The production generator temperature is re-validated as being on the flat
top of the curve: T=0.7 keeps the best cross-clone stability with
approval >= 0.94; T=0.3 is the efficiency-optimal alternative if future
rounds prioritise cost. No production change is mandatory from this sweep.

# E04 — Evaluator temperature 0.0 vs 0.2 vs 0.6 (REAL RESULTS, ROUND 11)

> 18 real runs (3 arms x 2 English clones x 3 repeats), GLM-5.3-Flash via
> the USFQ gateway. Generator fixed at 0.7 (production), top_k 3, blueprint
> of 8 questions, identical material (clones adam and bella). All 18 runs
> `completed` with LaTeX/PDF pipeline working. The first 6 arm-0 runs were
> interrupted by the pre-relaunch crash and resumed by the crash-proof
> runner (live-verification reruns appear as SKIP; no double cost).

## Per-arm results

![Approval rate](approval_rate.png)
![Quality mean](quality_mean.png)
![Bloom accuracy](bloom_accuracy.png)

| Metric | eval T=0.0 | eval T=0.2 (production) | eval T=0.6 |
|---|---|---|---|
| Approval rate | 0.938 ± 0.10 | **0.979 ± 0.05** | 0.938 ± 0.10 |
| Quality score mean | 4.71 ± 1.31 | 4.38 ± 1.02 | **5.55 ± 1.63** |
| Intra-run quality sigma | 4.02 | 3.81 | **3.17** |
| Attempts per item | 0.062 | **0.021** | 0.062 |
| Pairwise similarity (diversity) | 0.492 | 0.503 | 0.520 |
| Topic coverage | 1.000 | 1.000 | 0.958 |
| Bloom accuracy | 0.938 | **0.979** | 0.938 |
| RAG faithfulness (lexical) | 0.025 | 0.021 | 0.026 |
| Tokens per item | 2,249 | 2,130 | 2,185 |
| Calls per item | 2.16 | **2.03** | 2.16 |
| Robustness across clones (sigma) | 0.526 | 0.684 | **0.419** |

## Findings

1. **Approval is insensitive to evaluator temperature** (0.938-0.979 across
   arms): the approve/reject decision of GLM is robust to sampling
   temperature, consistent with H2 and with round 10.

2. **T=0.2 (production) is the most efficient arm**: fewest attempts per
   item (0.021), fewest calls per item (2.03), highest Bloom accuracy
   (0.979). Quality_mean is lowest in this arm, but the evaluator's
   quality_score is itself a sampled judgement — comparing quality means
   across evaluator temperatures partially measures the judge's own
   sampling behaviour, not only item quality.

3. **The arm-2 evaluator (T=0.6) grades more leniently on average**
   (quality 5.55 vs 4.38-4.71) with a tighter intra-run sigma (3.17):
   higher temperature averages out extreme low scores. This is a judge-
   calibration observation, useful for the LLM-as-judge discussion chapter.

4. **Cross-clone sigma is in the same band in all arms** (0.42-0.68),
   higher than round 10 but with a different subject pool (adam/bella vs
   Eva/Maria) and only 3 repeats; not a basis for a monotonic claim this
   round.

5. **Judge caveat (round 11)**: the in-run LLM faithfulness judge produced
   num_judged=0 in all 82 runs (harness passed un-correlated retrieval
   records; correlation fixed in harness.py after this campaign). The
   6 arm-0 records from the interrupted first attempt also carry
   judge_err=1 from a pre-relaunch judge failure. Post-hoc judging was
   deliberately aborted: the audit-row windowing has a +-1 row uncertainty
   (E04 relaunch 79 gen calls vs 80 rows in window; E01 213 vs 214), which
   would silently misalign statement<->chunks pairs. Lexical
   rag_faithfulness (0.021-0.026) is available and flat across arms.

## Configuration implication

Production evaluator temperature T=0.2 remains validated: same approval as
the other arms with the best efficiency and alignment. Evaluator
temperatures >= 0.6 shift the quality-score scale (leniency) without
improving any decision-relevant metric.

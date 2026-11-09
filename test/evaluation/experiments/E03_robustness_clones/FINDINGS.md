# E03 — Robustness across clones (REAL RESULTS, ROUND 11)

> 10 real runs (1 arm x 5 English clones x 2 repeats), GLM-5.3-Flash via the
> USFQ gateway. Config identical in all runs (generator 0.7, evaluator 0.2,
> top_k 3); identical material; only the subject name changes (Applied
> Economics - adam/bella/carlos/diana/esteban). All 10 runs `completed`.

## Results

![Approval rate](approval_rate.png)
![Quality mean](quality_mean.png)
![Bloom accuracy](bloom_accuracy.png)

| Metric | Mean ± sigma (10 runs) |
|---|---|
| Approval rate | 0.912 ± 0.10 |
| Quality score mean | 4.55 ± 1.63 |
| Pairwise similarity (diversity) | 0.502 ± 0.01 |
| RAG faithfulness (lexical) | 0.046 ± 0.05 |
| RAG retrieval score | 0.489 ± 0.00 |
| Bloom accuracy | 0.912 ± 0.10 |
| Calls per item | 2.22 ± 0.26 |
| Tokens per item | 2,232 ± 300 |

## Cross-clone robustness (same config, identical material)

Quality mean per clone: adam 5.65, bella 2.85, carlos 4.54, diana 3.40,
esteban 6.33. Between-clone sigma = **1.311** — above the H5 threshold
(1.0) that round 10 accepted with 4 repeats per clone.

## Findings

1. **H5 NOT confirmed at 2 repeats per clone in the English setup**:
   sigma(between clones) = 1.311 > 1.0. With only 2 runs per clone, each
   clone mean rests on 16 items and the sigma estimate itself is noisy
   (round 10 saw the same estimator move 1.051 -> 0.665 when repeats went
   2 -> 4). bella (2.85) and esteban (6.33) are the extremes.

2. **Approval remains high and stable** (0.912 ± 0.10): the pipeline
   approves ~7.3 of 8 items per run consistently across 5 different
   "professors" — the practical robustness signal that matters for the MVP.

3. **Quality variance is generator-driven, not retrieval-driven**:
   retrieval score is flat (0.489 ± 0.00) while quality mean swings 2.85-6.33
   between clones. The stochastic sampler at T=0.7, not the material,
   explains the spread.

4. **Diversity stable** (pairwise 0.502, far below the 0.82 duplicate
   threshold): the anti-duplicate mechanism stays dormant in normal
   conditions (validates H3 in the English setup).

5. **Cost consistent**: 2.22 calls/item and ~2,232 tokens/item with small
   dispersion.

## Judge caveat

Same round-11 caveat as E01/E02: in-run LLM judge num_judged=0 (fixed in
harness.py post-campaign); post-hoc judging aborted due to +-1 row
windowing uncertainty. Only the lexical faithfulness metric is available.

## Recommendation

If the thesis claims pipeline stability (H5), extend E03 to >= 4 repeats
per clone (20 runs, ~35 min) before defending the sigma estimate; 2 repeats
per clone is not enough for a between-group sigma with 5 groups.

"""Agent SOTA metrics: self-consistency, pass@k, robustness.

Computed ACROSS runs (not within one run), by the aggregator:
  - self_consistency: share of specs approved in ALL k repeats of a config.
  - pass@k: unbiased estimator (Chen et al., 2021) that at least one of k
    attempts is approved.
  - robustness: cross-clone (same material, different subject names) and
    cross-run variance of each metric family.
"""
from __future__ import annotations

from math import comb
from statistics import pstdev, mean
from typing import Any


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k estimator (Chen et al., 2021).

    ``n`` total attempts, ``c`` successful ones. Returns P(>=1 success in k).
    """
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def self_consistency(spec_outcomes: list[bool]) -> float:
    """Share of specs approved in ALL of their repeats.

    ``spec_outcomes``: one bool per (spec, repeat) — True if the spec's item
    was approved in that repeat.
    """
    if not spec_outcomes:
        return 0.0
    return sum(1 for o in spec_outcomes if o) / len(spec_outcomes)


def robustness(values_by_group: dict[str, list[float]]) -> dict[str, Any]:
    """Cross-group variance summary for one metric.

    ``values_by_group``: e.g. {clone_name: [quality_score per run]}.
    Returns per-group mean/std and the global between-group spread.
    """
    group_stats = {}
    for group, values in values_by_group.items():
        if values:
            group_stats[group] = {
                "mean": round(mean(values), 4),
                "std": round(pstdev(values), 4) if len(values) > 1 else 0.0,
                "n": len(values),
            }
    group_means = [s["mean"] for s in group_stats.values()]
    return {
        "groups": group_stats,
        "between_group_mean": round(mean(group_means), 4) if group_means else None,
        "between_group_std": round(pstdev(group_means), 4) if len(group_means) > 1 else None,
    }

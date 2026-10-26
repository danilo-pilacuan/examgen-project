"""Quality metrics: approval rate, quality score, retries, rejection reasons.

Data source: the pipeline result state (approved_items, rejection_log) plus
the per-item evaluations collected by the harness.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def quality_metrics(state: dict[str, Any], item_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes the quality family for one run.

    ``item_records``: one entry per spec attempt with keys
    ``approved`` (bool), ``quality_score`` (float), ``retry_count`` (int),
    ``rejection_reason`` (str|None).
    """
    approved_items = state.get("approved_items", [])
    rejection_log = state.get("rejection_log", [])
    total_specs = len(item_records) or len(approved_items) + len(rejection_log)

    scores = [r["quality_score"] for r in item_records if r.get("quality_score") is not None]
    approved_scores = [r["quality_score"] for r in item_records if r.get("approved") and r.get("quality_score") is not None]
    retries = [r.get("retry_count", 0) for r in item_records]

    reasons = Counter(
        r.get("rejection_reason") or "unspecified"
        for r in item_records
        if not r.get("approved")
    )

    return {
        "total_specs": total_specs,
        "approved_count": len(approved_items),
        "approval_rate": round(len(approved_items) / total_specs, 4) if total_specs else None,
        "quality_score_mean": _round(_mean(scores)),
        "quality_score_std": _round(_std(scores)),
        "quality_score_mean_approved": _round(_mean(approved_scores)),
        "mean_attempts_per_approved_item": _round(_mean(retries)),
        "rejection_reasons": dict(reasons),
    }


def _round(value: float | None, digits: int = 4) -> float | None:
    return round(value, digits) if value is not None else None


def _mean(xs: list[float]) -> float | None:
    if not xs:
        return None
    return sum(xs) / len(xs)


def _std(xs: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5

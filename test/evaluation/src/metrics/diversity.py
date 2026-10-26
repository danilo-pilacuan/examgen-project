"""Diversity metrics: pairwise semantic similarity and topic/Bloom coverage.

Similarity uses the configured embedder (real bge-m3 service or stub) so the
metric behaves identically in dry-run and real mode.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def diversity_metrics(
    items: list[Any],
    blueprint_topics: list[str],
    embedder: Any,
) -> dict[str, Any]:
    """Computes the diversity family for one run's approved items.

    ``items``: list of GeneratedItem (pydantic) approved in the run.
    """
    if len(items) < 2:
        return {
            "pairwise_similarity_mean": None,
            "pairwise_similarity_max": None,
            "topic_coverage": None,
            "bloom_coverage": None,
            "num_items": len(items),
        }

    vectors = embedder.embed([it.statement for it in items])
    sims = [
        _cosine(vectors[i], vectors[j])
        for i in range(len(items))
        for j in range(i + 1, len(items))
    ]
    topic_counts = Counter(it.topic for it in items)
    bloom_counts = Counter(it.bloom_level.value for it in items)

    return {
        "pairwise_similarity_mean": round(sum(sims) / len(sims), 4),
        "pairwise_similarity_max": round(max(sims), 4),
        "topic_coverage": round(len(topic_counts) / max(len(blueprint_topics), 1), 4),
        "bloom_coverage": round(len(bloom_counts) / 6.0, 4),
        "topic_counts": dict(topic_counts),
        "bloom_counts": dict(bloom_counts),
        "num_items": len(items),
    }


def _cosine(a: list[float], b: list[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    da = sum(x * x for x in a) ** 0.5
    db = sum(y * y for y in b) ** 0.5
    return num / (da * db) if da and db else 0.0

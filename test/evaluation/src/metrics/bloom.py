"""Bloom/difficulty alignment metrics: spec vs generated item agreement.

The generator receives an explicit spec (topic, bloom, difficulty, type).
This module measures how faithfully the produced item matches the spec —
an implicit classification accuracy, plus a confusion matrix for the thesis.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def bloom_metrics(item_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes the alignment family for one run.

    ``item_records``: one entry per generated attempt with keys
    ``spec_bloom``, ``item_bloom``, ``spec_difficulty``, ``item_difficulty``,
    ``spec_type``, ``item_type`` (all lowercase enum values or None when the
    item could not be generated).
    """
    records = [r for r in item_records if r.get("item_bloom") is not None]
    if not records:
        return {
            "bloom_accuracy": None,
            "difficulty_accuracy": None,
            "type_accuracy": None,
            "bloom_confusion": {},
            "num_items": len(records),
        }

    bloom_ok = sum(1 for r in records if r["item_bloom"] == r["spec_bloom"])
    diff_ok = sum(1 for r in records if r.get("item_difficulty") == r.get("spec_difficulty"))
    type_ok = sum(1 for r in records if r.get("item_type") == r.get("spec_type"))

    confusion = Counter(f"{r['spec_bloom']}->{r['item_bloom']}" for r in records)

    return {
        "bloom_accuracy": round(bloom_ok / len(records), 4),
        "difficulty_accuracy": round(diff_ok / len(records), 4),
        "type_accuracy": round(type_ok / len(records), 4),
        "bloom_confusion": dict(confusion),
        "num_items": len(records),
    }

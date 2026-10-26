"""RAG quality metrics: retrieval scores and lexical faithfulness.

Faithfulness is approximated by token overlap between each generated
statement and the chunks retrieved for its spec (the context the generator
actually saw). A LLM-judge version can replace it in a later phase.
"""
from __future__ import annotations

import re
from typing import Any

_TOKEN_RE = re.compile(r"[a-záéíóúñü]{3,}", re.IGNORECASE)


def rag_metrics(retrieval_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes the RAG family for one run.

    ``retrieval_records``: one entry per generated spec with keys
    ``chunk_scores`` (list[float]), ``statement`` (str),
    ``chunks`` (list[str]).
    """
    if not retrieval_records:
        return {
            "retrieval_score_mean": None,
            "chunks_per_spec_mean": None,
            "faithfulness_mean": None,
            "specs_with_context": 0,
            "num_records": 0,
        }

    all_scores: list[float] = []
    chunks_counts: list[int] = []
    faithfulness: list[float] = []
    with_context = 0

    for rec in retrieval_records:
        scores = rec.get("chunk_scores") or []
        all_scores.extend(scores)
        chunks_counts.append(len(rec.get("chunks") or []))
        if rec.get("chunks"):
            with_context += 1
            faithfulness.append(_lexical_faithfulness(rec.get("statement") or "", rec["chunks"]))

    return {
        "retrieval_score_mean": round(sum(all_scores) / len(all_scores), 4) if all_scores else None,
        "chunks_per_spec_mean": round(sum(chunks_counts) / len(chunks_counts), 4) if chunks_counts else None,
        "faithfulness_mean": round(sum(faithfulness) / len(faithfulness), 4) if faithfulness else None,
        "specs_with_context": with_context,
        "num_records": len(retrieval_records),
    }


def _lexical_faithfulness(statement: str, chunks: list[str]) -> float:
    """Fraction of the statement's distinctive tokens present in the chunks."""
    st_tokens = {t.lower() for t in _TOKEN_RE.findall(statement)}
    if not st_tokens:
        return 0.0
    chunk_tokens: set[str] = set()
    for c in chunks:
        chunk_tokens.update(t.lower() for t in _TOKEN_RE.findall(c))
    covered = st_tokens & chunk_tokens
    return len(covered) / len(st_tokens)

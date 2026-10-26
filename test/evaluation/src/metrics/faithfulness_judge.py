"""LLM-as-judge faithfulness metric for RAG quality.

Replaces the lexical-overlap approximation (metrics/rag.py) with a judged
score: an LLM reads the generated statement and the retrieved chunks, and
scores 0-10 how much of the statement's factual content is supported by the
chunks. Aggregated as ``rag.faithfulness_judge_mean`` per run.

The judge runs post-hoc on the audit trail (generator prompts + statements),
so it never interferes with the pipeline under evaluation. Judge calls go
through the same model registry (``models.yaml``), so the judge can be the
same model as the generator (self-judge) or a different one (cross-judge).
"""
from __future__ import annotations

import json
import re
from typing import Any

from test.evaluation.src.models_registry import ModelProfile, get_profile

_JUDGE_PROMPT = """You are a rigorous evaluator of RAG faithfulness for exam questions.

You will receive:
  1. A generated exam question (the "statement").
  2. The list of source chunks that were retrieved as context when the question was generated.

Task: score FAITHFULNESS from 0 to 10, where:
  - 10  = every factual claim in the statement is directly supported by the chunks.
  - 5-7 = most claims are supported; some minor extrapolation beyond the chunks.
  - 1-4 = the statement is largely generic or contradicts / goes well beyond the chunks.
  - 0   = no relationship with the chunks.

Judge ONLY factual support, not pedagogical quality or grammar.

Respond with ONLY a JSON object: {{"faithfulness_score": <0-10>, "rationale": "<one short sentence>"}}

--- GENERATED STATEMENT ---
{statement}

--- RETRIEVED CHUNKS ---
{chunks}
"""

_SCORE_RE = re.compile(r"faithfulness_score\"?\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)


def build_judge_prompt(statement: str, chunks: list[str]) -> str:
    chunk_block = "\n\n".join(
        f"[Chunk {i}] {c[:1200]}" for i, c in enumerate(chunks, start=1)
    ) or "(no chunks retrieved)"
    return _JUDGE_PROMPT.format(statement=statement[:3000], chunks=chunk_block[:6000])


def parse_judge_answer(raw: str) -> float | None:
    """Extracts the faithfulness score from the judge's raw answer."""
    if not raw:
        return None
    try:
        data = json.loads(raw)
        score = data.get("faithfulness_score")
        if isinstance(score, (int, float)):
            return float(score)
    except json.JSONDecodeError:
        pass
    m = _SCORE_RE.search(raw)
    return float(m.group(1)) if m else None


def judge_faithfulness(
    records: list[dict[str, Any]],
    judge_profile_name: str = "glm-flash-default",
    temperature: float = 0.0,
) -> dict[str, Any]:
    """Judges faithfulness for each retrieval record.

    ``records``: same shape as rag_metrics input — keys ``statement``,
    ``chunks`` (list[str]). Records without statement/chunks are skipped.

    Returns the judged-faithfulness family dict:
      ``faithfulness_judge_mean`` (0-1, normalized /10), ``judge_profile``,
      ``num_judged``, ``judgement_errors``.
    """
    profile: ModelProfile = get_profile(judge_profile_name)
    from openai import OpenAI

    client = OpenAI(base_url=profile.base_url, api_key=profile.api_key)

    scores: list[float] = []
    errors = 0
    judged: list[dict[str, Any]] = []
    for rec in records:
        statement = (rec.get("statement") or "").strip()
        chunks = [c for c in (rec.get("chunks") or []) if c]
        if not statement or not chunks:
            continue
        prompt = build_judge_prompt(statement, chunks)
        try:
            resp = client.chat.completions.create(
                model=profile.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                # GLM-5.3-Flash consumes reasoning tokens even with
                # reasoning_effort=none; 300 starved the JSON answer.
                max_tokens=2000,
                reasoning_effort="none",
            )
            raw = resp.choices[0].message.content or ""
        except Exception:
            errors += 1
            continue
        score = parse_judge_answer(raw)
        if score is None:
            errors += 1
            continue
        scores.append(score)
        judged.append({
            "statement": statement[:200],
            "score_0_10": score,
            "normalized": round(score / 10.0, 4),
        })

    return {
        "faithfulness_judge_mean": round(sum(scores) / (10.0 * len(scores)), 4) if scores else None,
        "faithfulness_judge_std": _std(scores) if len(scores) > 1 else None,
        "judge_profile": judge_profile_name,
        "judge_model": profile.model,
        "num_judged": len(scores),
        "judgement_errors": errors,
        "judgements": judged,
    }


def _std(xs: list[float]) -> float:
    m = sum(xs) / len(xs)
    return round((sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5, 4)

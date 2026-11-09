"""Cost/efficiency metrics: LLM calls, latency and token estimates.

Token accounting: the USFQ gateway does not return per-call usage, so the
suite estimates tokens as chars/4 (standard heuristic for English/Spanish
mixed text). When a provider does return usage, add it in the harness and
the exact values take precedence.
"""
from __future__ import annotations

from typing import Any

CHARS_PER_TOKEN = 4.0


def cost_metrics(
    llm_calls: list[dict[str, Any]],
    approved_count: int,
) -> dict[str, Any]:
    """Computes the cost family for one run.

    ``llm_calls``: one entry per LLM invocation with keys
    ``node`` ('generator'|'evaluator'|'chat'|...), ``latency_ms`` (int|None),
    ``prompt_chars`` (int), ``answer_chars`` (int),
    ``usage_prompt_tokens``/``usage_completion_tokens`` (int|None when the
    provider reports real usage).
    """
    if not llm_calls:
        return {
            "total_llm_calls": 0,
            "calls_per_approved_item": None,
            "latency_mean_ms": None,
            "tokens_prompt_est": None,
            "tokens_completion_est": None,
            "tokens_per_item_est": None,
            "latency_by_node_ms": {},
        }

    latencies = [c["latency_ms"] for c in llm_calls if c.get("latency_ms") is not None]
    by_node: dict[str, dict[str, Any]] = {}
    for c in llm_calls:
        node = c.get("node") or "unknown"
        agg = by_node.setdefault(node, {"count": 0, "latency_ms": []})
        agg["count"] += 1
        if c.get("latency_ms") is not None:
            agg["latency_ms"].append(c["latency_ms"])

    # Real usage takes precedence when present; otherwise chars/4 estimate.
    usage_prompt = [c["usage_prompt_tokens"] for c in llm_calls if c.get("usage_prompt_tokens")]
    usage_completion = [c["usage_completion_tokens"] for c in llm_calls if c.get("usage_completion_tokens")]
    if usage_prompt:
        tokens_prompt = sum(usage_prompt)
    else:
        tokens_prompt = int(sum(c.get("prompt_chars", 0) for c in llm_calls) / CHARS_PER_TOKEN)
    if usage_completion:
        tokens_completion = sum(usage_completion)
    else:
        tokens_completion = int(sum(c.get("answer_chars", 0) for c in llm_calls) / CHARS_PER_TOKEN)

    return {
        "total_llm_calls": len(llm_calls),
        "calls_per_approved_item": round(len(llm_calls) / approved_count, 4) if approved_count else None,
        "latency_mean_ms": int(sum(latencies) / len(latencies)) if latencies else None,
        "tokens_prompt_est": tokens_prompt,
        "tokens_completion_est": tokens_completion,
        "tokens_per_item_est": int((tokens_prompt + tokens_completion) / approved_count) if approved_count else None,
        "latency_by_node_ms": {
            node: {
                "count": agg["count"],
                "mean_ms": int(sum(agg["latency_ms"]) / len(agg["latency_ms"])) if agg["latency_ms"] else None,
            }
            for node, agg in by_node.items()
        },
    }

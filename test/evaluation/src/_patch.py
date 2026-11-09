"""Runtime wiring between the evaluation harness and the pipeline.

Dry-run mode: monkey-patches the pipeline LLM singletons
(``agents_backend.shared.llm.generator_llm`` / ``evaluator_llm``) with the
deterministic stub, and ``retrieve_chunks`` with a stub retrieval backed by
the StubEmbedder — production code stays untouched.

Real mode: points the shared LLM factory settings at the arm's model profile
(base_url, model, api key) and applies the arm's hyperparameter overrides to
``core.config.settings`` for the duration of the run.
"""
from __future__ import annotations

from typing import Any

from test.evaluation.src.models_registry import ModelProfile


class _StubStructured:
    """Adapter: pipeline calls ``llm.with_structured_output(schema).invoke(prompt)``."""

    def __init__(self, stub: Any):
        self._stub = stub

    def with_structured_output(self, schema: type) -> Any:
        fn = self._stub.with_structured_output(schema)

        class _Invoker:
            def __init__(self, fn: Any, collector: "TelemetryCollector"):
                self._fn = fn
                self._collector = collector

            def invoke(self, prompt: str) -> Any:
                import time

                started = time.perf_counter()
                result = self._fn(prompt)
                latency = int((time.perf_counter() - started) * 1000)
                node = "generator" if schema.__name__ == "GeneratedItem" else "evaluator"
                self._collector.record(node, latency, len(prompt), len(str(result.model_dump_json())))
                return result

        return _Invoker(fn, _ACTIVE_COLLECTOR)


class TelemetryCollector:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def record(self, node: str, latency_ms: int, prompt_chars: int, answer_chars: int) -> None:
        self.calls.append({
            "node": node,
            "latency_ms": latency_ms,
            "prompt_chars": prompt_chars,
            "answer_chars": answer_chars,
            "usage_prompt_tokens": None,
            "usage_completion_tokens": None,
        })


_ACTIVE_COLLECTOR = TelemetryCollector()


class _StubRetrieval:
    """Stub retrieval: fake chunks derived deterministically from the query."""

    def __init__(self) -> None:
        self.records: list[dict] = []

    def retrieve_chunks(self, query: str, subject_id: str, top_k: int = 4, min_score: float = 0.15, db: Any = None) -> list[dict]:
        import hashlib

        seed = int(hashlib.sha256(query.encode()).hexdigest()[:8], 16)
        out = []
        for i in range(min(top_k, 3)):
            h = hashlib.sha256(f"{seed}:{i}".encode()).hexdigest()
            words = [h[j:j + 5] for j in range(0, 20, 5)]
            score = max(0.2, 0.9 - i * 0.2)
            out.append({
                "content": f"[stub-context] Topic '{query}' — reference fragment {i + 1}: {' '.join(words)} economics market study financial flows analysis pricing.",
                "score": round(score, 3),
            })
        result = [c for c in out if c["score"] >= min_score]
        self.records.append({"query": query, "chunks": result, "chunk_scores": [c["score"] for c in result]})
        return result

    def format_context(self, chunks: list[dict], max_chars_per_chunk: int = 1200) -> str:
        parts = []
        for i, c in enumerate(chunks, start=1):
            parts.append(f"[Chunk {i} (score {c['score']:.2f})]\n{c['content'][:max_chars_per_chunk]}")
        return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Activation
# ---------------------------------------------------------------------------
_ACTIVE_RETRIEVAL: _StubRetrieval | None = None


def activate_stubs(stub_llm: Any) -> None:
    """Patches the pipeline with deterministic stubs (dry-run)."""
    global _ACTIVE_RETRIEVAL
    import agents_backend.exam_pipeline.nodes as nodes
    import agents_backend.shared.llm as shared_llm
    import agents_backend.shared.retrieval as retrieval

    stub_adapter = _StubStructured(stub_llm)
    _ACTIVE_RETRIEVAL = _StubRetrieval()

    nodes.generator_llm = stub_adapter
    nodes.evaluator_llm = stub_adapter
    # Disable the raw-audit DB writes during dry-runs (no infra dependency).
    nodes.record_llm_response = lambda **kwargs: None
    # nodes.py did `from ...retrieval import retrieve_chunks` at module load,
    # so patch its namespace directly (not just the source module).
    nodes.retrieve_chunks = _ACTIVE_RETRIEVAL.retrieve_chunks
    nodes.format_context = _ACTIVE_RETRIEVAL.format_context
    retrieval.retrieve_chunks = _ACTIVE_RETRIEVAL.retrieve_chunks
    retrieval.format_context = _ACTIVE_RETRIEVAL.format_context
    shared_llm.generator_llm = stub_adapter
    shared_llm.evaluator_llm = stub_adapter


def get_retrieval_records() -> list[dict]:
    """Retrieval traces of the last dry-run, with the statement attached by
    the harness (query→statement correlation via order of generation)."""
    if _ACTIVE_RETRIEVAL is None:
        return []
    return [
        {
            "chunk_scores": rec["chunk_scores"],
            "chunks": [c["content"] for c in rec["chunks"]],
            "statement": "",  # filled by harness via correlate_statements
        }
        for rec in _ACTIVE_RETRIEVAL.records
    ]


def reset_retrieval_records() -> None:
    global _ACTIVE_RETRIEVAL
    _ACTIVE_RETRIEVAL = None


def activate_real(profile: ModelProfile, overrides: dict[str, Any]) -> None:
    """Points production settings at the arm's profile + overrides (real run).

    Restores previous values on context exit via :func:`deactivate_real`.
    """
    import agents_backend.exam_pipeline.nodes as nodes
    import agents_backend.shared.retrieval as retrieval
    from core import config as core_config

    s = core_config.settings
    if profile.base_url:
        s.llm_base_url = profile.base_url
    s.llm_model = profile.model
    if profile.api_key:
        s.openai_api_key = profile.api_key

    from core.domain import llm_log as llm_log_module

    for key, value in overrides.items():
        if hasattr(s, key):
            setattr(s, key, value)

    # Rebuild the node-level LLM singletons so they pick up the new settings.
    from agents_backend.shared.llm import get_llm

    nodes.generator_llm = get_llm(s.llm_reasoning_generator)
    nodes.evaluator_llm = get_llm(
        s.llm_reasoning_evaluator,
        temperature=s.llm_temperature_evaluator,
    )


def get_collector() -> TelemetryCollector:
    return _ACTIVE_COLLECTOR


def reset_collector() -> None:
    global _ACTIVE_COLLECTOR
    _ACTIVE_COLLECTOR = TelemetryCollector()

"""Deterministic offline stubs for dry-run validation of the harness.

The stub LLM mimics the contract used by the pipeline:
  - ``with_structured_output(schema)`` returns a valid pydantic instance.
  - Deterministic per (spec, temperature) so repeated dry-runs are stable.
The stub embedder mirrors ``core.infrastructure.embeddings.embedder``.
"""
from __future__ import annotations

import hashlib
import math
import random
import re
from typing import Any

from core.domain.schemas.exam import (
    AnswerOption,
    GeneratedItem,
    QuestionType,
)


def _seed(*parts: str) -> int:
    blob = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(blob.encode("utf-8")).hexdigest()[:8], 16)


class StubStructuredLLM:
    """Deterministic structured-output LLM stub.

    ``with_structured_output(GeneratedItem)`` builds a plausible item from
    the spec encoded in the prompt; ``with_structured_output(EvaluationResult)``
    approves with a quality score derived from the item text.
    """

    def __init__(self, temperature: float = 0.7, label: str = "stub"):
        self.temperature = temperature
        self.label = label

    def with_structured_output(self, schema: type) -> Any:
        if schema.__name__ == "GeneratedItem":
            return self._generate_item
        if schema.__name__ == "EvaluationResult":
            return self._evaluate_item
        raise NotImplementedError(f"Stub has no behavior for schema {schema.__name__}")

    # --- generator behavior -------------------------------------------------
    def _generate_item(self, prompt: str) -> GeneratedItem:
        spec = _parse_spec(prompt)
        rng = random.Random(_seed(spec["topic"], spec["bloom"], spec["difficulty"], spec["qtype"], self.label))
        qtype = QuestionType(spec["qtype"])
        topic = spec["topic"]
        bloom = spec["bloom"]

        if qtype == QuestionType.TRUE_FALSE:
            correct = rng.random() < 0.5
            options = [
                AnswerOption(text="True", is_correct=correct),
                AnswerOption(text="False", is_correct=not correct),
            ]
            statement = f"[stub/{self.label}] In the context of {topic}, the following statement is correct: '{topic} key concept #{rng.randint(1, 99)}'. True or false?"
            expected = "True" if correct else "False"
        else:
            correct_idx = rng.randrange(4)
            options = [
                AnswerOption(text=f"{topic} option {i}", is_correct=(i == correct_idx))
                for i in range(4)
            ]
            statement = f"[stub/{self.label}] ({bloom}) Which of the following best characterizes {topic} as covered in the course material?"
            expected = f"{topic} option {correct_idx}"

        return GeneratedItem(
            topic=topic,
            bloom_level=spec["bloom"],
            difficulty=spec["difficulty"],
            question_type=qtype,
            statement=statement,
            options=options,
            expected_answer=expected,
            solution_explanation=f"[stub] Deterministic solution for {topic} at {bloom} level.",
            points=1.0,
        )

    # --- evaluator behavior -------------------------------------------------
    def _evaluate_item(self, prompt: str) -> Any:
        from core.domain.schemas.exam import EvaluationResult

        # Quality derived deterministically from the item text + temperature.
        noise = random.Random(_seed(prompt[:500], self.label)).uniform(-0.5, 0.5)
        quality = max(0.0, min(10.0, 7.0 + (1.0 - self.temperature) + noise))
        return EvaluationResult(
            approved=quality >= 6.0,
            quality_score=round(quality, 2),
            difficulty_match=True,
            is_duplicate=False,
            similarity_score=None,
            rejection_reason=None,
        )


_SPEC_LINE = {
    "topic": r"- Topic: (.+)",
    "bloom": r"- Bloom level: (\w+)",
    "difficulty": r"- Difficulty: (\w+)",
    "qtype": r"- Question type: (\w+)",
}


def _parse_spec(prompt: str) -> dict[str, str]:
    out = {"topic": "general", "bloom": "remember", "difficulty": "easy", "qtype": "multiple_choice"}
    for key, pattern in _SPEC_LINE.items():
        m = re.search(pattern, prompt)
        if m:
            out[key] = m.group(1).strip()
    return out


class StubEmbedder:
    """Deterministic hash-based embedder with the bge-m3 interface."""

    def __init__(self, dim: int = 1024):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            rng = random.Random(_seed(text[:300]))
            vec = [rng.gauss(0.0, 1.0) for _ in range(self.dim)]
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vectors.append([v / norm for v in vec])
        return vectors

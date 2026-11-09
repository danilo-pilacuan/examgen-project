"""Harness: runs one evaluation run of the exam pipeline and collects metrics.

Responsibilities:
  1. Load experiment config (arms, repeats, subjects, blueprint presets).
  2. Register + index cloned subjects (same material, different names).
  3. Run the LangGraph pipeline with the arm's model profile + overrides,
     either against the real gateway or with deterministic stubs (--dry-run).
  4. Capture per-call LLM telemetry (node, latency, chars, usage) via a
     wrapping callback, without touching production code.
  5. Emit one JSON line per run into experiments/<id>/runs.jsonl.

Usage (from the meta-repo root):
  python -m test.evaluation.src.harness --experiment E01_temperature_sweep --dry-run
  python -m test.evaluation.src.harness --experiment E01_temperature_sweep --real
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path

import yaml

# Windows console (cp1252) cannot print the emoji/accents used in the logs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# Ensure API keys declared via api_key_env (e.g. OPENAI_API_KEY) are visible to
# os.environ consumers: pydantic-settings reads .env lazily inside core.config,
# but the evaluation registry and the LLM judge read os.environ directly. The
# process environment wins; .env only fills what the shell did not provide.
if not os.environ.get("OPENAI_API_KEY"):
    _env_file = ROOT / ".env"
    if _env_file.exists():
        for _line in _env_file.read_text(encoding="utf-8").splitlines():
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))

from test.evaluation.src.models_registry import get_profile, ModelProfile  # noqa: E402
from test.evaluation.src import _patch  # noqa: E402
from test.evaluation.src.metrics.quality import quality_metrics  # noqa: E402
from test.evaluation.src.metrics.diversity import diversity_metrics  # noqa: E402
from test.evaluation.src.metrics.rag import rag_metrics  # noqa: E402
from test.evaluation.src.metrics.bloom import bloom_metrics  # noqa: E402
from test.evaluation.src.metrics.cost import cost_metrics  # noqa: E402
from test.evaluation.src.metrics import faithfulness_judge  # noqa: E402

EVAL_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS_YAML = EVAL_ROOT / "experiments.yaml"
SUBJECTS_YAML = EVAL_ROOT / "subjects.yaml"
RUNS_DIR = EVAL_ROOT / "experiments"

# Overrides the arm can set to tweak RAG per blueprint.
RETRIEVAL_KEYS = {"retrieval_top_k", "retrieval_min_score", "retrieval_use_rag", "retrieval_max_chars_per_chunk"}


# ---------------------------------------------------------------------------
# Experiment / subjects loading
# ---------------------------------------------------------------------------
def load_experiment(exp_id: str) -> tuple[dict, dict]:
    """Returns (experiment, blueprints) from experiments.yaml."""
    with open(EXPERIMENTS_YAML, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    experiments = {e["id"]: e for e in cfg.get("experiments", [])}
    if exp_id not in experiments:
        available = ", ".join(sorted(experiments))
        raise KeyError(f"Unknown experiment '{exp_id}'. Available: {available}")
    return experiments[exp_id], cfg.get("blueprints", {})


def load_subject_defs() -> dict[str, dict]:
    """Returns {subject_id: {id, name, material_glob}} from subjects.yaml."""
    with open(SUBJECTS_YAML, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return {s["id"]: s for s in cfg.get("subjects", [])}


# ---------------------------------------------------------------------------
# Telemetry capture
# ---------------------------------------------------------------------------
class LLMTelemetry:
    """Thread-local-free collector of per-call LLM telemetry.

    The pipeline nodes already wrap their calls with perf_counter + latency;
    the harness re-measures by timing the whole structured invoke via the
    stub (dry-run) or by parsing pipeline timing (real mode keeps production
    code untouched and relies on the same clock methodology).
    """

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def record(self, node: str, latency_ms: int | None, prompt_chars: int, answer_chars: int) -> None:
        self.calls.append({
            "node": node,
            "latency_ms": latency_ms,
            "prompt_chars": prompt_chars,
            "answer_chars": answer_chars,
            "usage_prompt_tokens": None,
            "usage_completion_tokens": None,
        })


# ---------------------------------------------------------------------------
# Subject registration + indexing
# ---------------------------------------------------------------------------
def ensure_subject(name: str, material_glob: str, dry_run: bool) -> str:
    """Registers the subject and indexes its material. Returns subject_id."""
    from core.infrastructure.db.connection import SessionLocal
    from core.domain.models import Subject, MaterialChunk
    from core.infrastructure.embeddings.embedder import embedder as real_embedder
    from test.evaluation.src.stubs import StubEmbedder
    from test.evaluation.src._indexing import index_material_files

    if dry_run:
        embedder = StubEmbedder()
    else:
        embedder = real_embedder

    db = SessionLocal()
    try:
        subject = db.query(Subject).filter(Subject.name == name).first()
        if subject is None:
            subject = Subject(name=name)
            db.add(subject)
            db.commit()
            db.refresh(subject)
        subject_id = str(subject.id)
        has_chunks = db.query(MaterialChunk).filter(MaterialChunk.subject_id == subject.id).first() is not None
    finally:
        db.close()

    if not has_chunks:
        index_material_files(subject_id=subject_id, material_glob=material_glob, embedder=embedder, db_session_factory=SessionLocal)
    return subject_id


# ---------------------------------------------------------------------------
# Blueprint builder
# ---------------------------------------------------------------------------
def build_blueprint(preset: dict, subject_id: str) -> "Any":
    from core.domain.schemas.exam import BloomLevel, Difficulty, ExamBlueprint

    bloom = {BloomLevel(k): v for k, v in preset["bloom_distribution"].items()}
    diff = {Difficulty(k): v for k, v in preset["difficulty_distribution"].items()}
    topics = dict(preset["topics_weight"])
    blueprint = ExamBlueprint(
        subject_id=subject_id,
        total_questions=preset["total_questions"],
        bloom_distribution=bloom,
        difficulty_distribution=diff,
        topics_weight=topics,
        estimated_duration_minutes=preset.get("estimated_duration_minutes", 90),
    )
    if "retrieval" in preset:
        from core.domain.schemas.exam import RetrievalConfig
        blueprint.retrieval = RetrievalConfig(**preset["retrieval"])
    return blueprint


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------
def run_once(
    exp: dict,
    arm: dict,
    arm_index: int,
    repeat: int,
    subject_key: str,
    subject_def: dict,
    blueprint_preset: dict,
    dry_run: bool,
) -> dict:
    """Executes one pipeline run and returns the run record (dict)."""
    from test.evaluation.src.stubs import StubStructuredLLM

    profile: ModelProfile = get_profile(arm["model_profile"])
    telemetry = LLMTelemetry()

    subject_id = ensure_subject(
        name=subject_def["name"],
        material_glob=subject_def["material_glob"],
        dry_run=dry_run,
    )

    blueprint = build_blueprint(blueprint_preset, subject_id)
    _apply_retrieval_overrides(blueprint, arm.get("overrides") or {})

    if dry_run:
        stub = StubStructuredLLM(temperature=arm.get("overrides", {}).get("llm_temperature", 0.7), label=profile.model)
        _patch.activate_stubs(stub)
        _patch.reset_collector()
    else:
        _patch.activate_real(profile, arm.get("overrides") or {})
        _patch.reset_collector()

    from agents_backend.exam_pipeline.graph import run_exam_pipeline
    from core.infrastructure.latex.templates.registry import TemplateId

    materials = _resolve_materials(subject_def["material_glob"])
    started = time.perf_counter()
    state = run_exam_pipeline(
        subject_id=subject_id,
        subject_name=subject_def["name"],
        template_id=TemplateId.BASE_EXAM,
        raw_materials_paths=materials,
        blueprint=blueprint,
    )
    wall_ms = int((time.perf_counter() - started) * 1000)
    # For the audit-window query (llm_responses created_at filter).
    state["_eval_wall_seconds"] = max(1, wall_ms // 1000)

    # Collect per-item records from the pipeline state.
    item_records = _item_records_from_state(state)
    retrieval_records = _retrieval_records_from_state(state)

    approved_items = state.get("approved_items", [])
    q = quality_metrics(state, item_records)
    d = diversity_metrics(approved_items, list(blueprint_preset["topics_weight"].keys()), _get_embedder(dry_run))
    r = rag_metrics(_correlate_statements(_retrieval_records_from_state(state), item_records))
    b = bloom_metrics(item_records)
    # Real mode: derive telemetry from llm_responses audit rows (prompt,
    # answer, real latency per call); dry-run: from the stub instrument.
    calls, evaluator_answers, generator_answers, retrieval_records = _telemetry_for_cost(state, telemetry, dry_run)
    if evaluator_answers:
        _attach_evaluator_scores(item_records, evaluator_answers)
        q = quality_metrics(state, item_records)
    if generator_answers:
        _attach_generator_fields(item_records, generator_answers)
        b = bloom_metrics(item_records)
    if retrieval_records:
        r = rag_metrics(_correlate_statements(retrieval_records, item_records))
    c = cost_metrics(calls, len(approved_items))

    # LLM-judge faithfulness (post-hoc, real mode only): judged support of each
    # statement against the chunks the generator actually saw. Same model as
    # the pipeline (self-judge) unless a separate judge profile is configured.
    # The judge needs (statement, chunks) pairs: correlate the audit-derived
    # retrieval records the same way rag_metrics does, otherwise the judge
    # silently skips every record (statement is empty at this point) and
    # num_judged lands as 0.
    judged: dict[str, Any] = {}
    if not dry_run and retrieval_records:
        try:
            judged = faithfulness_judge.judge_faithfulness(
                _correlate_statements(retrieval_records, item_records)
            )
        except Exception as exc:  # judge failure must not kill the run record
            print(f"      ⚠️ judge faithfulness failed: {exc}")
            judged = {"faithfulness_judge_mean": None, "judgement_errors": 1}

    run_id = f"{exp['id']}_arm{arm_index}_r{repeat}_{subject_key}"
    record = {
        "run_id": run_id,
        "experiment": exp["id"],
        "arm_index": arm_index,
        "arm_overrides": arm.get("overrides") or {},
        "model_profile": arm["model_profile"],
        "model": profile.model,
        "mode": "dry_run" if dry_run else "real",
        "repeat": repeat,
        "subject_key": subject_key,
        "subject_name": subject_def["name"],
        "subject_id": subject_id,
        "status": state.get("status"),
        "error_message": state.get("error_message"),
        "wall_time_ms": wall_ms,
        "metrics": {"quality": q, "diversity": d, "rag": r, "bloom": b, "cost": c, "rag_judge": judged},
        "state_digest": {
            "approved_count": len(approved_items),
            "rejection_count": len(state.get("rejection_log", [])),
            "total_llm_calls": state.get("total_llm_calls"),
            "indexed_chunks_count": state.get("indexed_chunks_count"),
        },
        "items": [
            {
                "topic": it.topic,
                "bloom_level": it.bloom_level.value,
                "difficulty": it.difficulty.value,
                "question_type": it.question_type.value,
                "statement": it.statement,
                "expected_answer": it.expected_answer,
            }
            for it in approved_items
        ],
    }
    return record


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_runs_jsonl(path: Path) -> list[dict]:
    """Loads existing run records from a runs.jsonl (empty if missing/broken)."""
    if not path.exists():
        return []
    records: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _apply_retrieval_overrides(blueprint: Any, overrides: dict) -> None:
    for key in RETRIEVAL_KEYS:
        if key in overrides:
            attr = key.replace("retrieval_", "")
            setattr(blueprint.retrieval, attr, overrides[key])


def _resolve_materials(material_glob: str) -> list[str]:
    import glob as _glob
    from pathlib import Path as _Path

    os_cwd = Path.cwd()
    pattern = str(ROOT / material_glob) if not _Path(material_glob).is_absolute() else material_glob
    return sorted(set(_glob.glob(pattern)))


def _get_embedder(dry_run: bool) -> Any:
    if dry_run:
        from test.evaluation.src.stubs import StubEmbedder
        return StubEmbedder()
    from core.infrastructure.embeddings.embedder import embedder as real_embedder
    return real_embedder


def _item_records_from_state(state: dict) -> list[dict]:
    """Reconstructs per-spec attempt records from pipeline state.

    The rejection_log carries spec_id, attempt_number, reason and scores;
    approved items carry their spec via current acceptance. For specs that
    were approved, retries = 0 (accepted on the first attempt of that cycle).
    """
    records: list[dict] = []
    approved = state.get("approved_items", [])
    # NOTE: the pipeline's rejection_log is per rejected attempt; approval
    # events are not individually logged. We approximate per-spec outcomes:
    rejected_by_reason = {}
    for entry in state.get("rejection_log", []):
        rejected_by_reason.setdefault(entry.get("spec_id"), []).append(entry)

    approved_as_records = [
        {
            "approved": True,
            "quality_score": None,
            "retry_count": 0,
            "rejection_reason": None,
            "spec_bloom": it.bloom_level.value,
            "item_bloom": it.bloom_level.value,
            "spec_difficulty": it.difficulty.value,
            "item_difficulty": it.difficulty.value,
            "spec_type": it.question_type.value,
            "item_type": it.question_type.value,
        }
        for it in approved
    ]

    # Attempt-level records from rejection entries (spec level)
    for spec_id, entries in rejected_by_reason.items():
        for entry in entries:
            records.append({
                "approved": False,
                "quality_score": entry.get("quality_score"),
                "retry_count": entry.get("attempt_number", 1),
                "rejection_reason": entry.get("reason"),
                "spec_bloom": None,
                "item_bloom": None,
                "spec_difficulty": None,
                "item_difficulty": None,
                "spec_type": None,
                "item_type": None,
            })

    return approved_as_records + records


def _retrieval_records_from_state(state: dict) -> list[dict]:
    """Retrieval records: dry-run builds them from the stub retrieval cache;
    real mode would read llm_responses audit rows."""
    return state.get("_eval_retrieval_records", []) or _patch.get_retrieval_records()


def _correlate_statements(records: list[dict], item_records: list[dict]) -> list[dict]:
    """Attaches the generated statements to the retrieval traces by order.

    Retrieval happens once per generated spec in generation order, so record
    i correlates with the i-th generated statement (approved or rejected —
    the harness collects statements from both via the audit rows).
    """
    statements = [r["statement"] for r in item_records if r.get("statement")]
    out = []
    for i, rec in enumerate(records):
        rec = dict(rec)
        if statements:
            rec["statement"] = statements[i % len(statements)]
        out.append(rec)
    return out


def _read_audit_calls(since_seconds: int | None = None) -> tuple[list[dict], list[dict], list[dict]]:
    """Reads this run's LLM calls from the llm_responses audit table.

    Node attribution: context 'pipeline:generator' / 'pipeline:evaluator'.
    Chars are counted from the stored prompt/answer; latency is the real
    per-call latency the pipeline already measured.

    Returns (calls, evaluator_answers, generator_answers): raw evaluator
    and generator JSON answers in chronological order, for quality-score
    and spec/item field extraction by positional correlation with attempts.
    """
    from datetime import datetime, timedelta, timezone

    from sqlalchemy import select

    from core.domain.models import LLMResponse
    from core.infrastructure.db.connection import SessionLocal

    db = SessionLocal()
    try:
        stmt = select(LLMResponse).where(LLMResponse.context.like("pipeline:%"))
        if since_seconds:
            cutoff = datetime.now(timezone.utc) - timedelta(seconds=since_seconds + 10)
            stmt = stmt.where(LLMResponse.created_at >= cutoff)
        stmt = stmt.order_by(LLMResponse.created_at.asc())
        rows = db.execute(stmt).scalars().all()
    finally:
        db.close()

    calls = []
    evaluator_answers: list[dict] = []
    generator_answers: list[dict] = []
    retrieval_records: list[dict] = []
    for row in rows:
        node = row.context.split(":")[-1] if ":" in row.context else row.context
        calls.append({
            "node": node,
            "latency_ms": row.latency_ms,
            "prompt_chars": len(row.prompt or ""),
            "answer_chars": len(row.raw_answer or ""),
            "usage_prompt_tokens": None,
            "usage_completion_tokens": None,
        })
        prompt = row.prompt or ""
        if row.context.endswith("evaluator"):
            try:
                evaluator_answers.append(json.loads(row.raw_answer or "{}"))
            except json.JSONDecodeError:
                pass
        elif row.context.endswith("generator"):
            try:
                generator_answers.append(json.loads(row.raw_answer or "{}"))
            except json.JSONDecodeError:
                pass
            retrieval_records.append(_parse_retrieval_from_prompt(prompt))
    return calls, evaluator_answers, generator_answers, retrieval_records


_CHUNK_HEADER = re.compile(r"\[Chunk (\d+) \(score ([0-9.]+)\)\]")


def _parse_retrieval_from_prompt(prompt: str) -> dict:
    """Extracts the retrieval trace from a generator prompt.

    The pipeline formats the RAG context as `[Chunk i (score s)]\\n<content>`;
    when RAG was not used the prompt carries a 'Syllabus context' fallback.
    """
    headers = _CHUNK_HEADER.findall(prompt)
    chunks = []
    scores = []
    if headers:
        # Split the prompt by chunk headers to recover each chunk body.
        parts = _CHUNK_HEADER.split(prompt)
        # parts: [pre, idx1, score1, body1, idx2, score2, body2, ...]
        for i in range(1, len(parts) - 2, 3):
            _idx, score, body = parts[i], parts[i + 1], parts[i + 2]
            scores.append(float(score))
            chunks.append(body.strip())
    return {
        "query": "",
        "chunks": chunks,
        "chunk_scores": scores,
        "statement": "",
        "used_rag": bool(headers),
    }


def _attach_evaluator_scores(item_records: list[dict], evaluator_answers: list[dict]) -> None:
    """Fills quality_score of attempts from the evaluator's raw audit answers.

    Correlation: the evaluator runs once per generator attempt in order, so
    the i-th evaluator answer maps to the i-th attempt record. Records that
    already carry a score (rejection_log) keep it.
    """
    scored = [r for r in item_records if r.get("quality_score") is None]
    for record, answer in zip(scored, evaluator_answers):
        if isinstance(answer, dict) and isinstance(answer.get("quality_score"), (int, float)):
            record["quality_score"] = float(answer["quality_score"])


def _attach_generator_fields(item_records: list[dict], generator_answers: list[dict]) -> None:
    """Fills spec/item fields of attempts from the generator's raw audit answers.

    Each generator answer is a full GeneratedItem JSON: it carries what the
    spec asked (topic/bloom/difficulty/type echoed by the prompt) and what
    the model actually produced. Positional correlation with attempt records.
    """
    unscored = [r for r in item_records if r.get("item_bloom") is None]
    for record, answer in zip(unscored, generator_answers):
        if not isinstance(answer, dict):
            continue
        record["item_bloom"] = answer.get("bloom_level")
        record["item_difficulty"] = answer.get("difficulty")
        record["item_type"] = answer.get("question_type")
        # The spec asked exactly what the prompt specified; the generator
        # echo of the same fields doubles as the spec value per attempt.
        record.setdefault("spec_bloom", record.get("spec_bloom") or answer.get("bloom_level"))
        record.setdefault("spec_difficulty", record.get("spec_difficulty") or answer.get("difficulty"))
        record.setdefault("spec_type", record.get("spec_type") or answer.get("question_type"))
        statement = answer.get("statement")
        if statement:
            record["statement"] = statement


def _telemetry_for_cost(state: dict, telemetry: LLMTelemetry, dry_run: bool) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    if dry_run:
        return _patch.get_collector().calls or telemetry.calls, [], [], _patch.get_retrieval_records()
    # Real mode: read the pipeline's own audit rows (llm_responses) for this
    # run window; they carry prompt/answer/latency per call, and generator
    # prompts carry the RAG chunks used per call.
    return _read_audit_calls(since_seconds=state.get("_eval_wall_seconds"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Run evaluation experiments")
    parser.add_argument("--experiment", help="Experiment id from experiments.yaml")
    parser.add_argument("--list", action="store_true", help="List experiments and exit")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Use deterministic stubs (default)")
    parser.add_argument("--real", action="store_true", help="Call the real LLM gateway")
    parser.add_argument("--limit-subjects", nargs="*", help="Subset of subject ids")
    parser.add_argument("--limit-repeats", type=int, help="Override repeats (smoke test)")
    args = parser.parse_args()

    with open(EXPERIMENTS_YAML, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    if args.list:
        for e in cfg.get("experiments", []):
            n_arms = len(e.get("arms", []))
            n_subjects = len(e.get("subjects", []))
            print(f"{e['id']}: {n_arms} arms x {n_subjects} subjects x {e.get('repeats')} repeats")
        return

    if not args.experiment:
        parser.error("--experiment is required (or use --list)")

    exp, blueprints = load_experiment(args.experiment)
    subjects = load_subject_defs()
    subject_keys = args.limit_subjects or exp["subjects"]
    repeats = args.limit_repeats or exp.get("repeats", 1)
    dry_run = not args.real

    out_dir = RUNS_DIR / exp["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    runs_path = out_dir / "runs.jsonl"

    total = len(exp["arms"]) * len(subject_keys) * repeats
    done = 0
    print(f"🧪 Experiment {exp['id']} — {total} runs ({'DRY-RUN' if dry_run else 'REAL'})")
    # Drop previously failed records upfront: they are retried by this run.
    existing = load_runs_jsonl(runs_path)
    failed_before = [r for r in existing if r.get("status") == "failed"]
    if failed_before:
        print(f"♻️ Retrying {len(failed_before)} previously failed run(s)", flush=True)
        with open(runs_path, "w", encoding="utf-8") as f:
            for r in existing:
                if r.get("status") != "failed":
                    f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    existing_run_ids = {r.get("run_id") for r in existing if r.get("status") != "failed"}
    failed: list[str] = []
    for arm_index, arm in enumerate(exp["arms"]):
        for subject_key in subject_keys:
            subject_def = subjects[subject_key]
            for repeat in range(1, repeats + 1):
                done += 1
                run_id = f"{exp['id']}_arm{arm_index}_r{repeat}_{subject_key}"
                if run_id in existing_run_ids:
                    print(f"  [{done}/{total}] arm={arm_index} subject={subject_key} repeat={repeat} SKIP (resume: {run_id} already in runs.jsonl)", flush=True)
                    continue
                print(f"  [{done}/{total}] arm={arm_index} subject={subject_key} repeat={repeat} ...", flush=True)
                try:
                    record = run_once(
                        exp=exp,
                        arm=arm,
                        arm_index=arm_index,
                        repeat=repeat,
                        subject_key=subject_key,
                        subject_def=subject_def,
                        blueprint_preset=blueprints[exp["blueprint"]],
                        dry_run=dry_run,
                    )
                except Exception as exc:
                    # One unstable run must not kill the batch: log it as a
                    # failed record and continue with the remaining combos.
                    traceback.print_exc()
                    failed.append(run_id)
                    record = {
                        "run_id": run_id,
                        "experiment": exp["id"],
                        "arm_index": arm_index,
                        "arm_overrides": arm.get("overrides") or {},
                        "model_profile": arm["model_profile"],
                        "mode": "dry_run" if dry_run else "real",
                        "repeat": repeat,
                        "subject_key": subject_key,
                        "status": "failed",
                        "error_message": f"{type(exc).__name__}: {exc}",
                    }
                with open(runs_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
                print(f"      status={record['status']} approved={record.get('state_digest', {}).get('approved_count')}")

    if failed:
        print(f"⚠️ {len(failed)} failed run(s): {', '.join(failed)}")
    print(f"✅ Runs written to {runs_path}")


if __name__ == "__main__":
    main()

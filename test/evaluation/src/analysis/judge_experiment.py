"""Post-hoc LLM-judge faithfulness over an experiment's runs.jsonl.

Reads each run record's retrieval records (stored in the audit-derived
metrics), re-derives them from llm_responses when needed, judges
faithfulness and writes runs_judged.jsonl (original record + rag_judge).

Usage:
  python -m test.evaluation.src.analysis.judge_experiment --experiment E03_robustness_clones
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EVAL_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = EVAL_ROOT / "experiments"


def main() -> None:
    parser = argparse.ArgumentParser(description="Post-hoc judge faithfulness for an experiment")
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--judge-profile", default="glm-flash-default")
    args = parser.parse_args()

    from test.evaluation.src.metrics import faithfulness_judge

    runs_path = RUNS_DIR / args.experiment / "runs.jsonl"
    out_path = RUNS_DIR / args.experiment / "runs_judged.jsonl"
    if not runs_path.exists():
        raise FileNotFoundError(runs_path)

    # The judge needs (statement, chunks) pairs. They live in the audit
    # table (generator prompts + generator answers), correlated per run by
    # the run's time window. Rebuild them the same way the harness does.
    from test.evaluation.src.harness import _read_audit_calls, _parse_retrieval_from_prompt

    import json as _json

    from sqlalchemy import select

    from core.domain.models import LLMResponse
    from core.infrastructure.db.connection import SessionLocal

    # All audit rows with generator context (chronological); we window them
    # per run using each run's stored total latency + call count heuristic.
    db = SessionLocal()
    try:
        rows = db.execute(
            select(LLMResponse).where(LLMResponse.context.like("pipeline:generator%")).order_by(LLMResponse.created_at.asc())
        ).scalars().all()
    finally:
        db.close()

    runs = [json.loads(line) for line in runs_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"judging {len(runs)} runs ({len(rows)} generator audit rows available)")

    def _gen_count(run: dict) -> int:
        # Generator call count stored per run by cost_metrics; fall back to
        # total_llm_calls for legacy records without per-node latency.
        nodes = ((run.get("metrics") or {}).get("cost") or {}).get("latency_by_node_ms") or {}
        count = (nodes.get("generator") or {}).get("count")
        if count is None:
            count = run.get("state_digest", {}).get("total_llm_calls") or 0
        return int(count)

    # Runs are judged in chronological order and the campaign rows sit at the
    # tail of the audit table: rows created before the campaign (e.g. seed
    # bank generation) must not be consumed by the first run's window.
    total_gen_calls = sum(_gen_count(run) for run in runs)
    campaign_rows = rows[-total_gen_calls:] if len(rows) > total_gen_calls else rows

    consumed = 0
    judged_rows = []
    for run in runs:
        window = campaign_rows[consumed:consumed + _gen_count(run)]
        consumed += _gen_count(run)
        records = []
        for row in window:
            prompt = row.prompt or ""
            rec = _parse_retrieval_from_prompt(prompt if "[Chunk" in prompt else prompt)
            try:
                answer = _json.loads(row.raw_answer or "{}")
            except _json.JSONDecodeError:
                continue
            statement = answer.get("statement", "")
            rec["statement"] = statement
            records.append(rec)
        records = [r for r in records if r["chunks"] and r["statement"]]
        if not records:
            judged_rows.append({**run, "metrics": {**run["metrics"], "rag_judge": {"faithfulness_judge_mean": None, "num_judged": 0}}})
            continue
        res = faithfulness_judge.judge_faithfulness(records, judge_profile_name=args.judge_profile)
        print(f"  {run['run_id']}: judged={res['num_judged']} mean={res['faithfulness_judge_mean']} errors={res['judgement_errors']}")
        judged_rows.append({**run, "metrics": {**run["metrics"], "rag_judge": res}})

    with open(out_path, "w", encoding="utf-8") as f:
        for r in judged_rows:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    print(f"✅ {out_path}")


if __name__ == "__main__":
    main()

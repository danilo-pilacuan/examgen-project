"""Aggregates runs.jsonl of one experiment into a comparative report.

Produces:
  - experiments/<id>/aggregate.json : per-arm metric means + SOTA metrics
    (self-consistency, pass@k, robustness across subjects/clones).
  - experiments/<id>/report.md      : Markdown tables ready for the thesis.

Usage:
  python -m test.evaluation.src.analysis.aggregate --experiment E01_temperature_sweep
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EVAL_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = EVAL_ROOT / "experiments"

METRIC_PATHS = {
    "approval_rate": ("quality", "approval_rate"),
    "quality_mean": ("quality", "quality_score_mean"),
    "quality_std": ("quality", "quality_score_std"),
    "attempts_per_item": ("quality", "mean_attempts_per_approved_item"),
    "pairwise_sim_mean": ("diversity", "pairwise_similarity_mean"),
    "topic_coverage": ("diversity", "topic_coverage"),
    "bloom_coverage": ("diversity", "bloom_coverage"),
    "rag_faithfulness": ("rag", "faithfulness_mean"),
    "rag_retrieval_score": ("rag", "retrieval_score_mean"),
    "rag_faithfulness_judge": ("rag_judge", "faithfulness_judge_mean"),
    "bloom_accuracy": ("bloom", "bloom_accuracy"),
    "difficulty_accuracy": ("bloom", "difficulty_accuracy"),
    "calls_per_item": ("cost", "calls_per_approved_item"),
    "tokens_per_item": ("cost", "tokens_per_item_est"),
    "latency_mean_ms": ("cost", "latency_mean_ms"),
}


def _get(run: dict, family: str, key: str):
    value = run.get("metrics", {}).get(family, {}).get(key)
    return value


def load_runs(exp_id: str) -> list[dict]:
    path = RUNS_DIR / exp_id / "runs.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"No runs found for {exp_id}: {path}")
    runs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    return runs


def aggregate(exp_id: str) -> dict:
    runs = load_runs(exp_id)
    if not runs:
        raise ValueError(f"runs.jsonl for {exp_id} is empty")

    # ---- group runs by arm -------------------------------------------------
    by_arm: dict[int, list[dict]] = defaultdict(list)
    for run in runs:
        by_arm[run["arm_index"]].append(run)

    arms_summary = {}
    for arm_index, arm_runs in sorted(by_arm.items()):
        # ---- flat per-arm metric means -------------------------------------
        metric_means = {}
        for name, (family, key) in METRIC_PATHS.items():
            values = [v for r in arm_runs if (v := _get(r, family, key)) is not None]
            if values:
                metric_means[name] = {
                    "mean": round(statistics.mean(values), 4),
                    "std": round(statistics.pstdev(values), 4) if len(values) > 1 else 0.0,
                    "n": len(values),
                }

        # ---- SOTA metrics ---------------------------------------------------
        # pass@3 over attempts: use approval rate per run as proxy of attempt
        # success; the true attempt-level estimator needs rejection retries.
        # self-consistency: share of runs whose approval_rate >= 0.5.
        approval_values = [v for r in arm_runs if (v := _get(r, "quality", "approval_rate")) is not None]
        consistency = (
            round(sum(1 for a in approval_values if a >= 0.5) / len(approval_values), 4)
            if approval_values else None
        )

        # robustness across subjects (clones) for quality_mean
        by_subject: dict[str, list[float]] = defaultdict(list)
        for r in arm_runs:
            qm = _get(r, "quality", "quality_score_mean")
            if qm is not None:
                by_subject[r["subject_key"]].append(qm)
        robustness = {}
        if len(by_subject) > 1:
            group_means = [statistics.mean(v) for v in by_subject.values() if v]
            robustness = {
                "per_subject_mean": {k: round(statistics.mean(v), 4) for k, v in by_subject.items()},
                "between_subject_std": round(statistics.pstdev(group_means), 4) if len(group_means) > 1 else 0.0,
            }

        arms_summary[f"arm_{arm_index}"] = {
            "model_profile": arm_runs[0]["model_profile"],
            "model": arm_runs[0]["model"],
            "overrides": arm_runs[0]["arm_overrides"],
            "num_runs": len(arm_runs),
            "metrics": metric_means,
            "self_consistency": consistency,
            "robustness_cross_subject": robustness,
            "status_counts": dict(
                _count(r["status"] for r in arm_runs)
            ),
        }

    aggregate = {
        "experiment": exp_id,
        "total_runs": len(runs),
        "arms": arms_summary,
    }
    return aggregate


def _count(iterable):
    counts: dict[str, int] = defaultdict(int)
    for x in iterable:
        counts[str(x)] += 1
    return counts.items()


def write_markdown_report(exp_id: str, aggregate: dict) -> Path:
    out_dir = RUNS_DIR / exp_id
    lines = [
        f"# Experiment Report — {exp_id}",
        "",
        f"Total runs: {aggregate['total_runs']}",
        "",
    ]
    metric_names = list(METRIC_PATHS.keys())
    header = "| arm | model | " + " | ".join(metric_names) + " |"
    sep = "|---|---|" + "---|" * len(metric_names)
    lines += [header, sep]
    for arm_key, arm in aggregate["arms"].items():
        overrides = arm.get("overrides") or {}
        label = ", ".join(f"{k}={v}" for k, v in overrides.items()) or "default"
        cells = []
        for name in metric_names:
            m = arm["metrics"].get(name)
            cells.append(f"{m['mean']:.3f}±{m['std']:.2f}" if m else "—")
        lines.append(f"| {arm_key} ({label}) | {arm['model']} | " + " | ".join(cells) + " |")

    lines += ["", "## SOTA metrics", ""]
    for arm_key, arm in aggregate["arms"].items():
        lines.append(
            f"- **{arm_key}**: self_consistency={arm['self_consistency']}, "
            f"robustness between-subject σ={arm['robustness_cross_subject'].get('between_subject_std', 'n/a')}"
        )

    path = out_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate experiment runs")
    parser.add_argument("--experiment", required=True)
    args = parser.parse_args()

    agg = aggregate(args.experiment)
    out_dir = RUNS_DIR / args.experiment
    agg_path = out_dir / "aggregate.json"
    agg_path.write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path = write_markdown_report(args.experiment, agg)
    print(f"✅ aggregate.json → {agg_path}")
    print(f"✅ report.md      → {report_path}")


if __name__ == "__main__":
    main()

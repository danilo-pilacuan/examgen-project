"""Plot generation for experiment reports (matplotlib PNGs).

Usage:
  python -m test.evaluation.src.reporting.report --experiment E01_temperature_sweep
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

EVAL_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = EVAL_ROOT / "experiments"

PLOTS = [
    ("approval_rate", "Approval rate by arm", (0.0, 1.0)),
    ("quality_mean", "Mean quality score by arm", None),
    ("pairwise_sim_mean", "Pairwise similarity (diversity ↓ = more diverse)", None),
    ("rag_faithfulness", "RAG faithfulness by arm", (0.0, 1.0)),
    ("bloom_accuracy", "Bloom alignment accuracy", (0.0, 1.0)),
    ("tokens_per_item", "Estimated tokens per approved item", None),
    ("calls_per_item", "LLM calls per approved item", None),
]


def plot_experiment(exp_id: str) -> list[Path]:
    agg_path = RUNS_DIR / exp_id / "aggregate.json"
    if not agg_path.exists():
        raise FileNotFoundError(f"Run the aggregator first: {agg_path}")
    agg = json.loads(agg_path.read_text(encoding="utf-8"))

    out_paths: list[Path] = []
    arms = agg["arms"]
    labels = []
    for key, arm in arms.items():
        overrides = arm.get("overrides") or {}
        label = ", ".join(f"{k.replace('llm_', '')}={v}" for k, v in overrides.items()) or "default"
        labels.append(f"{key}\n({label})")

    for metric, title, ylim in PLOTS:
        values = []
        for arm in arms.values():
            m = arm["metrics"].get(metric)
            values.append(m["mean"] if m else 0.0)
        if all(v == 0.0 for v in values):
            continue

        fig, ax = plt.subplots(figsize=(8, 4.5))
        stds = [arms[key]["metrics"].get(metric, {}).get("std", 0.0) for key in arms]
        ax.bar(labels, values, yerr=stds, capsize=4, color="#4C72B0")
        ax.set_title(title)
        ax.set_ylabel(metric)
        if ylim:
            ax.set_ylim(*ylim)
        ax.grid(axis="y", alpha=0.3)
        plt.xticks(fontsize=8)
        plt.tight_layout()
        out = RUNS_DIR / exp_id / f"{metric}.png"
        fig.savefig(out, dpi=120)
        plt.close(fig)
        out_paths.append(out)
    return out_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate experiment plots")
    parser.add_argument("--experiment", required=True)
    args = parser.parse_args()
    paths = plot_experiment(args.experiment)
    for p in paths:
        print(f"🖼 {p}")


if __name__ == "__main__":
    main()

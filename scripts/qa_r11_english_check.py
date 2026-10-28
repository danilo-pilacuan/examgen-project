"""QA round 11 - English enforcement spot-check (HITL).

Scans every run record of the r11 campaign (82 runs) and flags generated
items whose statement/options/answer/explanation contain Spanish markers
(diacritics or common Spanish stopwords). Prints a deterministic sample
for manual human review.

Usage (repo root, .venv):
    .venv\\Scripts\\python.exe scripts\\qa_r11_english_check.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP_DIR = ROOT / "test" / "evaluation" / "experiments"
EXPERIMENTS = [
    "E01_temperature_sweep",
    "E02_rag_topk_sweep",
    "E03_robustness_clones",
    "E04_evaluator_temperature",
]

DIACRITICS = set("áéíóúñüÁÉÍÓÚÑÜ¿¡")
SPANISH_STOPWORDS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "del",
    "que", "como", "para", "por", "con", "sin", "sobre", "entre", "segun",
    "donde", "cuando", "porque", "aunque", "esto", "esta", "este", "eso",
    "se", "su", "sus", "hay", "son", "ser", "es", "mas", "tambien",
}

FIELDS = ("statement", "expected_answer", "options", "explanation")


def iter_items(runs_path):
    with open(runs_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            run = json.loads(line)
            for idx, item in enumerate(run.get("items") or []):
                yield run, idx, item


def check_text(text):
    flags = []
    lowered = text.lower()
    if any(ch in DIACRITICS for ch in lowered):
        flags.append("diacritic")
    words = set(lowered.split())
    hits = words & SPANISH_STOPWORDS
    if hits:
        flags.append("stopword:" + ",".join(sorted(hits)[:4]))
    return flags


def item_texts(item):
    for field in FIELDS:
        value = item.get(field)
        if value is None:
            continue
        if isinstance(value, list):
            for part in value:
                if isinstance(part, str):
                    yield field, part
        elif isinstance(value, dict):
            for part in value.values():
                if isinstance(part, str):
                    yield field, part
        elif isinstance(value, str):
            yield field, value


def main():
    total_items = 0
    flagged = []
    sample = []
    for exp in EXPERIMENTS:
        runs_path = EXP_DIR / exp / "runs.jsonl"
        if not runs_path.exists():
            print(f"MISSING {runs_path}")
            sys.exit(1)
        exp_items = 0
        for run, idx, item in iter_items(runs_path):
            exp_items += 1
            texts = list(item_texts(item))
            item_flags = set()
            for field, text in texts:
                item_flags.update(check_text(text))
            if (run.get("repeat") or 0) == 0 and idx < 2 and len(sample) < 24:
                sample.append((exp, run.get("run_id"), idx, item.get("statement", "")[:160]))
            if item_flags:
                flagged.append((exp, run.get("run_id"), idx, sorted(item_flags),
                                item.get("statement", "")[:120]))
        total_items += exp_items
        print(f"{exp}: {exp_items} items")

    print(f"\nTOTAL items scanned: {total_items}")
    print(f"Flagged items: {len(flagged)}")
    for entry in flagged[:20]:
        print("FLAG", entry)
    print("\n--- Manual review sample (first 2 items of repeat 0 per run, capped 24) ---")
    for exp, run_id, idx, stmt in sample:
        print(f"[{exp} / {run_id} / item {idx}] {stmt}")


if __name__ == "__main__":
    main()

"""One-off fix: re-index the 5 cloned subjects with the REAL embedder.

The dry-run harness indexed material with StubEmbedder vectors into the
real DB; those chunks are unusable for real RAG retrieval (similarity
~0.08 << min_score 0.15). This script deletes the stub-embedded chunks of
the clones and re-indexes with bge-m3.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import yaml

from sqlalchemy import text

from core.infrastructure.db.connection import SessionLocal
from test.evaluation.src._indexing import index_material_files

with open(Path(__file__).parent / "subjects.yaml", encoding="utf-8") as f:
    subjects = yaml.safe_load(f)["subjects"]

db = SessionLocal()
for s in subjects:
    sid = db.execute(
        text("SELECT id FROM subjects WHERE name = :name"), {"name": s["name"]}
    ).scalar()
    if sid is None:
        print(f"skip (not found): {s['name']}")
        continue
    deleted = db.execute(
        text("DELETE FROM material_chunks WHERE subject_id = CAST(:sid AS uuid)"),
        {"sid": str(sid)},
    ).rowcount
    db.commit()
    print(f"{s['name']}: deleted {deleted} stub-embedded chunks")
db.close()

# Re-index with the real embedder
from core.infrastructure.embeddings.embedder import embedder as real_embedder

for s in subjects:
    db = SessionLocal()
    sid = db.execute(
        text("SELECT id FROM subjects WHERE name = :name"), {"name": s["name"]}
    ).scalar()
    db.close()
    if sid is None:
        continue
    n = index_material_files(
        subject_id=str(sid),
        material_glob=s["material_glob"],
        embedder=real_embedder,
        db_session_factory=SessionLocal,
    )
    print(f"{s['name']}: re-indexed {n} chunks with bge-m3")

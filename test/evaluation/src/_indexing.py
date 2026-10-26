"""Material indexing helper for the evaluation harness.

Reuses the same chunking + persistence logic as scripts/index_material.py
but accepts an injected embedder (real or stub) so dry-runs never need the
embedding service.
"""
from __future__ import annotations

import glob
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]


def index_material_files(
    subject_id: str,
    material_glob: str,
    embedder: Any,
    db_session_factory: Any,
    chunk_size: int = 1500,
    chunk_overlap: int = 150,
) -> int:
    """Indexes the material files into material_chunks. Returns chunk count."""
    from core.domain.models import MaterialChunk

    pattern = material_glob if Path(material_glob).is_absolute() else str(ROOT / material_glob)
    files = sorted(set(glob.glob(pattern)))
    if not files:
        print(f"  ⚠️ eval-index: no files matched {pattern}")
        return 0

    from core.infrastructure.files.extract import (
        _extract_pdf,
        _extract_docx,
        _extract_pptx,
        _extract_xlsx,
        _extract_text_file,
    )

    def extract(path: str) -> str:
        ext = path.lower().rsplit(".", 1)[-1]
        if ext == "pdf":
            return _extract_pdf(path)
        if ext == "docx":
            return _extract_docx(path)
        if ext == "pptx":
            return _extract_pptx(path)
        if ext == "xlsx":
            return _extract_xlsx(path)
        return _extract_text_file(path)

    def chunk_text(text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []
        chunks, start = [], 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end].strip())
            if end == len(text):
                break
            start = end - chunk_overlap
        return [c for c in chunks if c]

    texts: list[str] = []
    for f in files:
        try:
            texts.extend(chunk_text(extract(f)))
        except Exception as e:  # noqa: BLE001
            print(f"  ⚠️ eval-index: failed to extract {Path(f).name}: {e}")

    if not texts:
        return 0

    vectors = embedder.embed(texts)
    db = db_session_factory()
    try:
        for content, vec in zip(texts, vectors):
            db.add(MaterialChunk(
                subject_id=uuid.UUID(subject_id),
                source_file="evaluation",
                chunk_index=0,
                content=content,
                embedding=vec,
            ))
        db.commit()
    finally:
        db.close()
    return len(texts)

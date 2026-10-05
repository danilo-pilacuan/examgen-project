"""Indexes a subject's material into the DB (RAG).

Usage:
    python scripts/index_material.py --subject-id <id> --name "Applied Economics" \
        --materials "data/inputs/Applied_Economics/Notes/*.pdf"

This script:
  1. Registers (or updates) the subject in the `subjects` table.
  2. Reads the material files and splits them into chunks.
  3. Generates embeddings for each chunk via the local service.
  4. Saves chunks + embeddings into `material_chunks`.
"""
import argparse
import glob
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import select  # noqa: E402

from core.infrastructure.db.connection import SessionLocal  # noqa: E402
from core.domain.models import Subject, MaterialChunk  # noqa: E402
from core.infrastructure.embeddings.embedder import embedder  # noqa: E402
from core.infrastructure.files.extract import (  # noqa: E402
    _extract_pdf,
    _extract_docx,
    _extract_pptx,
    _extract_xlsx,
    _extract_text_file,
)

CHUNK_SIZE = 1500  # characters per chunk
CHUNK_OVERLAP = 150  # overlap to avoid cutting ideas


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Splits a text into chunks with overlap."""
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = end - overlap
    return [c for c in chunks if c]


def extract_file(path: str) -> str:
    """Extracts text from a file according to its extension."""
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    if ext == "pdf":
        return _extract_pdf(path)
    if ext == "docx":
        return _extract_docx(path)
    if ext == "pptx":
        return _extract_pptx(path)
    if ext == "xlsx":
        return _extract_xlsx(path)
    return _extract_text_file(path)


def resolve_materials(patterns: list[str]) -> list[str]:
    """Expands glob patterns into a list of file paths."""
    files: list[str] = []
    for pat in patterns:
        files.extend(str(p) for p in glob.glob(pat))
    return sorted(set(files))


def main() -> None:
    parser = argparse.ArgumentParser(description="Indexes a subject's material into the DB")
    parser.add_argument("--subject-id", help="Subject ID (UUID). Created if it doesn't exist.")
    parser.add_argument("--name", required=True, help="Name of the subject")
    parser.add_argument(
        "--materials", nargs="+", required=True,
        help="Glob patterns of the material files (e.g. 'data/inputs/**/*.pdf')",
    )
    parser.add_argument("--clear", action="store_true", help="Delete previous chunks of the subject")
    args = parser.parse_args()

    files = resolve_materials(args.materials)
    if not files:
        print("❌ No files found with the given patterns.")
        sys.exit(1)
    print(f"📚 Files to index: {len(files)}")

    # Collect all chunks
    all_chunks: list[tuple[str, int, str]] = []  # (source_file, index, content)
    for f in files:
        try:
            text = extract_file(f)
            chunks = chunk_text(text)
            for i, c in enumerate(chunks):
                all_chunks.append((f, i, c))
            print(f"  ✅ {Path(f).name}: {len(chunks)} chunks")
        except Exception as e:
            print(f"  ⚠️ {Path(f).name}: error {e}")

    if not all_chunks:
        print("❌ Could not extract any chunk.")
        sys.exit(1)
    print(f"\n🧩 Total chunks: {len(all_chunks)}")

    # Generate embeddings (in batches to avoid exceeding the service timeout)
    print("🔄 Generating embeddings...")
    contents = [c for _, _, c in all_chunks]
    vectors: list[list[float]] = []
    batch = 16
    for i in range(0, len(contents), batch):
        part = contents[i:i + batch]
        vectors.extend(embedder.embed(part))
        print(f"  ... {min(i + batch, len(contents))}/{len(contents)}")
    print(f"✅ Embeddings generated: {len(vectors)} (dim={len(vectors[0]) if vectors else 0})")

    # Persist to DB
    db = SessionLocal()
    try:
        # Register/get the subject
        if args.subject_id:
            subject = db.get(Subject, uuid.UUID(args.subject_id))
            if subject is None:
                subject = Subject(id=uuid.UUID(args.subject_id), name=args.name)
                db.add(subject)
        else:
            subject = Subject(name=args.name)
            db.add(subject)
            db.flush()  # to get the id

        # Clear previous chunks if requested
        if args.clear:
            db.query(MaterialChunk).filter(MaterialChunk.subject_id == subject.id).delete()

        # Insert chunks
        for (src, idx, content), vec in zip(all_chunks, vectors):
            db.add(MaterialChunk(
                subject_id=subject.id,
                source_file=src,
                chunk_index=idx,
                content=content,
                embedding=vec,
            ))
        db.commit()
        print(f"\n💾 Saved {len(all_chunks)} chunks for the subject '{subject.name}' (id={subject.id})")
    finally:
        db.close()


if __name__ == "__main__":
    main()

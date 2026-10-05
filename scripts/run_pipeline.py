"""Runs the full exam generation pipeline with a test subject.

Usage:
    python scripts/run_pipeline.py

This script:
  1. Loads the materials of the subject "Applied Economics" (data/inputs).
  2. Builds a realistic ExamBlueprint with Bloom, difficulty and topic
     distributions.
  3. Runs the full LangGraph graph (ingestor → ... → compiler).
  4. Shows a summary of the result and saves the generated PDF.
"""
import glob
import json
import os
import sys
from pathlib import Path

# Asegura que el módulo `src` sea importable desde la raíz del proyecto.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents_backend.exam_pipeline.graph import run_exam_pipeline  # noqa: E402
from core.domain.schemas.exam import (  # noqa: E402
    BloomLevel,
    Difficulty,
    ExamBlueprint,
)
from core.infrastructure.latex.templates.registry import TemplateId  # noqa: E402

BASE_DIR = Path("data/inputs/Economia_Aplicada")


def load_materials() -> list[str]:
    """Returns the paths of the subject's materials (all formats)."""
    patterns = [
        "Apuntes/*.pdf",
        "Apuntes/*.docx",
        "Apuntes/*.pptx",
        "Filminas/*.pdf",
        "Filminas/*.pptx",
        "Practica/*.pdf",
    ]
    files: list[str] = []
    for pat in patterns:
        files.extend(str(p) for p in glob.glob(str(BASE_DIR / pat)))
    # Deduplicate and sort
    return sorted(set(files))


def build_blueprint(total_questions: int = 8) -> ExamBlueprint:
    """Builds a realistic blueprint for Applied Economics."""
    return ExamBlueprint(
        subject_id="economia-aplicada-test",
        total_questions=total_questions,
        bloom_distribution={
            BloomLevel.REMEMBER: 0.25,
            BloomLevel.UNDERSTAND: 0.25,
            BloomLevel.APPLY: 0.25,
            BloomLevel.ANALYZE: 0.25,
        },
        difficulty_distribution={
            Difficulty.EASY: 0.4,
            Difficulty.MEDIUM: 0.4,
            Difficulty.HARD: 0.2,
        },
        topics_weight={
            "Estudio de Mercado": 0.3,
            "Flujos Financieros": 0.3,
            "Análisis Económico-Financiero": 0.25,
            "Fijación de Precios": 0.15,
        },
        estimated_duration_minutes=90,
    )


def main() -> None:
    materials = load_materials()
    print(f"📚 Materials loaded: {len(materials)} files")
    for m in materials:
        print(f"   - {Path(m).name}")

    # Register/get the subject in the DB (for persistence and RAG)
    from core.infrastructure.db.connection import SessionLocal
    from core.domain.models import Subject

    db = SessionLocal()
    try:
        subject = db.query(Subject).filter(Subject.name == "Applied Economics").first()
        if subject is None:
            subject = Subject(name="Applied Economics")
            db.add(subject)
            db.commit()
            db.refresh(subject)
            print(f"\n🆕 Subject registered in DB: id={subject.id}")
        else:
            print(f"\n✅ Existing subject in DB: id={subject.id}")
        subject_id = str(subject.id)
    finally:
        db.close()

    blueprint = build_blueprint(total_questions=8)
    blueprint.subject_id = subject_id
    print(f"\n📋 Blueprint: {blueprint.total_questions} questions")
    print(f"   Bloom: { {k.value: v for k, v in blueprint.bloom_distribution.items()} }")
    print(f"   Difficulty: { {k.value: v for k, v in blueprint.difficulty_distribution.items()} }")

    print("\n🚀 Running pipeline...")
    result = run_exam_pipeline(
        subject_id=subject_id,
        subject_name="Applied Economics",
        template_id=TemplateId.BASE_EXAM,
        raw_materials_paths=materials,
        blueprint=blueprint,
    )

    print("\n=== RESULT ===")
    print(f"Status: {result.get('status')}")
    print(f"Error: {result.get('error_message')}")
    print(f"Indexed chunks: {result.get('indexed_chunks_count')}")
    print(f"Approved items: {len(result.get('approved_items', []))}")
    print(f"Rejections: {len(result.get('rejection_log', []))}")
    print(f"LLM calls: {result.get('total_llm_calls')}")
    print(f"Compilation attempts: {result.get('compilation_attempts')}")

    # Save summary to JSON for inspection
    out_dir = Path("data/agent_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "status": result.get("status"),
        "error_message": result.get("error_message"),
        "indexed_chunks_count": result.get("indexed_chunks_count"),
        "approved_items": [i.model_dump() for i in result.get("approved_items", [])],
        "rejection_log": result.get("rejection_log", []),
        "total_llm_calls": result.get("total_llm_calls"),
        "compilation_attempts": result.get("compilation_attempts"),
        "compilation_log": result.get("compilation_log", []),
        "pdf_path": result.get("compiled_exam").pdf_path if result.get("compiled_exam") else None,
    }
    summary_path = out_dir / "pipeline_result.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n📄 Summary saved to: {summary_path}")

    if result.get("compiled_exam") and result["compiled_exam"].pdf_path:
        print(f"✅ PDF generated at: {result['compiled_exam'].pdf_path}")


if __name__ == "__main__":
    main()

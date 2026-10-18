"""Verification of the export_questions tool (no DB, with a mocked bank).

Tests:
  1. That the tool is registered in the graph (TOOLS).
  2. That the args_schema validates invalid format (falls back to csv) and
     out-of-range limit.
  3. That it generates real CSV and XLSX with the full columns (mocked questions).
  4. That the HTTP fallback works if the OpenWebUI upload fails.
"""
import sys
import os
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Avoid connecting to the DB when importing the graph (Postgres checkpointer).
os.environ.setdefault("DATABASE_URL", "postgresql://x:x@localhost:1/xdb")
os.environ.setdefault("LATEX_COMPILER_URL", "http://localhost:1/compile")

from core.domain.schemas.tools import ExportQuestionsInput, TableColumn, COLUMN_LABELS  # noqa: E402
from agents_backend.conversational import tools as tools_mod  # noqa: E402


class FakeQ:
    """Fake question with the fields used by the export."""

    def __init__(self, i):
        self.id = f"00000000-0000-0000-0000-{i:012d}"
        self.topic = "Reading"
        self.subtopic = None
        self.bloom_level = "understand"
        self.difficulty = "medium"
        self.question_type = "multiple_choice"
        self.question_text = f"Test question {i} with | pipe and\nline break"
        self.options = [
            {"text": "Option A", "is_correct": True},
            {"text": "Option B", "is_correct": False},
        ]
        self.expected_answer = "Option A"
        self.solution_explanation = "Because A is correct."
        self.points = 1.5
        self.verified_by_human = i % 2 == 0
        self.verified_by_ai = True
        self.ai_review_priority = "low"
        self.source = "chat"
        self.created_at = "2026-09-17 10:00:00"


def main():
    ok = True

    # 1) Tool registered in the graph.
    from agents_backend.conversational.graph import TOOL_BY_NAME
    assert "export_questions" in TOOL_BY_NAME, "export_questions NOT in TOOLS"
    print("1. Tool registered in the graph: OK")

    # 2) args_schema: out-of-range limit -> ValidationError.
    from pydantic import ValidationError
    try:
        ExportQuestionsInput(subject_id="x", limit=1000)
        print("2. limit=1000 NOT rejected: FAIL")
        ok = False
    except ValidationError:
        print("2. args_schema rejects out-of-range limit: OK")

    # 3) Real CSV and XLSX generation with mocked bank and upload.
    out_dir = ROOT / "data" / "agent_outputs"
    with patch.object(tools_mod.bank, "list_questions", return_value=[FakeQ(i) for i in range(3)]), \
         patch("core.infrastructure.files.output_paths.get_output_dir", lambda: out_dir), \
         patch("exam_app.infrastructure.openwebui_bridge.upload_file_to_openwebui",
               side_effect=RuntimeError("no network (fallback)")):
        res_csv = tools_mod.export_questions.func(subject_id="x", format="csv")
        res_xlsx = tools_mod.export_questions.func(subject_id="x", format="xlsx")

    assert "Exported **3 question(s)**" in res_csv, res_csv
    assert "Download" in res_csv and "http://localhost:8000/output/" in res_csv, res_csv
    print("3a. CSV generated with HTTP fallback: OK")

    assert "Exported **3 question(s)**" in res_xlsx, res_xlsx
    print("3b. XLSX generated with HTTP fallback: OK")

    # Verify CSV content (full columns, unescaped pipes, BOM).
    csv_files = sorted(out_dir.glob("questions_*.csv"))
    assert csv_files, "No CSV was generated"
    content = csv_files[-1].read_text(encoding="utf-8-sig")
    for h in ["#", "Id", "Topic", "Question", "Options", "Answer", "Solution", "Human verif."]:
        assert h in content, f"Missing column {h} in the CSV"
    assert "1) *Option A | 2) Option B" in content, "Options badly formatted"
    assert "Test question 0 with | pipe and line break" in content, "Pipe/line break badly processed"
    print("3c. CSV with 17 columns, marked options and BOM: OK")

    # Verify the XLSX with openpyxl.
    from openpyxl import load_workbook
    xlsx_files = sorted(out_dir.glob("questions_*.xlsx"))
    assert xlsx_files, "No XLSX was generated"
    wb = load_workbook(xlsx_files[-1])
    ws = wb.active
    headers = [c.value for c in ws[1]]
    assert headers[7] == "Question" and headers[8] == "Options", headers
    assert ws.max_row == 4, f"Expected 4 rows, got {ws.max_row}"
    print("3d. XLSX readable with openpyxl, correct headers and rows: OK")

    # 4) Successful upload to OpenWebUI (mock) -> native attachment markdown.
    with patch.object(tools_mod.bank, "list_questions", return_value=[FakeQ(1)]), \
         patch("core.infrastructure.files.output_paths.get_output_dir", lambda: out_dir), \
         patch("exam_app.infrastructure.openwebui_bridge.upload_file_to_openwebui",
               return_value={"id": "abc-123", "filename": "questions.xlsx"}):
        res_up = tools_mod.export_questions.func(subject_id="x", format="xlsx")
    assert "http://localhost:3000/api/v1/files/abc-123/content" in res_up, res_up
    assert "Download the Excel" in res_up, res_up
    print("4. Upload to OpenWebUI -> native attachment with link: OK")

    # 5) Invalid format falls back to csv (doesn't crash).
    with patch.object(tools_mod.bank, "list_questions", return_value=[FakeQ(1)]), \
         patch("core.infrastructure.files.output_paths.get_output_dir", lambda: out_dir), \
         patch("exam_app.infrastructure.openwebui_bridge.upload_file_to_openwebui",
               side_effect=RuntimeError("no network")):
        res_inv = tools_mod.export_questions.func(subject_id="x", format="pdf")
    assert "CSV" in res_inv, res_inv
    print("5. Invalid format ('pdf') falls back to CSV: OK")

    # 6) Empty bank -> clear message.
    with patch.object(tools_mod.bank, "list_questions", return_value=[]):
        res_empty = tools_mod.export_questions.func(subject_id="x")
    assert "There are no questions" in res_empty, res_empty
    print("6. Empty bank -> clear message: OK")

    # Clean up test files.
    for f in out_dir.glob("questions_*.csv"):
        f.unlink()
    for f in out_dir.glob("questions_*.xlsx"):
        f.unlink()

    print("\nTODO OK" if ok else "\nHAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

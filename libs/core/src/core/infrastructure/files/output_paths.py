"""Rutas de salida compartidas (PDFs de exámenes, exportaciones CSV/XLSX).

El directorio de salida se comparte con el latex-compiler vía volumen y es
servido por exam-app en `GET /output/{filename}`.

Resolución (en orden):
  1. `/app/output` (contenedor: volumen compartido con latex-compiler).
  2. `data/agent_outputs` relativo a la raíz del repo (desarrollo local).
"""
from __future__ import annotations

import os
from pathlib import Path

_CANDIDATE_OUTPUT = [
    Path("/app/output"),  # contenedor (volumen compartido con latex-compiler)
    Path(__file__).resolve().parents[6] / "data" / "agent_outputs",  # desarrollo local
]


def get_output_dir() -> Path:
    """Devuelve el directorio de salida, creándolo si no existe."""
    env = os.environ.get("EXAM_OUTPUT_DIR", "")
    if env:
        out = Path(env)
    else:
        out = next((p for p in _CANDIDATE_OUTPUT if p.exists()), _CANDIDATE_OUTPUT[-1])
    out.mkdir(parents=True, exist_ok=True)
    return out

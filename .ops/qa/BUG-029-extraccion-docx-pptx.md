---
id: BUG-029
tipo: Defect
type: Defect
title: Indexacion docx/pptx falla en contenedor por dependencias no declaradas
description: extract_file soporta .docx/.pptx pero python-docx/python-pptx no estan en la imagen de exam_app; el endpoint /subjects/{id}/index responde 400 y no reindexa nada.
estado: corregido          # abierto | corregido | verificado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [QT-011]        # QT que lo detecto
status: draft
---

## Evidencia

Ronda 11, materia Economia Aplicada - QA11 (51 chunks antes):
POST /subjects/6c9e3cc3-.../index con materials
["/app/inputs/Economia_Aplicada/Apuntes/*.docx"], clear=true ->
HTTP 400 {"detail":"Could not extract text"}. Log del contenedor
(docker logs exam_app):
`⚠️ .../2. MODULO 2 - Actividades (29-04-26) .docx: No module named 'docx'`
`⚠️ .../Actividades 1 y 2 del MODULO 2 (22-04-26).docx: No module named 'docx'`
Chunks en BD despues del intento fallido: 51 (sin perdida).
Con solo un docx inexistente: HTTP 400 {"detail":"No files found"}.

## Causa

projects/exam-app/src/exam_app/scripts/index_material.py::extract_file
intenta extraer texto de .docx/.pptx (librerias python-docx /
python-pptx), pero ningun manifest las declara: exam-app/pyproject.toml
(mvp-exam-app, deps solo mvp-core, mvp-agents-backend, fastapi, uvicorn,
python-multipart, pyjwt) ni core/pyproject.toml (mvp-core). La imagen se
construye sin ellas; en runtime falla el import -> la excepcion se captura
por archivo como warning, y si todos los archivos fallan el endpoint
responde 400. Nota: con clear=true los chunks existentes se conservan
porque la validacion (extract/embed) ocurre ANTES del borrado.

## Fix y verificacion

Fix aplicado (ronda 11): python-docx>=1.1.0 y python-pptx>=1.0.0
declarados en requirements.txt (raiz) y en los pyproject de mvp-core y
mvp-exam-app (pymupdf y openpyxl tambien formalizados ahi). Rebuild de
la imagen exam-app y recreacion del contenedor.

Verificacion real (2026-10-28, contenedor reconstruido):
- Paquetes en contenedor: docx 1.2.0, pptx 1.0.2, PyMuPDF 1.28.5,
  openpyxl 3.1.5.
- POST /subjects/{id}/index con solo *.docx -> HTTP 200,
  {"indexed_chunks": 4}; chunks en BD 51 -> 4 (clear=true borra y
  reinserta, sin 400).
- POST con solo *.pptx -> HTTP 200, {"indexed_chunks": 40}.
- POST con *.pdf+*.docx+*.pptx -> HTTP 200, {"indexed_chunks": 85}
  (41 PDF, 4 docx, 40 pptx), sin warnings en el log del contenedor.
- Repro script: scripts/qa_r11_docx_index.py.

Pendiente: verificacion humana (rol:propietario) para pasar a
"verificado".

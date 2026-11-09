---
id: BUG-021
tipo: Defect
type: Defect
title: El flag persist=false de POST /exams/generate no evita la persistencia del examen (fila BD + PDFs + ZIP)
description: persist solo controla guardar las preguntas aprobadas; el nodo de compilacion escribe la fila en exams, los PDFs y el ZIP siempre.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-001, IMPL-021, BUG-018]
status: draft
---

## Evidencia

Ronda 6 (2026-10-27). La sonda 2 de BUG-018 (metadata anidada, generacion
valida) se envio explicitamente con `persist: false`. Verificado despues:

- `GET /subjects/{sid}/exams` (nginx, Accept json): la lista contiene el
  examen `f4a744b6-fccc-4916-bd10-1b9172023bde` creado 2026-10-27 15:56:46
  (exactamente el momento de la sonda).
- BD: fila con `name=SondaR6Anidada`, `num_versions=2`, 4 nombres de PDF y
  `zip_path=SondaR6Anidada.zip`.
- La vista Exams del frontend lo listaba como "SondaR6Anidada - 2 questions".

## Causa

En `agents_backend/exam_pipeline/graph.py::run_exam_pipeline`, el flag
`persist` solo envuelve a `persist_generated_items` (guardar las preguntas
aprobadas en `generated_questions`). La persistencia del EXAMEN ocurre antes,
dentro del nodo de compilacion/finalizacion
(`exam_pipeline/nodes.py` ~linea 627): `db.add(ExamModel(...))` + renombrado
de PDFs + creacion del ZIP se ejecutan incondicionalmente para toda
generacion exitosa, sin consultar `persist`. El docstring del endpoint
("every generation is persisted") confirma que es un comportamiento deseado
por el producto, pero entonces el campo `persist` es enganoso para clientes
REST: un `persist=false` deja igualmente artefactos y fila.

## Fix y verificacion

Pendiente de decision de producto (RFC-14 propuesta):

- (a) Respetar el flag: en el nodo de finalizacion, si `persist=false`,
  omitir `db.add`, renombrado y ZIP (o limpiarlos al final del pipeline).
- (b) Quitar el flag del schema y documentar que toda generacion persiste
  (coherente con "professor request"); la sonda de QA usaria un subject
  desechable.

Verificacion propuesta (a): sonda con persist=false y luego
`GET /subjects/{sid}/exams` SIN el examen nuevo y sin PDFs/ZIP en /output;
(b): el campo se elimina del API (breaking, documentar en changelog).

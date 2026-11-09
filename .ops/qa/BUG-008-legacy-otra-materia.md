---
id: BUG-008
tipo: Defect
type: Defect
title: Examenes legacy de otra materia aparecen en el historial
description: Multi-tenant roto a nivel de vista; el fallback legacy listaba PDFs de cualquier materia.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): con Base de Datos activa, la vista Exams listaba `Parcial_1_A/B`
(generados para Economia Aplicada, segun `Parcial_1.json`) y 30+ PDFs con nombre UUID de
corridas antiguas del pipeline batch. Historial contaminado y confuso entre materias.

## Causa

`exam_app/api/v1/exams.py::list_subject_exams`: el fallback "legacy" lista todos los PDFs
del directorio de salida no persistidos en BD, sin filtrar por materia (el nombre de
archivo no contiene subject_id).

## Fix y verificacion

Fix 11.2 (ronda 2, variante de RFC-05): agrupado por nombre base (strip de
`_respondido`, `_with_answers`, `_v\d+`, `_[A-J]`), ZIP buscado en `{base}.zip`/
`exam_{base}.zip`, y filtro de huerfanos (legacy sin ZIP y sin items no se listan).
Verificado en ronda 2 (P7-P8): 37 -> 8 registros, uno por examen, solo boton ZIP. La
migracion completa a tabla queda en BL-014.
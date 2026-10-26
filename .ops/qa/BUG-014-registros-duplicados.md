---
id: BUG-014
tipo: Defect
type: Defect
title: Registros duplicados de examenes (uno por PDF en vez de uno por examen)
description: La vista Exams listaba 37 registros basura; variantes A/B y huerfanos UUID.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-002, IMPL-015]
status: stable
---

## Evidencia

Ronda 2 (2026-10-23): la vista Exams listaba un registro por PDF individual (variantes
A/B, respondido, with_answers, v1/v2) en vez de uno por examen; 26 PDFs huerfanos UUID de
corridas pre-persistencia creaban registros basura (37 en total).

## Causa

El fallback legacy de `list_subject_exams` agrupaba por prefijo exacto del filename;
`Parcial_1_A`, `Parcial_1_A_respondido` y `Parcial_1_B` eran registros separados.

## Fix y verificacion

Agrupado por nombre base (regex strip de sufijos), ZIP en `{base}.zip`/`exam_{base}.zip`,
filtro de huerfanos (sin ZIP y sin items); frontend elimina botones por PDF y `pdfLabel`,
solo boton ZIP por examen con fallback al primer PDF. Verificado en ronda 2 (P7-P9): 37
-> 8 registros, descarga ZIP 200 (64 KB). Re-verificado en ronda 3 (BUG-13/14
re-verificados). Migracion completa en BL-014.
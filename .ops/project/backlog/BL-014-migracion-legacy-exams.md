---
id: BL-014
tipo: BacklogItem
type: BacklogItem
title: Migracion de examenes legacy a la tabla exams
description: Los PDFs legacy sin subject_id requieren migracion one-shot para salir del fallback.
estado: idea
dueno: rol:propietario
fecha: 2026-10-22
relaciona: [REQ-001]
status: draft
---

## Descripcion

RFC-05 (ronda 1, parcialmente cubierto en la ronda 2 por el agrupado por base y el filtro
de huerfanos): migrar los PDFs legacy del output dir a la tabla `exams` con su
`subject_id` real inferido del JSON hermano, y eliminar el fallback de listado. Los 26
huerfanos UUID siguen en `/app/output` sin listarse. Deuda heredada listada en el backlog
de la ronda 3.

## Criterio de salida

El listado de examenes solo lee de la tabla `exams`; los artefactos legacy quedan
asignados a su materia o fuera del listado, visibles solo via `/output/`.

## IMPL

IMPL-015
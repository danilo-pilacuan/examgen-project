---
id: BL-023
tipo: BacklogItem
type: BacklogItem
title: Tercera revision - fechas de verificacion y tipos de pregunta restringibles
description: Items A1 y A2 de Requisitos/tercera_revision_Felipe.md; A2 extendido con distribucion custom de Bloom/dificultad y retrieval (capacidad extendida).
estado: hecho
dueno: rol:propietario
fecha: 2026-11-05
relaciona: [REQ-001, BL-022]
status: draft
---

## Descripcion

Del analisis de la tercera revision de Felipe (Requisitos/tercera_revision_items.md)
el propietario aprobo implementar A1 y A2; A2 en version extendida.

- A1: el Question Bank muestra fecha de creacion y de verificacion por pregunta.
  `created_at` ya existia (no visible en UI); `verified_at` es columna nueva con
  migracion Alembic (head c9d0e1f2a3b4), sellada al verificar (IA en creacion,
  humano via toggle) y a NULL al quitar la verificacion.
- A2 (extendido): checkboxes de tipos de pregunta en el formulario Generate
  (`allowed_question_types` en ExamBlueprint, default los 6 tipos; lista vacia
  rechazada 422 por BUG-018 extra=forbid), el planner filtra su eleccion por el
  conjunto permitido con fallback determinista, y un panel avanzado expone
  distribucion custom de Bloom/dificultad y retrieval (use_rag, top_k, min_score).

Fuera de alcance: A3/A4, B1/B2, C1-C5 (pospuestos por el propietario).

## Criterio de salida

Columnas de fechas visibles en BankView; generate() envia allowed_question_types
y el planner solo elige tipos permitidos; lista vacia rechazada; validacion
estatica verde (tsc, vue-tsc, build, py_compile, AST) y caso de rechazo ejecutado.

## IMPL

IMPL-030

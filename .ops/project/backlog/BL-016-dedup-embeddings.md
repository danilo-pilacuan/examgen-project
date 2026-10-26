---
id: BL-016
tipo: BacklogItem
type: BacklogItem
title: Deduplicacion por embeddings en el pipeline
description: dedup_similarity_threshold sigue siendo overlap de tokens; pasar a embeddings reales.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

Deuda tecnica de la ronda 1: `dedup_similarity_threshold` opera por solapamiento de tokens
(placeholder declarado en el codigo y anotado en ARCHITECTURE.md como pendiente). Paso a
similitud de embeddings reales (bge-m3 ya disponible). Relacionado con BL-007 pero a
nivel de pipeline, no de guardado manual.

## Criterio de salida

El umbral de dedup se calcula con embeddings; campanas de evaluacion y QA no muestran
temas duplicados entre items aprobados.

## IMPL

IMPL-014
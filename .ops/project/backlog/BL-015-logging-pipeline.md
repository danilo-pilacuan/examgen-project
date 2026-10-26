---
id: BL-015
tipo: BacklogItem
type: BacklogItem
title: Logging estructurado de errores silenciosos del pipeline
description: generator_node/evaluator_node tragan excepciones; usar el contexto pipeline del audit log.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

Deuda tecnica sin ticket de la ronda 1: `evaluator_node`/`generator_node` convertian
excepciones en rechazos silenciosos (causa de BUG-004). El fail-fast de RFC-04 ya
loguea `pipeline:generator_error`/`pipeline:evaluator_error` en `llm_responses` (fix
aplicado); falta el logging estructurado general de la deuda (contexto `pipeline:*`
reutilizado para errores) y revisar la politica de `max_total_llm_calls = 200` al
escalar examenes grandes con reintentos.

## Criterio de salida

Toda excepcion dentro de los nodos queda registrada con contexto en el audit log; la
politica de llamadas maximas documentada para examenes de 50 preguntas.

## IMPL

IMPL-014
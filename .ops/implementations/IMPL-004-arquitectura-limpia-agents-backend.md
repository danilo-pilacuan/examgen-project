---
id: IMPL-004
tipo: Implementation
type: Implementation
title: Arquitectura limpia agents-backend core
description: Conversational graph, exam pipeline y shared kernel desacoplados del consumidor.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-16
relaciona: [BL-002, IMPL-002]
status: stable
---

## Alcance

Incluye: agents-backend con grafo conversacional (tools HITL, guardrails, pending store)
y pipeline de examenes (generator/evaluator/assembler/compiler), mas el shared kernel
(events, retrieval, llm) desacoplado del consumidor exam-app. No incluye: core
(shared kernel de modelos SQLAlchemy, IMPL-011 lo referencia).

## Diseno

El framework de evaluacion (IMPL-018) se apoya en esta estructura: `test/evaluation/src/
_patch.py` activa stubs/real por monkey-patching de nodes + shared_llm, lo que solo fue
posible por el desacople de capas. Verificado E2E; pipeline fail-fast anadido en
BUG-004.
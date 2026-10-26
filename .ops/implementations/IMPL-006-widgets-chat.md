---
id: IMPL-006
tipo: Implementation
type: Implementation
title: Widgets de chat
description: QuestionCard, ToolActivity, MarkdownRenderer y artefactos dentro del stream.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-17
relaciona: [BL-001, IMPL-005]
status: stable
---

## Alcance

Incluye: widgets renderizados dentro del stream del chat (QuestionCard con acciones
Save/Save & verify, tool-cards de actividad, MarkdownRenderer con tablas scrolleables) y
artefactos (card de ZIP al terminar un examen). No incluye: pantallas fuera del chat
(IMPL-007).

## Diseno

QuestionCard consume el contrato HITL (token en body, BUG-001); las tablas markdown
scrollean dentro de la burbuja (ISS-10, fix 11.6); las tool-cards listan las tools del
turno (el ancho en viewports chicos queda en BL-012). Verificado E2E; C7/C13 certificados
en la ronda 3.
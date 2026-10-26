---
id: REQ-001
tipo: Requirement
type: Requirement
title: Flujo central del profesor (MVP)
description: Un profesor genera examenes LaTeX por chat con agente e HITL, con versiones con y sin respuestas.
estado: aprobado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [BL-001, BL-002, BL-003, BL-004, BL-005, BL-006, BL-007, BL-008, BL-009]
status: stable
sources: [{ id: copilot-instructions, resource: ../../.github/copilot-instructions.md, title: copilot-instructions }]
---

## Requisito

El sistema debe permitir, solo con el navegador: iniciar sesion (multi-profesor JWT),
registrar y activar materias, subir e indexar material (PDF -> chunks + embeddings),
generar y verificar preguntas por chat con human-in-the-loop (texto y botones del
QuestionCard), generar examenes (por chat o formulario) con versiones anti-copia y
descargar el ZIP. Derivado del caso de uso central certificado en las rondas QA
(antiguo 10-qa-flujo-completo-navegador, hoy BUG-001..BUG-017b en qa/).

## Criterio de aceptacion

Flujo completo certificado E2E en navegador: login -> materia -> material -> 3 preguntas
HITL -> examen -> descarga ZIP con las 2 versiones (definicion de "hecho" del backlog P0
de la ronda 1). Verificaciones por ronda en `../qa/traceability.md`.

## No objetivos

El pipeline batch (pre-agente), el webui de desarrollo (exam_open_webui) y la optimizacion
de hiperparametros (REQ-002).
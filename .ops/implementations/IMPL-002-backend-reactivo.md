---
id: IMPL-002
tipo: Implementation
type: Implementation
title: Backend reactivo exam-app
description: FastAPI con chat SSE, auth JWT, REST de subjects/bank/exams/material y salida LaTeX.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-16
relaciona: [BL-002, IMPL-003, IMPL-011]
status: stable
---

## Alcance

Incluye: exam-app (FastAPI :8000) con SSE de chat, auth multi-profesor JWT, REST
(subjects, bank, exams, material), integracion con latex-compiler y `/output/` para
artefactos. Sub-tareas 2.1-2.7 completadas. No incluye: token streaming real por tokens
(backlog BL-002); el turno llega como un solo bloque al final.

## Diseno

SSE sobre `/api/chat`; el token viaja en el body del POST (limitacion de SSE en
navegador, sin headers); el contracto de eventos vive en 3 capas
(agents_backend/shared/events.py -> exam_app/schemas/events.py ->
frontend/src/types/events.ts). Verificado E2E en las rondas QA; el streaming real queda
para post-RC.
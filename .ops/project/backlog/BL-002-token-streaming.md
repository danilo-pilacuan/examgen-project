---
id: BL-002
tipo: BacklogItem
type: BacklogItem
title: Token streaming real por tokens
description: Hoy el turno del agente llega como un solo bloque al final; emitir tokens incrementales.
estado: idea
dueno: rol:propietario
fecha: 2026-10-20
relaciona: [REQ-001]
status: draft
---

## Descripcion

El SSE emite el turno completo como un unico token al finalizar (backlog de la etapa 02,
punto 2.5). El streaming real por tokens mejoraria la percepcion de latencia del chat.
Deriva del alcance de la etapa 02 (backend reactivo) dejado explicitamente pendiente.

## Criterio de salida

La burbuja del chat crece incrementalmente durante la generacion, sin romper el contrato
SSE de 3 capas (shared/events.py -> exam_app/schemas -> frontend/types).

## IMPL

IMPL-002
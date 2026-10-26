---
id: BL-005
tipo: BacklogItem
type: BacklogItem
title: Paginacion o virtualizacion del Banco y del historial del chat
description: El banco (limit 200) y la lista de mensajes no escalan a bancos/historiales grandes.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

Dos issues de la ronda 1: ISS-03 (BankView renderiza la tabla completa con limit default
200; no escala a bancos de miles) e ISS-04 (MessageList renderiza todos los mensajes y
widgets; tras ~30 turnos los snapshots se vuelven lentos; las conversaciones crecen sin
limite y degradan el DOM). Agrupados por ser el mismo patron de virtualizacion.

## Criterio de salida

Paginacion server-side o virtualizacion en BankView; historial del chat virtualizado o
paginado con widgets antiguos colapsados a resumen; sin degradacion perceptible con
200+ preguntas y 30+ turnos.

## IMPL

IMPL-013
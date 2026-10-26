---
id: BL-011
tipo: BacklogItem
type: BacklogItem
title: Conteo del agente debe reflejar la BD real
description: La herramienta de conteo responde con el estado de sesion, no con el total del banco.
estado: idea
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001]
status: draft
---

## Descripcion

Al preguntar "How many questions are in the bank?" el agente responde con su estado de
sesion (1 pregunta por materia, total 6) mientras la BD tiene 21 en Base de Datos
(OBS-4/ISS-18, ronda 4). Divergencia de semantica entre conversacion y banco que puede
confundir al docente.

## Criterio de salida

La herramienta de conteo consulta la BD (agregado por materia) y el chat coincide con el
Bank; tool-cards alineadas con la respuesta.

## IMPL

IMPL-019
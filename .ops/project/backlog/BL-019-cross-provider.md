---
id: BL-019
tipo: BacklogItem
type: BacklogItem
title: Comparativa cross-provider del framework de evaluacion
description: Anadir perfiles OpenAI/DeepSeek en models.yaml y re-ejecutar E01-E04 comparando.
estado: idea
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-002]
status: draft
---

## Descripcion

Pendiente #1 de la etapa 15: anadir perfil de proveedor nuevo en `models.yaml` + brazo con
`model_profile` distinto; re-ejecutar E01-E04 y comparar (todo lo demas identico).
Depende de acceso a otro modelo en el gateway USFQ (decision externa, fuera de control
local).

## Criterio de salida

Tabla comparativa entre proveedores con las 6 familias de metricas; conclusiones
documentadas en FINDINGS.md de cada experimento.

## IMPL

IMPL-018
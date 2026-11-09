---
id: BL-021
tipo: BacklogItem
type: BacklogItem
title: Tests unitarios de metricas del framework
description: Hoy el framework se valida por ejecucion; pytest unitario de metricas es opcional y barato.
estado: idea
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-002]
status: draft
---

## Descripcion

Pendiente #3 de la etapa 15: tests automatizados del framework. Hoy validado por
ejecucion real; podria anadirse pytest unitario de metricas (quality/diversity/rag/bloom/
cost) a bajo costo. Opcional; no bloquea el escrito. Nota: la regla "sin pytest" aplica al
producto (exam-app/frontend), no a `test/evaluation/`.

## Criterio de salida

Suite unitaria de metricas con fixtures minimos corre en local sin red ni coste.

## IMPL

IMPL-018
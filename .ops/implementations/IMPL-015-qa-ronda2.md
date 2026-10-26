---
id: IMPL-015
tipo: Implementation
type: Implementation
title: QA ronda 2 - persistencia y registros de examenes
description: Fixes BUG-013/014 (historial de chat, un registro por examen) certificados E2E (2026-10-23).
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-002, IMPL-014, IMPL-016]
status: stable
---

## Alcance

Incluye: correccion y certificacion de los 2 bugs reportados tras la ronda 1 (BUG-013
conversaciones no persisten; BUG-014 registros duplicados de examenes), con 3 capas de
fix (endpoint de historial, servicio + engine, hidratacion en frontend) y reglas de
validacion sin pytest/vitest. No incluye: commits atomicos de la ronda (BL-018, a
verificar) ni tag V1.1.0 (el historial de tags sugiere que ya existe V1.1.0).

## Diseno

El endpoint de historial delega en el checkpointer de LangGraph (no duplica
almacenamiento; thread sin checkpoints -> lista vacia). Los 26 PDFs huerfanos UUID no se
borran; dejan de listarse (migracion futura en BL-014). Verificado E2E (P1-P9, R1-R3):
threads persisten tras logout/login, contenido hidratado, 37 -> 8 registros, ZIP 200.
Los metadatos de threads siguen en localStorage; tabla threads en BL-017.
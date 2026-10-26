---
id: IMPL-003
tipo: Implementation
type: Implementation
title: Arquitectura limpia en exam-app
description: Capas domain/services/infrastructure/api en exam-app con puertos e inyeccion.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-16
relaciona: [BL-002, IMPL-002]
status: stable
---

## Alcance

Incluye: reorganizacion de exam-app en capas limpias (domain, services, infrastructure,
api) con puertos e inyeccion de dependencias, y separacion del engine LangGraph como
detalle de infraestructura. No incluye: agents-backend (IMPL-004).

## Diseno

`domain/ports.py` define los puertos (SSE frames, engine); `services/chat_engine.py`
orquesta; `infrastructure/langgraph_engine.py` implementa con PostgresSaver como
checkpointer; `api/v1/` expone routers. Beneficio directo observado: el heartbeat SSE
(RFC-02) se propagto sin romper capas al cambiar `Union[SSEEvent, str]` en ports ->
engine -> service -> router. Verificado E2E en rondas QA.
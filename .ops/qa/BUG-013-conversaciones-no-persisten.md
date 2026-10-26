---
id: BUG-013
tipo: Defect
type: Defect
title: Conversaciones no persisten al cerrar sesion
description: Tras re-login a veces solo el nombre del hilo; el contenido vivia solo en Pinia.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-002, IMPL-015]
status: stable
---

## Evidencia

Ronda 2 (2026-10-23): al iniciar sesion de nuevo no se veian las conversaciones; a veces
solo los nombres pero el chat cargaba vacio. BD: el checkpointer `PostgresSaver` si
persistia el grafo (thread `7f2f53c0`, 47 filas en `checkpoints`) pero no existia ninguna
API para leerlo; los metadatos de threads viven en `localStorage` (`mvp_chat_threads`).

## Causa

El contenido de los mensajes vivia solo en memoria Pinia; no habia endpoint de historial.

## Fix y verificacion

Nuevo endpoint `GET /api/chat/history/{thread_id}` autenticado; `ChatService.history()` ->
`LangGraphEngine.history()` lee `get_state` del grafo y serializa mensajes (filtra
system/tool, maneja multimodal); `loadThread()` async en el store hidrata `messages` con
guard anti-carrera; ChatView restaura la ultima conversacion al montar. Verificado en
ronda 2 (P1-P6): logout/login preserva 2 threads, contenido hidratado completo,
`checkpoints` 47 -> 50 filas. Re-verificado en ronda 3.
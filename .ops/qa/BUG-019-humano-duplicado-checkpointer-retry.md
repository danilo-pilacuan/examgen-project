---
id: BUG-019
tipo: Defect
type: Defect
title: El mensaje del usuario se duplica en el checkpointer al reintentar un turno abortado
description: Cada POST /api/chat/stream reinserta el HUMAN en el historial; tras un abort + Retry el mensaje del usuario queda 2 veces en el hilo.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-001, C8, IMPL-022]
status: draft
---

## Evidencia

Ronda 6 (2026-10-27, navegador + curl + BD). Flujo reproducido en la UI:

1. Envie "Genera una pregunta de opcion multiple sobre pilas y colas..." al
   thread `0afd6caa-3b7f-49db-951d-64387cfe176a` y aborte la respuesta a los
   ~1.5 s (parche de `window.fetch` + AbortController -> `net::ERR_ABORTED`).
   La burbuja quedo `failed=true` con aviso y boton "↻ Retry" (C8 OK).
2. Click en Retry: el turno completo, la burbuja se rehidrato con el contenido
   completo desde el checkpointer (RFC-11 OK, sin duplicar el CONTENIDO de la
   respuesta). PERO el historial del backend quedo con el mensaje HUMAN
   duplicado: indices [8] y [9] del `GET /api/chat/history/{thread_id}`, ambos
   `{"role":"user","content":<mismo texto, 80 chars>}`.
3. Sonda curl independiente confirmo el mecanismo: dos POST consecutivos a
   `/api/chat/stream` con el MISMO `thread_id` y el mismo texto pasaron de 11
   a 13 mensajes persistidos (el segundo POST inserto el HUMAN otra vez).

## Causa

El engine re-construye el estado inicial en cada invocacion:
`langgraph_engine.py::_initial_state` retorna
`{"messages": [{"role": "user", "content": message}], ...}` y el estado
conversacional usa el reducer `add_messages`
(`agents_backend/conversational/state.py:21`). Con un checkpointer activo,
`add_messages` anade (no reemplaza): si el turno abortado ya persistio el
HUMAN original, el Retry reinserta una copia idéntica (mismo contenido, id
distinto) en lugar de reanudar desde el checkpoint. El duplicado es
acumulativo por cada reintento y contamina el contexto de los turnos
siguientes (el modelo ve la misma pregunta 2+ veces).

## Fix y verificacion

Pendiente. Opciones evaluadas (RFC pendiente de decision):

- (a) En el endpoint de stream, detectar si el ultimo mensaje persistido del
  hilo ya es el mismo HUMAN (mismo contenido) y omitir la reinserccion
  (dedupe por contenido en la cola del hilo).
- (b) Pasar el mensaje con un `id` determinista derivado del hash
  (thread_id + contenido + indice de turno) para que `add_messages` lo
  trate como upsert en vez de insercion.
- (c) En el frontend, marcar el reintento y que el backend reanude el turno
  previo en vez de crear uno nuevo (mayor acoplamiento).

La (a) es la de menor riesgo y no cambia el contrato SSE. Verificacion
propuesta: repetir el abort+Retry y comprobar que el history mantiene 1 sola
copia del HUMAN; sonda curl de doble POST con mismo thread.

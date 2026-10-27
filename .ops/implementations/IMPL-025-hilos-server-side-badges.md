---
id: IMPL-025
tipo: Implementation
type: Implementation
title: Hilos de chat server-side con ownership y badges (fix BUG-022/023)
description: Tabla chat_threads + API de listado/rename/delete + ownership 403 + sidebar server-side con badges.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BL-017]
status: done
---

## Alcance

Incluye: modelo ChatThread + migracion b8c9d0e1f2a3; threads_service.py
(register_or_adopt, require_owned_thread, record_turn, list, rename,
delete); endpoints GET/PATCH/DELETE /api/chat/threads; ownership en
history/stream/invoke; frontend server-backed (useThreadId reescrito,
ThreadSidebar con badges, ChatPanel sin titulo por turno, ChatView
hidratacion, auth invalidate()); i18n es/en; pruebas QT-008.

No incluye: purga del checkpointer al borrar hilo (seguimiento separado);
badge de preguntas verificadas (GeneratedQuestion no enlaza thread_id).

## Diseno

DEC-004 resolucion (a) extendida por el propietario: tabla con owner +
listado server-side; badges = ultima materia usada + contador de mensajes;
titulo fijado al primer mensaje (pinned). El almacenamiento entre materias
sigue global (la materia es contexto por turno); lo que se acota es por
usuario y por dispositivo. Hilos heredados del checkpointer (rondas 1-7)
se registran con lazy adoption en el primer turno del dueno; un id ajeno
nunca se reasigna (403). message_count es aproximado (+2 por turno, tope
1M); MAX hilos por usuario 1000; titulo 1-200.

Pasos atomicos: (1) modelo+migracion; (2) servicio+schemas; (3) endpoints
chat.py; (4) frontend composable+sidebar+panel+view+auth+i18n; (5) pruebas
scripts/verify-threads-r8.ps1 (12 comprobaciones API) + Playwright;
(6) rollback: alembic downgrade -1 y revert de los 3 submodulos.

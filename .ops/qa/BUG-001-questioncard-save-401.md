---
id: BUG-001
tipo: Defect
type: Defect
title: Botones Save/Save & verify del QuestionCard fallan con 401
description: El HITL por botones estaba roto; el token no viajaba en el body ni llegaban las props.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Consola: `401 (Unauthorized)` al pulsar Save o Save & verify en el widget "Question
generated" (ronda 1, 2026-10-19). El widget muestra "Not authenticated" y queda en estado
error; la pregunta no se guarda. Solo funcionaba la confirmacion textual por chat.

## Causa

`POST /api/chat` resuelve el usuario desde `token` en el body (`_resolve_user`, chat.py)
porque el SSE no siempre puede mandar headers; `QuestionCard.save()` enviaba
`{message, thread_id, subject_id}` sin `token`. Ademas `MessageList.vue` renderizaba
`<QuestionCard>` sin las props `subjectId`/`threadId` declaradas.

## Fix y verificacion

Fix 11.1 (RFC-03): `save()` incluye `token: getAuthToken()` en el body; `MessageList`
pasa `:subject-id`/`:thread-id`; `_resolve_user` acepta `Authorization: Bearer` como
fallback. Verificado en ronda 3 (C7): badge "Verified" y fila en BD con
`verified_by_human=True` (id `ae5e97db`) sin recargar.
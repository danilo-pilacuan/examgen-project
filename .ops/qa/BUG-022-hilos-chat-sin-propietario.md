---
id: BUG-022
tipo: Defect
type: Defect
title: Hilos de chat sin control de propiedad (lectura y escritura entre usuarios)
description: Cualquier usuario autenticado lee y escribe el hilo de otro via /api/chat/history y /api/chat.
estado: corregido
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-007, QT-008, IMPL-024, IMPL-025, BL-017, DEC-004]
status: fixed
---

## Evidencia

Ronda 7 (2026-10-27), dos usuarios reales (qa-r7 y qa-r7-b) via API y navegador:

1. GET `/api/chat/history/ad0e765d-...` (hilo de qa-r7) con token de qa-r7-b ->
   200 con los mensajes de A; re-confirmado al cierre (4 mensajes, "Hola,
   registro una nota de control...").
2. POST `/api/chat` de qa-r7-b con el thread_id de A -> inserto
   "probe-continuity-B" + respuesta del modelo en el historial de A (roles
   user,assistant,user,assistant verificados via history).
3. Confirmacion visual Playwright: con sesion de un tercer usuario
   (qa-r7-ui-temp) en el mismo navegador, la sidebar listo los hilos de qa-r7
   y al hacer click cargo su contenido completo.

Hallazgo relacionado: materias semilla sin owner (owner_id NULL) son
escribibles por cualquiera (qa-r7-b altero una pregunta de Eva via
PUT /questions/{id}/verification, sin 403).

## Causa

`chat.py` autentica pero nunca verifica la propiedad del thread_id: history
(~linea 99), stream (~linea 79) e invoke (~linea 126) aceptan cualquier id;
el checkpointer LangGraph no registra owner y no existe tabla de hilos
(BL-017). El check de materia (`_check_subject_access`) no cubre el hilo.

## Fix y verificacion

Implementado (IMPL-025, DEC-004 a): tabla `chat_threads` con owner (migracion
b8c9d0e1f2a3), `require_owned_thread` en history (404 desconocido, 403 ajeno)
y `register_or_adopt` en stream/invoke (403 si el id ya esta registrado a
otro usuario; nunca reasigna). Verificado via API con qa-r8-a/qa-r8-b
(scripts/verify-threads-r8.ps1): lectura, escritura, rename y delete del
hilo ajeno -> 403; listado de B no contiene hilos de A; hilos de control
purgados del registro. Pendiente: verificado final del propietario
(estado pasa a `verificado` solo con su revision).

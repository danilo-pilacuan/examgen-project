---
id: BUG-022
tipo: Defect
type: Defect
title: Hilos de chat sin control de propiedad (lectura y escritura entre usuarios)
description: Cualquier usuario autenticado lee y escribe el hilo de otro via /api/chat/history y /api/chat.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-007, IMPL-024, BL-017, DEC-004]
status: draft
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

Pendiente de DEC-004: tabla `threads` con owner (BL-017) + validacion 403 en
los 3 endpoints de chat. Verificacion: B recibe 403 al leer/escribir el hilo
de A; el listado de hilos (BL-017) devuelve solo hilos propios; caso adversario
con thread_id ajeno.

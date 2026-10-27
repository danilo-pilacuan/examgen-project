---
id: QT-008
tipo: TestCase
type: TestCase
title: Hilos de chat server-side con ownership y badges (ronda 8)
description: Verifica tabla chat_threads, listado por usuario, 403 entre usuarios y badges del listado (IMPL-025, DEC-004 a).
estado: pendiente
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [REQ-001]
status: draft
fase: 4
---

## Objetivo

Verifica el fix de BUG-022/BUG-023 via BL-017 (resolucion DEC-004 a,
extendida por el propietario): hilos con owner, listado server-side con
badges (ultima materia + contador de mensajes), titulo fijado al primer
mensaje. Deriva de la seccion 9 de AGENTS.md (seguridad multitenant).
Precondicion: migracion b8c9d0e1f2a3 aplicada; dos usuarios de control.

## Caso que debe pasar

Ejecutado con scripts/verify-threads-r8.ps1 (qa-r8-a/qa-r8-b, API directa):
1. login A y B ok; listas iniciales vacias (A=0, B=0).
2. Primer turno de A -> fila en chat_threads con titulo fijado
   "Hola: conversacion de control QA ronda 8", message_count=2.
3. Listado de A contiene el hilo con badges (last_subject_name vacio sin
   materia, contador 2). PASS.
4. Playwright (qa-r7): conversacion visible tras reload, click hidrata el
   contenido; badge de materia "QA R7 Recert" + contador "4" tras segundo
   turno con materia activa. PASS.
5. A renombra su hilo (PATCH) -> 200 y titulo nuevo. PASS.
6. A borra su hilo (DELETE) -> fila fuera del listado y de la BD. PASS.

## Caso que debe ser rechazado

Regla 3 de la seccion 0: casos adversariales ejecutados en el mismo script.
7. B intenta leer history del hilo de A -> 403 (antes 200, BUG-022).
8. B intenta escribir en el hilo de A via /api/chat -> 403.
9. B intenta renombrar (PATCH) el hilo de A -> 403.
10. B intenta borrar (DELETE) el hilo de A -> 403.
11. Listado de B no contiene el hilo de A (aislamiento del listado). PASS.
12. GET /api/chat/threads sin token -> 401. PASS.

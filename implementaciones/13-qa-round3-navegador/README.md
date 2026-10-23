# 13 — QA ronda 3 en el navegador (correcciones de las rondas 1-2 + fixes 11.1-11.6)

> **Fecha:** 2026-10-23 · **Alcance:** E2E manual del MVP tras las rondas 1-2, desde `http://localhost:3000` (frontend dockerizado), actuando como profesor real. Cubre lo que quedaba pendiente de la etapa 11 (checklist C6, C7, C9-C13 + regresión R1-R7) y verifica la estructura de la ronda 1 ([10-qa-flujo-completo-navegador](../10-qa-flujo-completo-navegador/README.md)).
> **Regla de la sesión:** toda interacción exclusivamente por el navegador integrado + Playwright (sin llamadas directas a la API para validar UI).

## Contenido

| Archivo | Descripción |
|---|---|
| [bugs.md](./bugs.md) | Bugs nuevos detectados en esta ronda (severidad, evidencia, causa raíz, fix) |
| [issues.md](./issues.md) | Observaciones menores y mejoras de UX no bloqueantes |
| [rfcs.md](./rfcs.md) | Propuestas de solución para los bugs de esta ronda |
| [backlog.md](./backlog.md) | Backlog priorizado (P0/P1/P2) resultante |

## Resumen ejecutivo

**Los fixes de las rondas 1-2 funcionan de punta a punta.** El caso de uso central (generar examen por chat y por formulario, descargar ZIP, HITL de preguntas) está certificado. Se detectaron **2 bugs nuevos** (uno crítico de nginx que rompía el hard-reload de `/subjects` y vaciaba el selector de materias) y se corrigieron durante la misma sesión.

- ✅ **C7 (BUG-01):** los botones Save / Save & verify del QuestionCard ya funcionan (token en body + props + fallback de header `Authorization`); badge "✔ Verified" y la pregunta llega al banco sin recargar.
- ✅ **C8 (BUG-06/07):** matar `exam_app` a mitad de turno → burbuja "⚠️ Connection lost" + botón "↻ Retry"; el Retry reenvía el turno y el contenido queda persistido en el checkpointer.
- ✅ **C9 (BUG-10):** re-consultar el guardado tras un stream muerto devuelve el estado real del banco ("already saved, id X, verified") en vez de "no pending question"; sin duplicados.
- ✅ **C11 (BUG-11 + ISS-06):** `HEAD /output/<file>` → 200 y `Content-Disposition: attachment` presente.
- ✅ **C12 (BUG-12 + ISS-07):** subida > 100 MB → mensaje accionable "El archivo supera el tamaño máximo (100 MB)…"; el formulario de Exams muestra banner de error con el detalle.
- ✅ **C13 (ISS-10):** tablas markdown con `display: block; overflow-x: auto` (scrollean dentro de la burbuja).
- ✅ **C5:** formulario Exams genera el examen (POST `/exams/generate` proxificado), refresca la lista y cierra el formulario.
- ✅ **C6 (BUG-04):** pedir un examen de un tema sin preguntas → el agente lo detecta y ofrece alternativas; con 2 preguntas disponibles genera el examen con 2 ítems (sin PDFs vacíos).
- ✅ **R2 (guardrail):** pedir borrar una pregunta verificada → el agente se niega e indica el procedimiento; la pregunta sigue en el banco.
- ✅ **R4 (banco):** filtros por topic/difficulty, toggle Remove→Pending→Verify operativo.
- ✅ **R5 (exportaciones):** CSV del banco descargable vía chat (200, 28 KB).
- ✅ **R6 (auditoría):** 54 filas nuevas en `llm_responses` durante la sesión.
- ✅ **R7 (idioma):** prompt en español → respuesta del agente en inglés.
- ❌→✅ **BUG-13/BUG-14 (ronda 2):** re-verificados: historial de chat persiste tras logout/login y la vista Exams muestra un registro por examen con solo el botón ZIP.

## Flujo ejecutado (evidencia)

### 1. Fixes 11.1-11.6 aplicados antes del QA
- 11.1: `QuestionCard.save()` envía `token: getAuthToken()`; `MessageList` pasa `:subject-id`/`:thread-id`; `_resolve_user` acepta `Authorization: Bearer` como fallback.
- 11.3: `save_pending_question` registra el id guardado en `PendingItemStore` ANTES de limpiar el pending y emite `question_saved` antes de limpiar; re-consulta devuelve el estado real.
- 11.4: `@app.api_route("/output/{filename}", methods=["GET","HEAD"])`.
- 11.5: `friendlyHttpMessage()` en `http.ts` (413/401/403 accionables); banner `.form-error` en ExamsView.
- 11.6: `overflow-x: auto` en `:deep(table)` del MarkdownRenderer.
- Validación estática: `py_compile` OK (exam-app + agents-backend), `type-check`/`lint:check`/`build-only` OK; rebuild Docker healthy.

### 2. C7 — HITL por botones (antes BUG-01)
- Chat → "Generate a question about database indexing with medium difficulty" → QuestionCard renderizado.
- Click en "✔ Save & verify" → badge "✔ Verified" (sin 401 en consola).
- BD: fila nueva en `generated_questions` con `verified_by_human=True` (id `ae5e97db`); el Banco la muestra como "✔ Human" sin recargar.

### 3. C8 — Stream muerto + Retry (BUG-06/07)
- Turno en curso → `docker stop exam_app` → `net::ERR_INCOMPLETE_CHUNKED_ENCODING`.
- La burbuja muestra "⚠️ Connection lost — the action may have completed. Check the Bank/Exams view." + botón "↻ Retry".
- `docker start exam_app` → click en Retry → el turno se reenvía y completa; al recargar, el historial hidratado muestra la pregunta generada (checkpointer, 75 filas en `checkpoints`).

### 4. C9 — Idempotencia del guardado (BUG-10)
- Tras guardar y verificar (pending limpio): "Please save the pending question again" → "✅ Your question was already saved (id: ae5e97db…) and is currently verified by human. No action needed."
- En una conversación nueva (sin pending ni id guardado): "save the pending question" → mensaje honesto "There is currently no pending question to save…".
- BD: sin duplicados (10 preguntas antes y después).

### 5. C5/C6 — Generación de exámenes
- Chat: "Generate an exam… 3 questions about recipes and cooking" → el agente detecta que el banco no tiene ese tema y ofrece alternativas (guardrail de blueprint).
- Chat: confirmación "Name: QA_Empty_Test, 1 version, use existing bank questions" → examen generado con las 2 preguntas disponibles (avisa del ajuste 3→2), ZIP publicado y persistido (`exams`: 2 ítems, `QA_Empty_Test.zip`).
- Formulario: "+ Generate exam" (QA_Form_Round3) → POST proxificado, examen creado (8 ítems), lista refrescada, formulario cerrado.

### 6. C11/C12/C13 — Calidad
- `HEAD /output/QA_Rebuild_-_Examen_1.zip` → 200 (directo y vía nginx); `GET` incluye `content-disposition: attachment; filename="…"`.
- Subida de un PDF de 101 MB → 413 capturado y mostrado como "⚠️ El archivo supera el tamaño máximo (100 MB). Divide el material en capítulos o archivos más pequeños."
- Tabla markdown del chat: `display: block; overflow-x: auto` verificado por computed style.

### 7. Regresión R1-R7
- R2: "Delete the question about database indexing" → el agente localiza la pregunta verificada y se niega; sigue en BD.
- R4: filtro "Database Indexing" → 1 fila; toggle Remove→Pending→Verify→Remove OK.
- R5: "Export the question bank as CSV" → `questions_20261023_083157.csv` descargable (200, 28 KB).
- R6: 54 filas nuevas en `llm_responses` en la ventana de la sesión.
- R7: "¿Cuántas preguntas hay en el banco?" → respuesta en inglés con tabla.
- C1: registro de materia "Redes de Computadoras" → aparece en la lista y en el selector; Activate sincroniza navbar y chips (0 questions / 0 chunks).
- C10: cambiar de materia refresca los contadores (21 questions / 14 chunks al volver a Base de Datos).

### 8. BUG-13/BUG-14 (ronda 2) re-verificados
- Logout → login → los threads persisten y el contenido se hidrata (endpoint `/api/chat/history/{id}` 200).
- Vista Exams: un registro por examen, solo botón ZIP (fallback PDF en legacy sin ZIP).

## Métricas de la sesión

| Métrica | Valor |
|---|---|
| Checks de certificación ejecutados | C1, C5-C13, R1-R7 (los pendientes de la etapa 11) |
| Bugs nuevos | 2 (1 crítico nginx, 1 medio) |
| Fixes aplicados en la sesión | 2 (BUG-15 nginx + Accept header) |
| Preguntas en el banco (fin de sesión) | 21 (10 al inicio + generadas del QA) |
| Exámenes en BD (fin de sesión) | 12 (8 al inicio + QA_Empty_Test, QA_Form_Round3, Probe_Head ×2) |
| Filas nuevas en `llm_responses` | 54 |
| Rebuilds Docker | 4 (exam-app, frontend ×3) |

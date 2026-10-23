# RFCs — Propuestas de solución (ronda de corrección)

> Cada RFC indica el bug que resuelve, los archivos a tocar y el criterio de aceptación (QA re-test).

---

## RFC-01 — Proxy nginx completo y tolerante a operaciones largas
**Resuelve:** BUG-02, BUG-03, BUG-05, BUG-07 · **Esfuerzo:** S · **Riesgo:** bajo

### Cambios en `projects/frontend/nginx.conf`
```nginx
# 1) Tamaño de subida (BUG-05)
server {
    ...
    client_max_body_size 100m;

    # 2) /api/: SSE largo sin buffering (BUG-03/07)
    location /api/ {
        proxy_pass http://exam-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_read_timeout 3600s;   # default 60s mata el examen
        proxy_send_timeout 3600s;
        proxy_buffering off;        # imprescindible para text/event-stream
        proxy_cache off;
    }

    # 3) Generación de exámenes (BUG-02) — ANTES del SPA fallback
    location = /exams/generate {
        proxy_pass http://exam-app:8000;
        proxy_set_header Host $host;
    }
}
```
> Nota: `location = /exams/generate` (exacta) evita colisionar con la ruta SPA `/exams`.

### Criterio de aceptación (re-test)
1. Subir un PDF de 3-10 MB desde Material → indexa sin 413.
2. Generar examen de 10 preguntas por chat → el turno completa, llega `artifact_ready` y el ZIP se descarga.
3. `POST /exams/generate` desde el formulario de Exams → crea el examen y refresca la lista.

---

## RFC-02 — Heartbeat SSE + manejo de errores en el cliente
**Resuelve:** BUG-03, BUG-06, BUG-07, BUG-10 (parte) · **Esfuerzo:** M · **Riesgo:** bajo

### Backend (`exam_app/api/v1/chat.py` o `ChatService.stream`)
- Enviar `event: ping` (o comentario `: ping\n\n`) cada 15 s mientras no haya tokens (usa `asyncio.wait` con timeout sobre la cola de eventos).
- Al terminar el turno, emitir `event: done` siempre; ante excepción, `event: error` con `{"message": …}` y cerrar limpio.

### Frontend
- `api/sse.ts`: ignorar eventos `ping`; ante `error`, mostrar en la burbuja "⚠️ Connection lost — the action may have completed. Check the Bank/Exams view." y ofrecer botón **Retry** (reenvía el último mensaje).
- `useChatStream.ts`: propagar el tipo de error al store en vez de solo `finishMessage`.

### Criterio de aceptación
1. Un turno que tarde 3 min no se corta (con RFC-01) y muestra pings en el network tab.
2. Matar exam-app a mitad de turno → la UI muestra el aviso y permite reintentar.

---

## RFC-03 — HITL por botones del QuestionCard funcional
**Resuelve:** BUG-01 · **Esfuerzo:** S · **Riesgo:** bajo

### Cambios
1. `MessageList.vue`: pasar `:subject-id="chat.activeSubjectId"` y `:thread-id="chat.threadId"` a `QuestionCard` (requiere exponer el store o recibirlos por props desde `ChatPanel`).
2. `QuestionCard.vue::save()`:
```ts
const res = await apiFetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: verify ? t('questionCard.saveVerifiedPrompt', { statement }) : t('questionCard.savePrompt', { statement }),
    thread_id: props.threadId ?? undefined,
    subject_id: props.subjectId ?? undefined,
    token: getAuthToken(),          // ← el endpoint lo exige en el body
  }),
})
```
3. (Opcional, defensa en profundidad) `chat.py::_resolve_user`: aceptar también el header `Authorization: Bearer …` como fallback del body.

### Criterio de aceptación
1. Generar pregunta → `Save` guarda (badge "Saved") y `Save & verify` guarda + verifica (badge "Verified").
2. El banco refleja el estado sin recargar (evento `question_saved`).

---

## RFC-04 — Pipeline: fallar rápido cuando no hay ítems aprobados
**Resuelve:** BUG-04 · **Esfuerzo:** S · **Riesgo:** bajo

### Cambios
1. `nodes.py::compiler_node` (inicio):
```python
if not state.get("approved_items"):
    return {
        "status": "failed",
        "error_message": "No items were approved; nothing to compile.",
        "compilation_log": [{"attempt_number": 1, "version": 0, "success": False,
                             "error_excerpt": "empty_approved_items"}],
    }
```
2. `graph.py::should_retry_compilation`: con `status == "failed"` por ítems vacíos → `end` (no reintentar compilación).
3. `tools.py::generate_exam_pdf`: si `result["status"] != "completed"` o `len(approved_items) == 0` → devolver al chat un mensaje de error con el `rejection_log` resumido (nada de ZIP).
4. Incluir `rejection_log` y `total_llm_calls` en el JSON de artefacto para diagnóstico (hoy se pierden).
5. (Opcional) Loguear en exam-app los `generation_error` del generador para detectar problemas de structured output.

### Criterio de aceptación
1. Forzar un fallo del LLM (URL inválida) → el pipeline termina `failed`, no compila PDFs, no publica ZIP, y el chat recibe el error.
2. Un examen normal sigue funcionando igual.

---

## RFC-05 — Historial de exámenes por materia correcto
**Resuelve:** BUG-08 · **Esfuerzo:** M · **Riesgo:** medio (migración de legacy)

### Cambios
1. Script de migración one-shot: para cada PDF legacy del output dir, inferir la materia (del JSON hermano si existe; si no, marcar `subject_id=NULL`) e insertar fila en `exams`.
2. `list_subject_exams`: eliminar el fallback por prefijo; listar solo filas de la tabla filtradas por `subject_id` (ya hace el scoping de owner).
3. Los PDFs sin materia asignada quedan visibles solo en una sección "Unassigned legacy" (o se ocultan).

### Criterio de aceptación
1. Con Base de Datos activa, la vista Exams solo muestra exámenes de esa materia.
2. Los artefactos legacy de Economía Aplicada aparecen solo en su materia.

---

## RFC-06 — Contadores de contexto reactivos
**Resuelve:** BUG-09 · **Esfuerzo:** XS

- En el componente de la barra de contexto: `watch(() => subjects.activeSubjectId, refreshCounters)` (banco + chunks), igual que hacen las vistas.

---

## RFC-07 — Idioma del contenido como parámetro (ISS-05)
**Esfuerzo:** M · **Post-V1**

- Añadir `content_language: "en" | "es"` al blueprint y al prompt de `generate_question`; el template LaTeX ya es bilingüe vía babel. Default: `en` (contrato), configurable por materia.

# Bugs detectados — QA flujo completo (2026-10-19)

> Severidades: 🔴 CRITICAL (bloquea el flujo principal) · 🟠 HIGH (funcionalidad rota con workaround) · 🟡 MEDIUM (degrada la experiencia) · ⚪ LOW (cosmético/edge).

---

## 🔴 BUG-01 — Botones Save / Save & verify del QuestionCard fallan con 401

- **Componente:** `projects/frontend/src/components/widgets/QuestionCard.vue` + `projects/exam-app/src/exam_app/api/v1/chat.py`
- **Pasos:** generar una pregunta por chat → en el widget "Question generated" pulsar `Save` o `✔ Save & verify`.
- **Observado:** consola `401 (Unauthorized)`; el widget muestra "Not authenticated" y queda en estado `error` con los botones re-habilitados. La pregunta no se guarda.
- **Esperado:** guardar (y opcionalmente verificar) la pregunta pendiente.
- **Causa raíz:** `POST /api/chat` resuelve el usuario desde `token` **en el body** (`_resolve_user`, chat.py:29-31) porque el SSE del navegador no siempre puede mandar headers. `QuestionCard.save()` llama a `apiFetch('/api/chat', …)` solo con `{message, thread_id, subject_id}` — sin `token`. Además `apiFetch` sí inyecta `Authorization` en headers, pero este endpoint no lo lee. Adicionalmente `MessageList.vue` renderiza `<QuestionCard :question=…>` sin pasar las props `subjectId`/`threadId` que el componente declara.
- **Impacto:** el HITL por botón (la UX principal del widget) está roto; solo funciona la confirmación textual por chat.
- **Fix sugerido:** en `QuestionCard.save()` incluir `token: getAuthToken()` en el body (y `thread_id`/`subject_id` reales vía props desde `MessageList`/`ChatPanel`); alternativamente hacer que `/api/chat` acepte el header `Authorization` como fallback.

---

## 🔴 BUG-02 — `POST /exams/generate` no está proxificado por nginx (405 siempre)

- **Componente:** `projects/frontend/nginx.conf` + `projects/exam-app/src/exam_app/main.py:174`
- **Pasos:** vista Exams → "+ Generate exam" → completar (10 preguntas) → "Generate exam".
- **Observado:** consola `405 (Method Not Allowed)`; el botón vuelve a su estado normal y el formulario queda abierto **sin ningún mensaje de error**. Nunca se genera nada. El access log de exam-app confirma que la petición **nunca llega** al backend.
- **Esperado:** generar el examen y refrescar la lista.
- **Causa raíz:** nginx solo proxifica `/api/`, `/subjects`, `/questions`, `/auth/`, `/output/`, `/ws`, `/v1/`. `POST /exams/generate` cae en `location /` (SPA fallback → `index.html`), que solo acepta GET → 405. El comentario del propio nginx.conf lo documenta como decisión ("`/exams` is NOT proxied"), pero el frontend llama a esa ruta.
- **Impacto:** la vía REST de generación de exámenes es 100% inoperante.
- **Fix sugerido:** añadir `location /exams/generate { proxy_pass http://exam-app:8000; }` **antes** del SPA fallback (o mover el endpoint a `/api/exams/generate` y actualizar `ExamsView.vue`).

---

## 🔴 BUG-03 — SSE del chat muere a los 60 s (timeout nginx) y cancela la generación de exámenes

- **Componente:** `projects/frontend/nginx.conf` (`location /api/`) + `exam_app/api/v1/chat.py` (SSE sin heartbeat)
- **Pasos:** chat → "Generate an exam for the first midterm with 10 questions" → confirmar nombre y versiones.
- **Observado:** exactamente 60 s después de iniciar el turno (09:09:16 → 09:10:16), el navegador registra `net::ERR_INCOMPLETE_CHUNKED_ENCODING`; la burbuja del asistente queda **vacía**; no hay card de artefacto, no hay mensaje de error, y el pipeline del lado servidor **no produce ningún artefacto** (0 llamadas a `POST /compile`, sin fila en `exams`, sin JSON). El mismo patrón mató 3 turnos de guardado de preguntas durante el lote (ver BUG-06/07).
- **Esperado:** el turno completa, emite `artifact_ready` y el ZIP aparece en el chat y en la vista Exams.
- **Causa raíz:** `proxy_read_timeout` de nginx por defecto = 60 s. La generación de examen tarda más (LLM × N preguntas + compilación) y durante ese tiempo el SSE no envía ningún byte → nginx corta. El frontend no reintenta ni informa.
- **Impacto:** **ningún examen puede generarse por chat**; además pierde silenciosamente turnos largos.
- **Fix sugerido:** en `location /api/`: `proxy_read_timeout 3600s; proxy_send_timeout 3600s; proxy_buffering off;` + heartbeat SSE cada ~15 s desde el backend (`: ping\n\n`) para mantener viva la conexión y detectar cortes.

---

## 🔴 BUG-04 — El pipeline compila y publica exámenes VACÍOS como "completed"

- **Componente:** `projects/agents-backend/src/agents_backend/exam_pipeline/` (nodes.py, graph.py) + `conversational/tools.py::generate_exam_pdf`
- **Evidencia:** `data/agent_outputs/Parcial_1.json` (generado 03:13): `subject_name: "Economía Aplicada"`, `total_questions: 2`, **`items: []`**, sin `rejection_log` ni `total_llm_calls`. Los 4 PDFs (`Parcial_1_A/B[_respondido].pdf`, 25.395 B idénticos en tamaño) contienen 1 página con portada, "Question:", "Total Points: 0", "Score:" y **ninguna pregunta**. El estado fue `completed` y el ZIP se publicó en el chat.
- **Esperado:** si no se aprueba ningún ítem, el pipeline debe fallar (o al menos no compilar/publicar) con un error claro.
- **Causa raíz (hipótesis a confirmar):** todas las ranuras terminan en `rejection_log` (p. ej. `generation_error`/`evaluation_error` silenciosos — los `except` de `generator_node`/`evaluator_node` tragan la excepción y la convierten en rechazo) y `assembler_node`/`compiler_node` no validan `len(approved_items) > 0`. `generate_exam_pdf` solo valida que el banco tenga preguntas, no que el pipeline haya aprobado alguna.
- **Impacto:** el profesor recibe un "examen" sin preguntas como si fuera exitoso; envenena el historial de Exams.
- **Fix sugerido:** en `compiler_node` (o `should_retry_compilation`): si `approved_items` está vacío → `status="failed"`, `error_message="No items were approved"` y no compilar. En `generate_exam_pdf`: si `approved_items` vacío → devolver error al chat en vez del ZIP. Registrar el `rejection_log` en el JSON para diagnóstico.

---

## 🟠 BUG-05 — Subida de material > 1 MB falla con 413

- **Componente:** `projects/frontend/nginx.conf` (falta `client_max_body_size`)
- **Pasos:** vista Material → Upload file → PDF de 3.1 MB (*Foundations of Databases*, libro completo).
- **Observado:** `413 (Request Entity Too Large)`; la UI muestra el texto crudo "⚠️ Request Entity Too Large" sin guía.
- **Esperado:** subir PDFs de tamaño razonable (un libro de texto típico: 2-50 MB).
- **Causa raíz:** nginx default `client_max_body_size 1m`.
- **Impacto:** el profesor no puede indexar material real; tuvo que trocear el libro en capítulos.
- **Fix sugerido:** `client_max_body_size 100m;` en el `server` (o en `/api/`). Revisar también el límite del backend (`/api/files`) y dar un mensaje accionable ("file too large, max X MB").

---

## 🟠 BUG-06 — Turno de chat termina con burbuja de asistente VACÍA (sin tokens ni error)

- **Componente:** `exam_app/services/chat_engine.py` (SSE) + `frontend/src/composables/useChatStream.ts`
- **Evidencia:** lote 4, q41 ("database constraints CHECK and UNIQUE"): el turno de guardado terminó (botón Stop desapareció) y el último mensaje del asistente quedó con **0 caracteres**; la pregunta no se guardó y el ítem pendiente se perdió (el siguiente turno respondió "there is no pending question left to save").
- **Causa raíz (hipótesis):** el stream se corta sin propagar error al store (el `catch` de `useChatStream` solo hace `finishMessage`); sin heartbeat no se distingue "procesando" de "muerto". Relacionado con BUG-03.
- **Impacto:** pérdida silenciosa de trabajo del profesor; el estado del banco queda inconsistente con lo que la UI mostró.
- **Fix sugerido:** heartbeat + evento `error` tipado al cortarse el stream; en el frontend, marcar la burbuja con "⚠️ connection lost, retry" y ofrecer reintentar el turno.

---

## 🟠 BUG-07 — Cortes de stream intermitentes durante uso intensivo (ERR_INCOMPLETE_CHUNKED_ENCODING)

- **Componente:** nginx `/api/` + exam-app SSE
- **Evidencia:** 3 incidentes en ~90 turnos (08:29, 09:10 y el turno vacío del lote 5). En el del examen (09:10) el corte fue exactamente a los 60 s; en los otros ocurrió durante ráfagas de turnos.
- **Causa raíz:** misma familia que BUG-03 (timeouts de proxy + ausencia de keepalive/heartbeat); posible contribución de `proxy_buffering` activo sobre `text/event-stream`.
- **Impacto:** fiabilidad general del chat degradada bajo uso sostenido.
- **Fix sugerido:** mismo paquete que BUG-03 (timeouts largos + `proxy_buffering off` + heartbeat) y reintentos con backoff en el cliente SSE.

---

## 🟡 BUG-08 — Exámenes legacy de otra materia aparecen en el historial de Base de Datos

- **Componente:** `exam_app/api/v1/exams.py::list_subject_exams` (enriquecimiento legacy por prefijo de nombre)
- **Evidencia:** con la materia **Base de Datos** activa, la vista Exams lista `Parcial_1_A/B[_respondido]` (generados para **Economía Aplicada**, según `Parcial_1.json`) y además 30+ PDFs con nombre UUID (`652f0255-…`, `6180a363-…`) de ejecuciones antiguas del pipeline batch.
- **Causa raíz:** el fallback "legacy" lista **todos** los PDFs del directorio de salida que no estén persistidos en BD, sin filtrar por materia (el nombre de archivo no contiene subject_id).
- **Impacto:** historial contaminado y confuso entre materias (multi-tenant roto a nivel de vista).
- **Fix sugerido:** solo listar legacy cuando la materia no tenga exámenes persistidos, o mejor: migrar los legacy a la tabla `exams` con su `subject_id` real una vez y eliminar el fallback por prefijo.

---

## 🟡 BUG-09 — Contador de preguntas de la barra de contexto no se refresca al cambiar de materia

- **Componente:** barra de contexto del layout (header) / stores
- **Evidencia:** al activar "Base de Datos" (0 preguntas en ese momento) el header siguió mostrando "31 questions" (valor de Economía Aplicada); recién se actualizó al recargar la vista.
- **Causa raíz:** el contador no reacciona al `activeSubjectId` (no re-consulta el banco al cambiar la materia).
- **Fix sugerido:** `watch(activeSubjectId)` → refrescar contadores (como ya hacen Bank/Material/Exams).

---

## 🟡 BUG-10 — El guardado HITL por texto consume el ítem pendiente aunque el stream muera

- **Componente:** `conversational/tools.py::save_pending_question` + `PendingItemStore`
- **Evidencia:** tras el turno vacío de q41 (BUG-06), el intento de re-guardar respondió "no pending question left to save": el turno muerto **sí ejecutó** la tool (o la vació) sin entregar respuesta al profesor. En el lote 5 (q56) el mismo patrón dejó la pregunta guardada pero **sin verificar** pese a que el profesor pidió verificación.
- **Impacto:** estado del banco impredecible desde el punto de vista del profesor (a veces guardó, a veces no, a veces sin verificar).
- **Fix sugerido:** idempotencia + confirmación explícita: la tool debe emitir el evento `question_saved` **antes** de limpiar el pending, y el flujo debe tolerar re-consultas ("¿qué pasó con mi guardado?") consultando el banco por statement en vez de solo la memoria del thread.

---

## ⚪ BUG-11 — `HEAD /output/{file}` devuelve 405

- **Componente:** `exam_app/main.py::@app.get("/output/{filename}")`
- **Evidencia:** `HEAD /output/Parcial_1.zip` → 405 (solo GET registrado).
- **Impacto:** menor; rompe pre-chequeos de descarga (algunos gestores/antivirus hacen HEAD).
- **Fix sugerido:** `@app.api_route("/output/{filename}", methods=["GET","HEAD"])`.

---

## ⚪ BUG-12 — Errores de subida muestran el texto crudo del status HTTP

- **Componente:** `MaterialView.vue` (`uploadMessage`)
- **Evidencia:** "⚠️ Request Entity Too Large" (texto del status line, sin código ni guía).
- **Fix sugerido:** mapear 413 → "El archivo supera el tamaño máximo (X MB). Divide el material o sube capítulos." y 401/403 → mensajes de sesión/permisos.

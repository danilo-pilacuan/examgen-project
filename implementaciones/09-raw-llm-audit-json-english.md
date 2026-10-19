# Etapa 09 — Auditoría LLM (raw answer/thinking) + tool eliminar archivos + descarga JSON + inglés forzado

> **Objetivo:** Cerrar los 4 ítems pendientes de la **segunda revisión del proyecto** (`Requisitos/segunda revision_proyecto.md`): guardar el Raw Answer y Raw Thinking de cada llamada al LLM, tool para eliminar archivos del material, descarga del JSON intermedio antes del LaTeX y regla de idioma inglés en el prompt del sistema.
>
> **Estado:** ✅ Completada (smoke tests + E2E validados en Docker y navegador)
> **Depende de:** Etapas 0-8 (`Tag_V1.0.0`)
> **Fecha de última actualización:** 2026-10-19

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE

## 📋 Tareas

### 9.1 — Tabla `llm_responses` + captura (core + agents-backend)
- [x] Migración Alembic `f6a7b8c9d0e1_create_llm_responses` (cadena: `e5f6a7b8c9d0` → `f6a7b8c9d0e1`): tabla `llm_responses` — `id` UUID PK, `thread_id`, `context` (ej. `chat:model`, `pipeline:generator`), `model`, `prompt` TEXT, `raw_answer` TEXT, `raw_thinking` TEXT nullable, `latency_ms`, `created_at` + índices por `thread_id` y `created_at`
- [x] Modelo `LLMResponse` en `core/domain/models.py`
- [x] Settings en `core/config.py`: `llm_capture_raw: bool = True` (master switch) y `llm_capture_thinking: bool = False` (cadena de pensamiento)
- [x] Servicio `core/domain/llm_log/service.py`: `record_llm_response()` (sesión propia, **best-effort**: nunca lanza ni rompe el chat/pipeline), `serialize_messages()` (mensajes LangChain o dicts), `extract_thinking()` (busca `reasoning_content`/`reasoning`/`thinking` en `additional_kwargs`)
- [x] Hook en `agents_backend/conversational/graph.py` `_assistant_node`: registra prompt + raw answer + thinking + latencia de cada llamada del chat (context `chat:model`)
- [x] Captura en el pipeline batch: `generator_node` (context `pipeline:generator`) y `evaluator_node` (context `pipeline:evaluator`) en `exam_pipeline/nodes.py`
- [x] **Subclase `ReasoningCaptureChatOpenAI`** en `agents_backend/shared/llm.py`: langchain-openai 1.7.2 descarta el campo no-estándar `reasoning` que devuelve vLLM; la subclase lo recupera de `model_extra` del mensaje SDK y lo copia a `AIMessage.additional_kwargs["reasoning"]` para que `extract_thinking` pueda guardarlo

### 9.2 — Tool `delete_material_file` (core + agents-backend + exam-app)
- [x] `DeleteMaterialFileInput` en `core/domain/schemas/tools.py`: `subject_id`, `source_file` (exacto, de `list_subject_material`), `delete_physical_file` (default True)
- [x] Servicio `core/domain/material/service.py`: `delete_source_file()` (borra chunks por fuente + archivo físico bajo `MATERIAL_ROOT/<Materia>/` con guard anti path-traversal) y `delete_all_material()`
- [x] Refactor DRY: `DELETE /subjects/{id}/material` (exam-app `api/v1/exams.py`) ahora delega en el mismo servicio
- [x] Tool `delete_material_file_tool` en `conversational/tools.py` (tool 15 del agente); reporta chunks borrados y estado del archivo físico (`deleted`/`not_found`/`kept`/`unresolved`)
- [x] `SYSTEM_PROMPT`: regla 10 — eliminar material solo con pedido explícito, obtener `source_file` exacto de `list_subject_material`, confirmar antes de borrar
- [x] Registrada en `TOOLS` del grafo conversacional (14 → 15 tools)

### 9.3 — Descarga del JSON intermedio (core + agents-backend + exam-app + frontend)
- [x] `export_questions`: formato `json` (registros completos del banco: todos los campos, no solo las 17 columnas de tabla) + `artifact_ready` kind `json` + adjunto al chat
- [x] `generate_exam_pdf`: guarda `/output/exam_<pdf-stem>.json` con `{subject_id, subject_name, generated_at, num_versions, blueprint, items[]}` (datos crudos antes del render LaTeX) + `artifact_ready` kind `json` + enlace en la respuesta
- [x] `exam_app/main.py`: `_ALLOWED_OUTPUT_MIME` += `.json: application/json` (servible por `GET /output`)
- [x] Contrato del evento en 3 capas: `ArtifactReadyEvent.payload.kind` ahora `'pdf' | 'csv' | 'xlsx' | 'json'` en `agents_backend/shared/events.py`, `frontend/src/types/events.ts` y `ArtifactCard.vue` (icono 🧾 + label JSON)

### 9.4 — Inglés forzado en el prompt (agents-backend)
- [x] `SYSTEM_PROMPT`: regla **LANGUAGE** obligatoria (primera de las MANDATORY RULES) — responder SIEMPRE en inglés, use o no el profesor inglés; la traducción a otro idioma es un paso separado, nunca en el chat

### 9.5 — Infra y configuración (meta-repo)
- [x] `docker/docker-compose.yml`: `LLM_CAPTURE_RAW` y `LLM_CAPTURE_THINKING` (con defaults) en el servicio `exam-app`
- [x] `.env.example`: sección "LLM raw audit" documentando ambas variables

### 9.6 — Validación (sin pytest/vitest, regla del proyecto)
- [x] `py_compile` de todos los módulos tocados ✓
- [x] Smoke TestClient-style + SQLite (32 checks): registro con/sin thinking, master switch off, variantes de `extract_thinking`, delete material (chunks + físico + traversal + delete_all), schema de tools, reglas del prompt, registro de la tool 15 ✓
- [x] Migración aplicada en el contenedor (`entrypoint.sh` → `alembic upgrade head`): `e5f6a7b8c9d0 → f6a7b8c9d0e1`; tabla `llm_responses` verificada con `psql` ✓
- [x] Frontend: `npm run type-check` + `lint:check` + `build-only` ✓
- [x] E2E en Docker (chat real con GLM-5.3-Flash): llamada al chat → fila en `llm_responses` con prompt/answer/latencia ✓; prompt en español → respuesta en inglés ✓; "export in JSON" → JSON descargable con 31 preguntas y campos completos ✓; "delete the material file..." → chunks borrados (verificado en BD) ✓; "generate an exam PDF" → PDF + JSON con blueprint + 3 ítems ✓; thinking capturado con `LLM_CAPTURE_THINKING=true` ✓

---

## 🐛 Hallazgos técnicos de la etapa

| # | Hallazgo | Solución |
|---|---|---|
| 1 | langchain-openai 1.7.2 **descarta** el campo `reasoning` que vLLM devuelve para modelos de razonamiento (llega al SDK en `message.model_extra` pero `_convert_dict_to_message` no lo copia) | Subclase `ReasoningCaptureChatOpenAI._create_chat_result` que lo recupera y lo pone en `additional_kwargs["reasoning"]` |
| 2 | El servidor vLLM solo devuelve `reasoning` de forma consistente con `chat_template_kwargs: {enable_thinking: true}`; con `reasoning_effort` bajo devuelve trazas muy cortas o `None` | La captura es best-effort: si el servidor no envía la traza, `raw_thinking` queda NULL (no rompe nada) |
| 3 | `core.config.Settings` no tolera claves extra del `.env` de la raíz (`AUTH_SECRET` → `extra_forbidden` al correr desde el repo raíz) | Comportamiento preexistente, solo afecta runs locales desde la raíz; en Docker no aplica (sin `.env` en el working dir). Smoke tests corren desde `%TEMP%` |
| 4 | `Path('../evil.txt').name` = `evil.txt` (el `..` se pierde) | El guard anti-traversal resuelve contra la carpeta de la materia; un `../` se trata como nombre plano y el archivo simplemente no existe (no escapa) |

---

## ✅ Criterios de aceptación

- [x] Cada llamada al LLM del chat y del pipeline queda auditada en `llm_responses` (prompt + raw answer + latencia)
- [x] Con `LLM_CAPTURE_THINKING=true` la cadena de pensamiento se persiste cuando el servidor la envía; con `false` (default) queda NULL
- [x] Un fallo del logging de auditoría nunca rompe el chat ni el pipeline (best-effort verificado)
- [x] "Elimina el archivo X del material" en el chat borra los chunks (y el archivo físico si existe) vía el mismo service layer que el REST
- [x] "Exporta en JSON" descarga el banco completo en JSON; "genera examen" adjunta PDF + JSON crudo
- [x] El agente responde en inglés aunque el profesor escriba en español
- [x] `type-check` + `lint` + `build` del frontend sin errores; migración aplicada en Docker

---

## 📐 Decisiones de diseño

- **Tabla aparte `llm_responses`** (no columnas en `generated_questions`): audita TODAS las llamadas al LLM (chat + pipeline), no solo las preguntas guardadas; permite análisis futuro con un LLM más avanzado sin inflar la tabla del banco.
- **Captura best-effort con sesión propia**: la auditoría es observabilidad, no negocio; un fallo de BD en el logging no debe tumbar una generación de examen.
- **`raw_thinking` nullable + flag**: la traza de razonamiento depende del servidor (vLLM + parser de reasoning); guardarla es opcional y auditable por fila.
- **Servicio de material compartido**: la tool del chat y el endpoint REST comparten `core/domain/material/service.py` (una sola implementación del borrado, con guard de path-traversal).
- **JSON crudo junto al PDF**: el profesor (Felipe) pidió acceso a la data estructurada ANTES del render LaTeX para verificación; se emite como `artifact_ready` kind `json` (misma UX de descarga que PDF/CSV/XLSX).
- **Sin Vitest/Pytest** (regla del proyecto): validación con smoke script + E2E manual en Docker/navegador.

---

## 📝 Notas de sesión

### Sesión 2026-10-19 (implementación completa + E2E validado)

- **Alcance**: los 4 ítems pendientes de la segunda revisión cerrados de punta a punta; el 5.º (endpoint de modelo en caliente) quedó en backlog por decisión del usuario (el modelo ya es configurable por `.env`/compose sin tocar código).
- **Migración aplicada en el contenedor** tras rebuild de `exam-app`: `e5f6a7b8c9d0 → f6a7b8c9d0e1`; tabla + índices verificados con `psql`.
- **E2E real con GLM-5.3-Flash**: 14 filas de auditoría generadas durante las pruebas (limpiadas al final junto con el usuario de smoke); respuesta en inglés a prompt en español verificada; JSON de examen con blueprint + ítems validado; borrado de material verificado en BD (1 chunk, fuente `chat:material_prueba.txt`).
- **Descubrimiento clave**: el campo `reasoning` de vLLM no sobrevive el pipeline de langchain-openai; se necesitó la subclase `ReasoningCaptureChatOpenAI` (ver hallazgo 1). Sin ella, `LLM_CAPTURE_THINKING=true` no capturaba nada.
- **Pendiente conocido**: el attach a Open WebUI falla en el entorno actual (connection issue del bridge legacy) — el fallback de enlace directo `/output/` funciona; no bloquea (OpenWebUI es perfil legacy).

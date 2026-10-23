# Etapa 11 — Correcciones QA ronda 1 + certificación del flujo completo

> **Objetivo:** Cerrar la ronda de corrección derivada del QA de flujo completo en navegador ([10-qa-flujo-completo-navegador](./10-qa-flujo-completo-navegador/README.md)): completar los fixes P0/P1 que faltan, re-testear los ya aplicados y certificar el caso de uso central (profesor genera examen de 10 preguntas y descarga el ZIP) antes de congelar desarrollo (noviembre) y pasar al escrito de la tesis.
>
> **Estado:** ✅ Completada (fixes 11.1-11.6 aplicados y certificados en la ronda 3; ver [etapa 13](./13-qa-round3-navegador/README.md))
> **Depende de:** Etapas 0-9 (`Tag_V1.0.0` + stage 9) · QA ronda 1 (2026-10-19)
> **Fecha de última actualización:** 2026-10-23

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE

Validación: `py_compile` (backend), smoke scripts (TestClient + SQLite), `npm run type-check` / `lint:check` / `build-only` (frontend), rebuild Docker + E2E manual en navegador.

---

## 1. Estado actual (verificado en código, 2026-10-22)

### 1.1 Etapas del plan

| Etapa | Estado |
|---|---|
| 0, 2b, 2c, 3, 4, 5, 6, 7, 7a, 8, 9 | ✅ Completadas y validadas E2E |
| 1 (repos GitHub + submódulos + CI) | 🟨 Pendiente (repos locales listos, remotos no creados) |
| 2 (2.1-2.7) | 🟨 Completado salvo token streaming real (backlog) |
| **11 (esta etapa)** | 🟨 **En progreso** |

### 1.2 Fixes del QA ya APLICADOS en el working tree (sin commit)

Verificado contra el código real (no solo los docs del QA):

| Fix | Bugs | Archivos | Estado |
|---|---|---|---|
| RFC-01 nginx: `client_max_body_size 100m`, timeouts 3600s + `proxy_buffering off` en `/api/`, `location = /exams/generate` | BUG-02, 03, 05, 07 | `projects/frontend/nginx.conf` | ✅ Aplicado y certificado (ronda 3) |
| RFC-02 backend: heartbeat SSE `": ping\n\n"` cada ~15 s + propagación de frames crudos (`Union[SSEEvent, str]` en ports/engine/service/router) | BUG-03, 06, 07 | `exam_app/infrastructure/langgraph_engine.py`, `domain/ports.py`, `services/chat_engine.py`, `api/v1/chat.py` | ✅ Aplicado y certificado (ronda 3) |
| RFC-02 frontend: parser ignora frames de comentario, `useChatStream.retry()`, store `failMessage`/`clearMessageFailure`, UI "connection lost + Retry" (i18n en/es) | BUG-03, 06, 07 | `frontend/src/api/sse.ts`, `composables/useChatStream.ts`, `stores/chat.ts`, `ChatPanel.vue`, `MessageList.vue`, `i18n/{en,es}.ts` | ✅ Aplicado y certificado (ronda 3) |
| RFC-04 pipeline: fail-fast con `approved_items` vacío (`compiler_node` → `status="failed"`, `should_retry_compilation` → end, `generate_exam_pdf` → error con `rejection_log`), `rejection_log` + `total_llm_calls` en el JSON, errores de generator/evaluator logueados en `llm_responses` (`pipeline:generator_error` / `pipeline:evaluator_error`) | BUG-04 | `agents_backend/exam_pipeline/{nodes,graph}.py`, `conversational/tools.py` | ✅ Aplicado y certificado (ronda 3) |

### 1.3 Fixes PENDIENTES (verificados en código)

> **ACTUALIZACIÓN 2026-10-23:** los 6 fixes (11.1-11.6) fueron implementados y certificados E2E en la ronda 3 (ver [etapa 13](./13-qa-round3-navegador/README.md)). La tabla se conserva como registro histórico.

| # | Bug/Issue | Hallazgo en código | Fix |
|---|---|---|---|
| 1 | **BUG-01** (401 en Save/Save & verify del QuestionCard) | `QuestionCard.save()` envía `{message, thread_id, subject_id}` **sin `token`** en el body; `MessageList.vue` renderiza `<QuestionCard :question=…>` sin pasar `:subject-id`/`:thread-id`; `chat.py::_resolve_user` solo lee el token del body (sin fallback al header `Authorization` que `apiFetch` sí inyecta) | 11.1 ✅ certificado (C7) |
| 2 | **BUG-08** (exámenes legacy de otra materia en el historial) | `exams.py::list_subject_exams` mantiene el fallback que lista **todos** los PDFs no persistidos del output dir por prefijo de nombre, sin filtrar por materia | 11.2 ✅ cubierto por agrupado por base + filtro de huérfanos (ronda 2) |
| 3 | **BUG-10** (pending item consumido aunque el stream muera) | `save_pending_question` limpia el pending (`set_pending_item(None, None)`) después de guardar; si el stream muere tras la tool, el profesor no sabe si guardó y no hay re-consulta por statement | 11.3 ✅ certificado (C9) |
| 4 | **BUG-11** (HEAD /output → 405) | `main.py` registra solo `@app.get("/output/{filename}")` (verificado en vivo: `HEAD` → 405, `allow: GET`) | 11.4 ✅ certificado (C11) |
| 5 | **BUG-12 + ISS-07** (errores crudos / sin feedback) | `MaterialView.vue` muestra el texto crudo del status; `ExamsView.vue::generate()` tiene `catch {}` vacío (formulario queda abierto sin mensaje) | 11.5 ✅ certificado (C12) |
| 6 | **ISS-10** (tablas markdown desbordan) | `MarkdownRenderer.vue` tiene `overflow-x` en `pre` pero no en `table` | 11.6 ✅ certificado (C13) |

### 1.4 Fixes ya cubiertos sin código nuevo

- **BUG-09** (contadores de contexto): `AppHeader.onSubjectChange` ya refetch-ea `bank`/`material`/`exams` al cambiar de materia y los chips leen de esos stores → cubierto por RFC-06. Re-test en certificación.
- **ISS-06** (Content-Disposition): `FileResponse(filename=…)` ya lo provee; solo falta HEAD (11.4).

### 1.5 Higiene del repositorio (pendiente)

- Commit de los cambios en los 3 submódulos (`agents-backend`, `exam-app`, `frontend`) — los fixes P0 están sin commit.
- Commit de la carpeta QA `implementaciones/10-qa-flujo-completo-navegador/` (untracked) y de esta etapa 11.
- Eliminar el archivo basura `-w` en la raíz del meta-repo si reaparece.
- Actualizar punteros de submódulos en el meta-repo tras los commits.

---

## 2. Plan de implementación (tareas 11.1 – 11.6)

### 11.1 — BUG-01: HITL por botones del QuestionCard (RFC-03) · P1 · S

- [ ] `frontend/src/components/widgets/QuestionCard.vue`: en `save()` añadir `token: getAuthToken()` al body (import de `@/api/http`).
- [ ] `frontend/src/components/chat/MessageList.vue`: pasar `:subject-id="chat.activeSubjectId"` y `:thread-id="chat.threadId"` al `<QuestionCard>` (importar `useChatStore`).
- [ ] (Defensa en profundidad) `exam_app/api/v1/chat.py::_resolve_user`: aceptar `Authorization: Bearer` como fallback si `req.token` es None (necesita acceso al `Request`; mantener el body como fuente primaria para SSE).
- [ ] Criterio: generar pregunta → `Save` guarda (badge Saved) y `Save & verify` guarda + verifica (badge Verified); el banco refleja el estado sin recargar.

### 11.2 — BUG-08: historial de exámenes por materia (RFC-05) · P1 · M

- [ ] Script de migración one-shot (`scripts/`): para cada PDF legacy del output dir, inferir materia (del JSON hermano si existe; si no, `subject_id=NULL`) e insertar fila en `exams`.
- [ ] `exam_app/api/v1/exams.py::list_subject_exams`: eliminar el fallback por prefijo; listar solo filas de la tabla (el scoping por `subject_id` + owner ya existe).
- [ ] Los PDFs sin materia quedan fuera del listado (visibles solo vía `/output/`).
- [ ] Criterio: con Base de Datos activa, la vista Exams solo muestra exámenes de esa materia.

### 11.3 — BUG-10: idempotencia del guardado HITL (RFC-02 parte) · P1 · S

- [ ] `agents_backend/conversational/tools.py::save_pending_question`: emitir `question_saved` **antes** de limpiar el pending; si el guardado falla, NO limpiar el pending.
- [ ] Tolerar re-consulta: si no hay pending pero el banco ya tiene la pregunta (match por statement + subject), responder con el estado real ("ya estaba guardada, id X, verificada: sí/no") en vez de "no pending question left to save".
- [ ] Criterio: matar el stream tras un guardado → re-preguntar "did my question get saved?" devuelve el estado real del banco.

### 11.4 — BUG-11: HEAD en /output · P2 · XS

- [ ] `exam_app/main.py`: `@app.api_route("/output/{filename}", methods=["GET", "HEAD"])`.
- [ ] Criterio: `HEAD /output/<file>.pdf` → 200 con los headers de GET.

### 11.5 — BUG-12 + ISS-07: mensajes de error accionables · P2 · S

- [ ] `frontend/src/api/http.ts` (o helper): mapear 413 → "El archivo supera el tamaño máximo (100 MB)…", 401 → sesión expirada, 403 → sin permisos.
- [ ] `frontend/src/views/MaterialView.vue`: usar el mensaje mapeado en `uploadMessage`.
- [ ] `frontend/src/views/ExamsView.vue`: banner de error en el formulario (mostrar `e.message` del catch, hoy vacío) + mantener el botón deshabilitado mientras `generating`.
- [ ] i18n: claves nuevas en `en.ts`/`es.ts`.
- [ ] Criterio: subir archivo > límite muestra guía; fallo de generación muestra el detalle en el formulario.

### 11.6 — ISS-10: overflow-x en tablas markdown · P2 · XS

- [ ] `frontend/src/components/chat/MarkdownRenderer.vue`: `display: block; overflow-x: auto;` en `:deep(table)`.
- [ ] Criterio: tabla ancha de `search_questions` scrollea dentro de la burbuja.

### Post-V1 (no bloquea la certificación)

- ISS-01 (indexación en background), ISS-02 (progreso del pipeline en el chat), ISS-03/04 (paginación Banco/chat), ISS-05 (RFC-07 `content_language`), ISS-08 (advertencia de duplicados), ISS-09 (refresh de materias tras `done`), tests E2E Playwright, dedup con embeddings reales, endpoint de modelo en caliente.

---

## 3. Plan de ejecución

### 3.1 Orden de trabajo (una sesión)

1. **Bloque A — fixes P1/P2 restantes** (11.1 → 11.3 → 11.4 → 11.5 → 11.6): un commit por submódulo al cerrar cada bloque coherente.
2. **Bloque B — validación estática**: `py_compile` de módulos tocados (en contenedor o local), `npm run type-check` + `lint:check` + `build-only`.
3. **Bloque C — rebuild Docker**: `docker compose -f docker/docker-compose.yml build frontend exam-app && docker compose -f docker/docker-compose.yml up -d` (el rebuild de `exam-app` aplica el código nuevo; la migración 11.2 corre por `entrypoint.sh` → `alembic upgrade head` si hay migración).
4. **Bloque D — certificación E2E** (sección 4) en `http://localhost:3000`.
5. **Bloque E — commits + punteros**: commits en submódulos → commit del meta-repo (punteros + `implementaciones/`).

### 3.2 Convenciones

- **Commits atómicos por submódulo** (convención etapa 8): `fix(qa): ...` con el/los bugs resueltos en el cuerpo; el meta-repo solo actualiza punteros + docs.
- **Sin pytest/vitest** (regla del proyecto): smoke script TestClient+SQLite solo si se toca lógica de servicio (11.2/11.3).
- **Contrato SSE en 3 capas**: cualquier cambio de eventos debe reflejarse en `agents_backend/shared/events.py` → `exam_app/schemas/events.py` → `frontend/src/types/events.ts` (no aplica a los fixes actuales, recordatorio).
- **Calendario**: desarrollo cierra en noviembre (defensa 14-21 dic). Esta etapa es el último bloque de código antes del escrito.

---

## 4. Plan de certificación (checklist E2E final)

> Ejecutar en Docker con el stack completo (`exam_frontend`, `exam_app`, `exam_postgres_db`, `exam_latex_compiler`, `exam_embedding_service`) y LLM accesible. Todo desde el navegador en `http://localhost:3000` (regla del QA).

### 4.1 P0 — caso de uso central (definition of done del backlog)

- [ ] **C1. Login multi-profesor** y registro de materia nueva; el selector del navbar la muestra.
- [ ] **C2. Subida de material ≥ 5 MB** (PDF real) desde Material → indexa sin 413 (BUG-05/RFC-01); mensaje de éxito con nº de chunks.
- [ ] **C3. Examen por chat**: "Generate an exam for <materia> with 10 questions, 2 versions" → confirmar nombre/versiones → el turno **completa sin cortarse** (> 60 s), llega `artifact_ready`, el ZIP se descarga y contiene las 2 versiones (con/sin respuestas) (BUG-03/07 + RFC-01/02).
- [ ] **C4. El examen aparece en la vista Exams de ESA materia** (y no en otras) (BUG-08 tras 11.2).
- [ ] **C5. Formulario Exams**: "+ Generate exam" (10 preguntas) → genera, refresca la lista y cierra el formulario (BUG-02/RFC-01).
- [ ] **C6. Pipeline sin ítems aprobados**: forzar fallo (p. ej. LLM inaccesible) → NO compila PDFs, NO publica ZIP, el chat recibe el error con `rejection_log` (BUG-04/RFC-04).

### 4.2 P1 — HITL y consistencia

- [ ] **C7. QuestionCard**: `Save` → badge Saved; `Save & verify` → badge Verified; el banco refleja el estado sin recargar (BUG-01 tras 11.1).
- [ ] **C8. Stream muerto a mitad de turno**: matar `exam_app` (o cortar red) → la burbuja muestra "⚠️ connection lost" + botón Retry; Retry reenvía el turno (BUG-06/07/RFC-02).
- [ ] **C9. Guardado HITL tras stream muerto**: re-preguntar por el guardado devuelve el estado real del banco (BUG-10 tras 11.3).
- [ ] **C10. Contadores de contexto**: cambiar de materia en el navbar → chips de preguntas/chunks se refrescan (BUG-09/RFC-06).

### 4.3 P2 — calidad

- [ ] **C11. HEAD /output/<file>** → 200 (BUG-11 tras 11.4); GET descarga con `Content-Disposition` (ISS-06).
- [ ] **C12. Errores accionables**: subida > límite → mensaje con guía (BUG-12); fallo del formulario Exams → banner con detalle (ISS-07).
- [ ] **C13. Tabla markdown ancha** scrollea dentro de la burbuja (ISS-10).

### 4.4 Regresión (no romper lo que ya funcionaba)

- [ ] **R1. HITL textual**: generar → revisar → "yes, save it and mark it as verified by human" → guardado + verificado.
- [ ] **R2. Guardrail**: pedir borrar una pregunta verificada → el agente se niega e indica el procedimiento.
- [ ] **R3. Selector de materia**: sincronización bidireccional navbar ↔ vista Subjects ↔ chat.
- [ ] **R4. Banco**: filtros por topic/difficulty/verification, detalle, toggle de verificación.
- [ ] **R5. Exportaciones**: CSV/XLSX/JSON del banco y JSON del examen descargables.
- [ ] **R6. Auditoría LLM**: filas nuevas en `llm_responses` (incluye contextos `pipeline:generator_error`/`evaluator_error` si hubo fallos).
- [ ] **R7. Idioma**: prompt en español → respuesta del agente en inglés.

### 4.5 Cierre

- [ ] Todos los checks marcados → etiquetar `Tag_V1.1.0` (QA round 1 corregido) en los 3 submódulos + meta-repo.
- [ ] Actualizar `docs/informe_avance.md` (sección 1.2/1.3) con el cierre de la ronda QA.
- [ ] Etapa 1 (repos GitHub + CI) queda como único pendiente de desarrollo, sin bloquear el escrito.

---

## 5. Trazabilidad bugs ↔ fixes ↔ certificación

| Bug/Issue | Severidad | RFC | Fix (sección) | Check certificación |
|---|---|---|---|---|
| BUG-01 | 🔴 | RFC-03 | 11.1 | C7 |
| BUG-02 | 🔴 | RFC-01 | ✅ aplicado | C5 |
| BUG-03 | 🔴 | RFC-01+02 | ✅ aplicado | C3, C8 |
| BUG-04 | 🔴 | RFC-04 | ✅ aplicado | C6 |
| BUG-05 | 🟠 | RFC-01 | ✅ aplicado | C2 |
| BUG-06 | 🟠 | RFC-02 | ✅ aplicado | C8 |
| BUG-07 | 🟠 | RFC-01+02 | ✅ aplicado | C3, C8 |
| BUG-08 | 🟡 | RFC-05 | 11.2 | C4 |
| BUG-09 | 🟡 | RFC-06 | ✅ cubierto (AppHeader) | C10 |
| BUG-10 | 🟡 | RFC-02 | 11.3 | C9 |
| BUG-11 | ⚪ | — | 11.4 | C11 |
| BUG-12 | ⚪ | — | 11.5 | C12 |
| ISS-06 | ⚪ | — | ✅ cubierto (FileResponse) | C11 |
| ISS-07 | 🟡 | — | 11.5 | C12 |
| ISS-10 | ⚪ | — | 11.6 | C13 |
| ISS-01/02/03/04/05/08/09 | — | RFC-07 etc. | Post-V1 | — |

---

## 📝 Notas de sesión

### Sesión 2026-10-22 (análisis + plan)

- Verificación código-real de los 12 bugs + 10 issues del QA: **P0 (RFC-01/02/04) ya aplicado** en el working tree de los 3 submódulos (sin commit); BUG-09 e ISS-06 cubiertos sin código nuevo; quedan 11.1-11.6.
- Validación estática del estado actual: `py_compile` exam-app + agents-backend OK en contenedor; `type-check` + `lint:check` + `build-only` del frontend OK.
- Smoke de infraestructura con el stack levantado: `POST /exams/generate` proxificado (422 de validación Pydantic = llega al backend, ya no 405) ✔; `HEAD /output` → 405 (confirma 11.4) ✔; `POST /api/chat` sin token → 401 limpio ✔.
- Docker Desktop no estaba corriendo; se levantó y el stack completo quedó healthy.

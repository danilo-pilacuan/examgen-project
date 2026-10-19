# Etapa 8 — Auth multi-profesor + navbar reactivo + CRUD completo (Tag V1.0.0)

> **Objetivo:** Cerrar el MVP para múltiples profesores: esquema de autenticación JWT con scoping por profesor (multi-tenant), nueva UX con navbar superior y selector de materia reactivo (bidireccional con el chat), y CRUD completo del banco de preguntas desde el chat.
>
> **Estado:** ✅ Completada (validada E2E en Docker y en navegador; tag `Tag_V1.0.0`)
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapas 0-7
> **Fecha de última actualización:** 2026-10-19

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE

## 📋 Tareas

### 8.1 — Auth backend (multi-tenant)
- [x] `core/domain/models.py`: modelo `User` (email único, name, password_hash, role) + `subjects.owner_id` (FK nullable; NULL = materia legacy compartida, retrocompatible)
- [x] Migración Alembic `e5f6a7b8c9d0_add_users_and_subject_ownership` (cadena: `d4e5f6a7b8c9` → `e5f6a7b8c9d0`)
- [x] `core/domain/auth.py`: hashing PBKDF2-HMAC-SHA256 (240k iteraciones, formato `pbkdf2$iter$salt$hash`), JWT HS256 (12h, secret vía `AUTH_SECRET`), dependencias FastAPI `get_db` + `get_current_user` (HTTPBearer)
- [x] `exam-app/api/v1/auth.py`: `POST /auth/register` (409 si email duplicado), `POST /auth/login` (401 credenciales inválidas), `GET /auth/me`
- [x] Scoping por profesor: `GET/POST /subjects`, `GET /subjects/{id}/questions`, `PUT /questions/{id}/verification`, `DELETE /questions/{id}`, `GET/DELETE /subjects/{id}/material`, `GET /subjects/{id}/exams`, `POST /api/files` — todos filtran por `owner_id` (403 si la materia es de otro profesor; las legacy `owner_id IS NULL` siguen visibles para todos)
- [x] `POST /api/chat` y `/api/chat/stream`: token JWT en el **body** (SSE POST del navegador no siempre puede mandar header Authorization) + validación de propiedad de la `subject_id` del contexto
- [x] `pyproject.toml` de exam-app + `requirements.txt`: dependencia `pyjwt>=2.8.0`

### 8.2 — Auth frontend
- [x] `views/AuthView.vue`: login/registro con tabs, validación de formulario, errores del store
- [x] `stores/auth.ts`: sesión persistente en `localStorage` (`mvp_auth`), token restaurado **sincrónicamente** al crear el store (evita race con fetches de setup), `bootstrap()` valida contra `/auth/me` al recargar (token expirado → logout)
- [x] `api/http.ts`: inyección automática de `Authorization: Bearer` en todos los fetch
- [x] `api/sse.ts`: token en el body del stream del chat
- [x] `router/index.ts`: guard global — toda ruta excepto `/login` exige sesión; `/login` redirige a `/` si ya hay sesión

### 8.3 — Navbar superior reactivo (sidebar retirada)
- [x] `components/layout/AppHeader.vue`: navbar con navegación (Chat · Bank · Exams · Material · Subjects), **selector de materia** con botón `+` (crear materia al instante), switch EN/ES, menú de usuario con logout
- [x] **Barra de contexto** bajo el header: materia activa + contadores reactivos de preguntas y chunks
- [x] `App.vue`: un solo `RouterView` **dentro** del layout (`app-layout → header + context-bar + main-view → vista`); el header ya no renderiza el suyo (evita DOM duplicado)
- [x] `ChatPanel.vue`: indicador de contexto del chat (`Context: {materia}` / `No subject selected`)
- [x] `ChatView.vue`: `FileUpload` duplicado eliminado (solo `FileDrop` con drag & drop)

### 8.4 — Contexto bidireccional selector ↔ chat
- [x] **Selector → app**: `onSubjectChange` actualiza `subjects` + `chat` stores y refresca banco/material/exámenes; las vistas reaccionan por `watch(activeSubjectId)` (fetch propio de materias eliminado de las vistas)
- [x] **Chat → selector**: nueva tool `select_subject` (agents-backend) que emite el evento `subject_selected`; `ChatPanel.applyChatSubject()` sincroniza selector + stores (registra la materia si el agente la acaba de crear) y refresca los paneles
- [x] Evento `SUBJECT_SELECTED` en `agents_backend/shared/events.py`, en el `Literal` de `exam_app/schemas/events.py` y en `frontend/src/types/events.ts`
- [x] `SYSTEM_PROMPT`: regla 8 — el agente DEBE llamar `select_subject` (no solo decir que seleccionó); regla CRUD para update/delete
- [x] i18n: claves `auth.*`, `app.selectSubject`, `app.questionsChip`, `app.chunksChip`, `chat.contextWith/contextNone`, `chat.events.subject_selected`

### 8.5 — CRUD completo del banco desde el chat
- [x] `core/domain/schemas/tools.py`: `UpdateQuestionInput` (todos los campos opcionales = update parcial) y `DeleteQuestionInput`
- [x] `agents_backend/conversational/tools.py`: `update_question_tool` (delega en `bank.update_question`) y `delete_question_tool` (delega en `bank.delete_question`); errores de guardrail se reportan con 🔒
- [x] Guardrails heredados del service layer: preguntas `verified_by_human` **no** pueden modificarse ni borrarse (`SecurityError`)
- [x] `SYSTEM_PROMPT`: nunca inventar `question_id` (obtenerlo de `search_questions`); nunca borrar sin pedido explícito

### 8.6 — Infra y despliegue
- [x] `nginx.conf`: `Cache-Control: no-cache` para `index.html` (evita bundle obsoleto tras cada deploy; `/assets/` sigue con cache inmutable de 1 año)
- [x] `AUTH_SECRET` aleatorio (48 chars) agregado al `.env` local (consumido por compose vía `env_file`)
- [x] Despliegue Docker validado: rebuild de `exam-app` + `frontend`, migración aplicada al arrancar (`entrypoint.sh` → `alembic upgrade head`), tabla `users` verificada en Postgres

---

## 🐛 Bugs encontrados y corregidos durante la etapa

| # | Síntoma | Causa raíz | Fix |
|---|---|---|---|
| 1 | Pantalla en blanco (`SyntaxError: 10` en producción) | El `@` de `professor@university.edu` es sintaxis *linked message* de vue-i18n (`INVALID_LINKED_FORMAT` = código 10) | Escapar como `{'@'}` en los catálogos (con comillas dobles TS para no romper el parseo) |
| 2 | Chat renderizado dos veces | `RouterView` en `App.vue` **y** en `AppHeader.vue` | Un solo `RouterView` dentro del layout |
| 3 | Selector no actualizaba el nombre de la materia en el chat | Colisión getter/estado con el mismo nombre (`activeSubjectName`) en el store Pinia: la acción escribía al getter (solo lectura) y fallaba en silencio | Getter redundante eliminado (reemplazado por `hasActiveSubject`) |
| 4 | Evento `subject_selected` mataba el stream (`ValidationError` en exam-app) | `SSEEvent.type` es un `Literal` que no incluía el nuevo evento | Agregado al `Literal` (contrato espejado en 3 capas) |
| 5 | `NameError: get_db` al importar auth | `get_current_user` usaba `Depends(get_db)` antes de la definición | `get_db` movido antes de `get_current_user` |
| 6 | `NameError: sid` en `list_subject_questions` | El reemplazo del bloque de validación borró la variable que usaba `list_questions` | `_get_owned_subject` devuelve el subject y se extrae `sid` |
| 7 | Dropdown de materias vacío tras recargar la página | El header hacía `fetch` antes de que `auth.bootstrap()` restaurara el token | Token restaurado sincrónicamente en `state()` del store + `watch(isAuthenticated)` en el header |
| 8 | `Depends()` vacío hacía que FastAPI introspectara `Session.__init__` (pydantic `ForwardRef('JoinTransactionMode')` sin resolver) | `db: OrmSession = Depends()` usa la **clase** como dependencia | `Depends(get_db)` explícito |
| 9 | Bundle viejo en el navegador tras cada deploy | nginx cacheaba `index.html` (que referencia los hashes del bundle) | `no-cache, must-revalidate` en `index.html` |

---

## ✅ Criterios de aceptación

- [x] Registro/login/logout funcionan; sesión persiste entre recargas; token expirado → logout automático
- [x] Sin token: 401 en materias/banco/material/exámenes/chat; con token de otro profesor: 403 en materias ajenas
- [x] Materias legacy (`owner_id NULL`) visibles para todos (retrocompatibilidad con datos existentes)
- [x] Selector del header actualiza chat + banco + material + exámenes en vivo
- [x] "Selecciona la materia X" en el chat actualiza el selector del header en tiempo real (durante el streaming)
- [x] CRUD completo desde el chat verificado E2E: update de dificultad persistido en BD (verificado vía API), delete persistido (17→16 preguntas), guardrail 🔒 en preguntas verificadas
- [x] `npm run type-check` + `lint:check` + `build-only` ✓; `py_compile` de todos los módulos tocados ✓
- [x] Tests unitarios de las tools CRUD (SQLite en memoria): update 1 campo, update múltiple, inexistente, delete, delete duplicado, guardrails ✓
- [x] Desplegado en Docker local y validado en navegador integrado (flujo completo con cuenta real)

---

## 📐 Decisiones de diseño

- **Token en el body del chat** (no header): el cliente SSE usa `fetch` POST y el patrón del proyecto no adjunta headers al stream; el body es simple y compatible. Los endpoints REST sí usan `Authorization: Bearer`.
- **`owner_id` nullable**: las materias creadas antes de la auth quedan **compartidas** (visibles para todos los profesores) en vez de romper los datos existentes. Asignación retroactiva posible con `UPDATE subjects SET owner_id=...`.
- **HITL del CRUD por prompt** (igual que guardar/verificar): el agente pregunta/obtiene el id antes de escribir; el guardrail duro vive en el service layer (independiente del LLM).
- **Un solo `RouterView`** en el layout: el header es *chrome* de navegación, no contenedor de vistas.
- **Sin Vitest/Pytest** (regla del proyecto): validación con type-check, lint, build, smoke tests con TestClient/SQLite y E2E manual en navegador.

---

## 📝 Notas de sesión

### Sesión 2026-10-18/19 (implementación completa + Tag V1.0.0)

- **Alcance**: auth multi-profesor de punta a punta, re-UX con navbar superior, contexto bidireccional selector↔chat, CRUD completo del banco desde el chat, despliegue Docker local validado en navegador.
- **Migración aplicada en el contenedor** (`entrypoint.sh` ya ejecuta `alembic upgrade head`): `d4e5f6a7b8c9 → e5f6a7b8c9d0`; tabla `users` + `subjects.owner_id` verificadas con `psql`.
- **E2E auth (TestClient + SQLite)**: register OK (JWT 289 chars), duplicado 409, password errónea 401, `/me` OK, sin token 401; scoping: profesor A crea materia → A la ve, B no la ve, B bloqueado 403 en su banco, materias legacy accesibles por B.
- **E2E en navegador (cuenta real)**: login → header completo; selector → `Context: {materia}` + barra de contexto con contadores; "Selecciona la materia Ingles Tecnico" → selector cambia solo; "Ahora trabaja con Economía Aplicada" → ídem; banco reacciona al selector estando en la vista Bank; logout → login.
- **E2E CRUD en navegador**: "Busca una pregunta del banco y cámbiale la dificultad a hard" → el agente lista 5 y pregunta cuál; "La primera" → `✅ ...dificultad hard` (BD verificada: hard 1→2); "Elimina esa pregunta..." → `🗑️ Pregunta eliminada` (BD verificada: total 17→16, hard 2→1).
- **Hallazgo de contrato**: al agregar un evento nuevo hay que tocarlo en **3 capas** (`agents_backend/shared/events.py` → `exam_app/schemas/events.py` → `frontend/src/types/events.ts`); si se omite exam-app, el stream muere con `ValidationError` a mitad de turno (síntoma: `ERR_INCOMPLETE_CHUNKED_ENCODING` en el navegador).
- **Commits y tag**: un commit por submódulo (core `55ea3b7`, agents-backend `fa9359a`, exam-app `0902858`, frontend `2abdbed`) + meta-repo `b498569` (punteros + requirements + doc de revisión); tag anotado `Tag_V1.0.0` en el meta-repo y en los 4 submódulos. Remotos GitHub siguen pendientes (etapa 1).
- **Pendiente conocido**: asignar `owner_id` a las materias legacy si se quiere privacidad retroactiva; `AUTH_SECRET` debe definirse en producción (el fallback de dev es inseguro por diseño).

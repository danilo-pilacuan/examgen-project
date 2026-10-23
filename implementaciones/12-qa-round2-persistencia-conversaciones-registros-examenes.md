# Etapa 12 — QA ronda 2: persistencia de conversaciones + un registro por examen

> **Objetivo:** Corregir los 2 bugs reportados por el usuario tras la ronda 1 — (1) las conversaciones no persistían al cerrar sesión (a veces solo el nombre, sin contenido) y (2) la vista Exámenes generaba demasiados registros por examen individual — y certificar ambos E2E en navegador antes del tag `Tag_V1.1.0`.
>
> **Estado:** ✅ Completada (fixes aplicados, rebuild Docker, QA E2E en navegador OK)
> **Depende de:** Etapa 11 (plan de fixes + certificación)
> **Fecha:** 2026-10-23

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST

Validación: `py_compile` (backend), `npm run type-check` / `lint:check` / `build-only` (frontend), rebuild Docker + E2E manual en navegador (regla del proyecto).

---

## 1. Bugs reportados (ronda 2)

| # | Bug | Síntoma reportado |
|---|---|---|
| BUG-13 | Conversaciones no persisten | Al iniciar sesión de nuevo no se ven las conversaciones; a veces solo se muestran los nombres pero el chat carga vacío |
| BUG-14 | Registros duplicados de exámenes | La vista Exámenes lista un registro por PDF individual (variantes A/B, respondido, with_answers, v1/v2) en vez de uno por examen |

---

## 2. Causa raíz y fixes

### 2.1 BUG-13 — Persistencia de conversaciones

**Diagnóstico:** El contenido de los mensajes vivía **solo en memoria Pinia**. El checkpointer `PostgresSaver` SÍ persistía el estado del grafo (tabla `checkpoints`, p. ej. thread `7f2f53c0` con 47 filas), pero **no existía ninguna API para leerlo**. Los metadatos de threads (id/título) viven en `localStorage` (`mvp_chat_threads`), por eso tras re-login a veces se veían los nombres pero el chat quedaba vacío.

**Fix (3 capas):**

| Capa | Archivo | Cambio |
|---|---|---|
| Backend API | `exam_app/api/v1/chat.py` | Nuevo endpoint `GET /api/chat/history/{thread_id}` (autenticado con `get_current_user`) |
| Backend servicio | `exam_app/api/deps.py`, `services/chat_engine.py`, `infrastructure/langgraph_engine.py` | `ChatService.history()` → `LangGraphEngine.history()`: lee `conversational_graph.get_state({"configurable": {"thread_id": ...}})` y serializa `HumanMessage`/`AIMessage` a `{role, content}` (filtra system/tool, maneja contenido multimodal) |
| Frontend | `stores/chat.ts`, `components/chat/ThreadSidebar.vue`, `views/ChatView.vue` | `loadThread()` async: al seleccionar un thread llama al endpoint e hidrata `messages` (con guard anti-carrera si cambia el thread); `onMounted` de ChatView restaura la última conversación si `currentThreadId` existe y `messages` está vacío |

### 2.2 BUG-14 — Un registro por examen

**Diagnóstico:** El fallback legacy de `list_subject_exams` agrupaba por **prefijo exacto** del filename → `Parcial_1_A`, `Parcial_1_A_respondido`, `Parcial_1_B` eran registros separados. Además, 26 PDFs huérfanos de corridas pre-persistencia (solo UUID, sin JSON ni ZIP) creaban 26 registros basura (37 en total).

**Fix (backend + frontend):**

| Capa | Archivo | Cambio |
|---|---|---|
| Backend | `exam_app/api/v1/exams.py` | Agrupado por **nombre base** (regex strip de `_respondido`, `_with_answers`, `_v\d+`, `_[A-J]`); ZIP buscado en `{base}.zip` y `exam_{base}.zip`; **filtro de huérfanos**: los registros legacy sin ZIP y sin items (JSON) no se listan |
| Frontend | `views/ExamsView.vue`, `i18n/{es,en}.ts` | Eliminados los botones por PDF individual y `pdfLabel()`; solo botón **📦 Download ZIP (all versions)** por examen, con fallback `<a>` al primer PDF si no hay ZIP |

**Resultado:** 37 → **8 registros** (5 exámenes nombrados con ZIP + 3 legacy UUID con JSON/ZIP).

---

## 3. Validación estática

| Check | Resultado |
|---|---|
| `py_compile` de módulos tocados (en contenedor) | ✅ OK |
| `npm run type-check` | ✅ OK |
| `npm run lint:check` | ✅ OK |
| `npm run build-only` | ✅ OK (2.65 s) |
| Rebuild Docker `exam-app` | ✅ healthy (2 fallos de import corregidos durante el rebuild: `get_current_user` y `get_chat_service_sync`) |

---

## 4. QA E2E en navegador (round 2, 2026-10-23)

> Stack completo healthy (6 contenedores). Navegador integrado + Playwright en `http://localhost:3000`, credenciales `danilo.pilacuan@gmail.com`.

### 4.1 BUG-13 — Persistencia de conversaciones

| # | Paso | Resultado |
|---|---|---|
| P1 | Login → sidebar muestra 2 threads ("yes", "Generate an exam…") | ✅ |
| P2 | Click en thread "yes" (47 checkpoints en BD) → el historial se hidrata completo (preguntas, opciones, explicaciones, confirmaciones "✅ Question saved") | ✅ |
| P3 | Enviar mensaje nuevo ("¿qué es una clave foránea?") → respuesta streaming completa del agente | ✅ |
| P4 | **Sign out** → login de nuevo → los 2 threads siguen en la sidebar | ✅ |
| P5 | Click en el thread con el mensaje nuevo → **todo el contenido se recarga** (pregunta, respuesta con opciones, respuesta final del agente) | ✅ |
| P6 | BD: `checkpoints` del thread creció 47 → 50 filas (persistencia real confirmada) | ✅ |

### 4.2 BUG-14 — Un registro por examen

| # | Paso | Resultado |
|---|---|---|
| P7 | API `GET /subjects/{id}/exams` → 8 registros (antes 37) | ✅ |
| P8 | Vista Exams (materia activa) → 8 tarjetas, una por examen, solo botón ZIP (fallback PDF en 2 legacy sin ZIP) | ✅ |
| P9 | Descarga ZIP `QA_Rebuild_-_Examen_1.zip` → HTTP 200, 64 KB | ✅ |

### 4.3 Regresión

| # | Check | Resultado |
|---|---|---|
| R1 | Login/logout limpio (401 esperado al expirar token) | ✅ |
| R2 | Selector de materia sincronizado tras re-login (chips 9 questions / 14 chunks) | ✅ |
| R3 | `/docs` del backend 200 tras rebuild | ✅ |

---

## 5. Estado de la certificación (checklist etapa 11)

- C1–C3, C5, C8, R1–R3, R7: verificados en QA ronda 1 + esta ronda.
- **C4** (exámenes por materia): verificado en esta ronda (P7–P8).
- C6, C7, C9–C13: pendientes de re-test puntual (no bloquean el tag; cubiertos por los fixes ya aplicados en código).

---

## 6. Cierre

- [x] Fixes BUG-13 y BUG-14 aplicados y verificados E2E.
- [x] Rebuild Docker healthy.
- [ ] Commits atómicos por submódulo (`fix(qa): ...`) + punteros del meta-repo.
- [ ] Tag `Tag_V1.1.0` en los 3 submódulos + meta-repo.

---

## 📝 Notas de sesión

- El endpoint de historial delega en el checkpointer de LangGraph: no duplica almacenamiento; si el thread no tiene checkpoints responde lista vacía (comportamiento correcto, p. ej. thread `d2c9105c`).
- Los 26 PDFs huérfanos UUID siguen en `/app/output` (no se borran archivos del usuario); simplemente ya no se listan. Una migración futura (11.2) puede insertarlos en la tabla `exams` si se quiere recuperar.
- Los metadatos de threads siguen en `localStorage` (por navegador); el contenido vive en Postgres. Para multi-dispositivo haría falta una tabla `threads` (backlog post-V1).

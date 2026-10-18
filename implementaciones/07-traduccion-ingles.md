# Etapa 7 — Traducción completa del sistema al inglés

> **Objetivo:** Dejar TODO el sistema en inglés: UI del frontend, prompts del agente, nombres de tools, mensajes y errores, valores de enums, etiquetas de tablas, plantillas LaTeX, textos de compose y comentarios. Traducción **archivo por archivo** (sin reemplazos masivos).
>
> **Estado:** ✅ Completada (7.1-7.8 ✅; ver notas de sesión 2026-10-18)
> **Sesiones estimadas:** 3-4
> **Depende de:** Etapas 0-6
> **Fecha de última actualización:** 2026-10-18

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE

## ⛔ Reglas de la etapa

1. **NO tocar la DGX** — nada de SSH ni `deploy/*.sh` (ver regla crítica en el README de esta carpeta).
2. **Archivo por archivo, sin reemplazos masivos**: prohibido el `sed`/PowerShell-replace global sobre muchos archivos (precedente: mojibake de emojis en la etapa 0). Un archivo → revisar → commit.
3. **UTF-8 limpio**: tras editar, verificar que no se rompieron acentos/emojis.
4. **El contrato se rompe en 7.1 y se repara en orden**: enums (core) → migración de BD → frontend types → resto. No mezclar pasos.
5. **NO se traduce**: datos del usuario en la BD (preguntas/materias/material ya guardados), historial de chats viejos, `data/`, `Requisitos/` y `plan-frontendChatEmbebido.prompt.md` (documentos fuente históricos).
6. **Ya está en inglés y NO cambia**: nombres de eventos SSE (`question_generated`, `artifact_ready`, …), campos de API (`verified_by_human`, `thread_id`, …), el tag `<file id="..."/>`, nombres de servicios Docker y variables de entorno (`DATABASE_URL`, `LLM_BASE_URL`, …).

## 🗺 Orden de trabajo (contrato primero)

> **Mapa de dependencias:** ver [07a-mapa-dependencias.md](./07a-mapa-dependencias.md) — grafo `frontend → exam-app → agents-backend → core`, contratos compartidos y riesgos de desincronización.

| Paso | Qué | Por qué en este orden |
|---|---|---|
| 7.1 | Enums + labels en `core` | Define el contrato nuevo |
| 7.2 | Migración Alembic de datos | La BD existente queda legible |
| 7.3 | Tools + prompts (agents-backend) | El LLM usa el contrato nuevo |
| 7.4 | exam-app | Mensajes de API al inglés |
| 7.5 | Frontend | Tipos + UI alineados al contrato, **con i18n (vue-i18n, en/es)** |
| 7.6 | LaTeX | PDFs en inglés |
| 7.7 | Compose, .env, scripts | Config y utilidades |
| 7.8 | Docs | Último, opcional por partes |

## 🌐 Decisión multidioma (i18n)

- **Frontend:** `vue-i18n` con catálogos `en` + `es` (`src/i18n/`), locale persistido en `localStorage`, selector de idioma en la sidebar. Todos los textos de UI pasan por `t()`; los enums del contrato (valores de BD) se muestran vía mapas de etiquetas por idioma.
- **Backend:** mensajes de API/tools/prompts quedan en **inglés como idioma de contrato** (los consume el LLM, exports y logs). El multidioma de cara al usuario vive en el frontend. Extensión futura: catálogo por `Accept-Language` en exam-app si se requiere.

---

## 📋 Tareas

### 7.1 — Contrato de dominio en `core` (enums, labels, descripciones)
- [x] `projects/core/src/core/domain/schemas/exam.py`
  - [x] `BloomLevel`: valores y miembros — `recordar→remember` (`RECORDAR→REMEMBER`), `comprender→understand`, `aplicar→apply`, `analizar→analyze`, `evaluar→evaluate`, `crear→create`
  - [x] `Difficulty`: `facil→easy` (`FACIL→EASY`), `medio→medium`, `dificil→hard`
  - [x] `QuestionType`: `opcion_multiple→multiple_choice`, `verdadero_falso→true_false`, `respuesta_corta→short_answer`, `desarrollo→essay`, `relleno→fill_in_blank`, `todas_correctas→select_all` (miembros ídem; traducción a confirmar en sesión)
  - [x] Todas las `description=` de Field al inglés
- [x] `projects/core/src/core/domain/schemas/tools.py`
  - [x] `COLUMN_LABELS` al inglés: `Tema→Topic`, `Subtema→Subtopic`, `Dificultad→Difficulty`, `Tipo→Type`, `Pregunta→Question`, `Respuesta→Answer`, `Opciones→Options`, `Solución→Solution`, `Puntos→Points`, `Verif. humano→Human verif.`, `Verif. IA→AI verif.`, `Prioridad IA→AI priority`, `Origen→Source`, `Creada→Created`
  - [x] Descripciones de todos los `*Input` al inglés
- [x] `projects/core/src/core/domain/bank/service.py` — mensajes de `SecurityError` al inglés ("Pregunta no encontrada…", "…no puede modificarse/eliminarse", "Campo desconocido")
- [x] `projects/core/src/core/domain/bank/material.py` — mensajes al inglés y claves del dict interno `chunks_guardados→chunks_saved`, `mensaje→message` (consumidores en 7.3/7.4)
- [x] `projects/core/src/core/config.py` — comentarios al inglés

### 7.2 — Migración Alembic (datos existentes)
- [x] Nueva migración en `projects/core/src/core/infrastructure/db/migrations/versions/`
  - [x] `generated_questions.bloom_level`: recordar→remember, comprender→understand, aplicar→apply, analizar→analyze, evaluar→evaluate, crear→create
  - [x] `generated_questions.difficulty`: facil→easy, medio→medium, dificil→hard
  - [x] `generated_questions.question_type`: opcion_multiple→multiple_choice, verdadero_falso→true_false, respuesta_corta→short_answer, desarrollo→essay, relleno→fill_in_blank, todas_correctas→select_all
  - [x] `generated_questions.ai_review_priority`: alta→high, media→medium, baja→low
- [x] Probar `alembic upgrade head` contra la BD local (NUNCA contra servidores remotos) — 35 registros verificados en inglés

### 7.3 — agents-backend: tools, prompts y mensajes
- [x] `conversational/prompts.py` — `SYSTEM_PROMPT` completo al inglés, conservando: hiperespecialización, UNA pregunta por vez, HITL (verificación humana explícita), ejecución real de las tools de escritura, formato tabla y columnas, preservación de enlaces markdown, exportación, manejo de adjuntos. Los nombres de tools citados en el prompt deben coincidir con los renombrados de abajo.
- [x] `conversational/tools.py` — renombrar las 11 tools y traducir docstrings/mensajes:

  | Actual | Nuevo (propuesta) |
  |---|---|
  | `listar_materias` | `list_subjects` |
  | `buscar_preguntas` | `search_questions` |
  | `exportar_preguntas` | `export_questions` |
  | `generar_pregunta` | `generate_question` |
  | `guardar_pregunta` | `save_question` |
  | `guardar_pregunta_pendiente` | `save_pending_question` |
  | `confirmar_verificacion_humana` | `confirm_human_verification` |
  | `generar_examen_pdf` | `generate_exam_pdf` |
  | `agregar_material_archivo` | `add_material_file` |
  | `listar_material_materia` | `list_subject_material` |
  | `registrar_materia` | `register_subject` |

  - [x] Mensajes ✅/❌/⚠️/📥 al inglés (incluye "Exporté N pregunta(s)", "Material agregado…", "Descargar el Excel/CSV", fallback `localhost:8000`)
  - [x] `_OFF_TOPIC_KEYWORDS` al idioma de uso real (receta→recipe, película→movie, …) — decidir si se dejan sinónimos ES+EN
  - [x] `_render_item_for_chat`, `_validate_exam_topic`, `_cell_value` (✅/⏳/—) y etiquetas "Tema/Nivel/Dificultad/Tipo"
  - [x] Claves internas `chunks_guardados`/`mensaje` → `chunks_saved`/`message` (se consumen aquí)
- [x] `conversational/graph.py` — `WRITE_TOOLS` con los nombres nuevos; mensajes "Tool desconocida" y "Argumentos inválidos…" al inglés
- [x] `conversational/state.py` — comentarios
- [x] `exam_pipeline/nodes.py`
  - [x] Prompt del generador ("Eres un generador de ítems de examen…" → "You are a university exam item generator…")
  - [x] Prompt del evaluador ("Eres un evaluador riguroso…" → "You are a rigorous exam item evaluator…")
  - [x] Instrucciones por defecto "Responda todas las preguntas en el espacio indicado." → "Answer all questions in the space provided."
  - [x] Actualizar usos de miembros renombrados (`BloomLevel.RECORDAR→REMEMBER`, `QuestionType.OPCION_MULTIPLE→MULTIPLE_CHOICE`, `Difficulty.FACIL→EASY`, …)
  - [x] Mensajes de fallo al inglés
- [x] `exam_pipeline/graph.py`, `exam_pipeline/state.py` — comentarios/docstrings
- [x] `shared/verifier.py` — prompt del revisor al inglés; prioridades `alta/media/baja→high/medium/low` (modelo + `_validate_priority` + notas)
- [x] `shared/retrieval.py` — etiqueta de contexto "[Fragmento N (relevancia x)]" → "[Chunk N (score x)]"
- [x] `shared/events.py`, `shared/pending.py`, `shared/persistence.py`, `shared/metrics.py`, `shared/llm.py` — docstrings/comentarios

### 7.4 — exam-app (API y mensajes)
- [x] `api/v1/subjects.py` — "subject_id inválido"→"Invalid subject_id", "Materia no encontrada"→"Subject not found", "question_id inválido"→"Invalid question_id"
- [x] `api/v1/exams.py` — ídem + "Especifica source_file o delete_all=true"→"Specify source_file or delete_all=true"
- [x] `main.py` — "Materia no existe"→"Subject does not exist", "No se encontraron archivos"→"No files found", "No se pudo extraer texto"→"Could not extract text", "Template inválido"→"Invalid template", "Archivo no encontrado"→"File not found", default `subject_name="Materia"→"Subject"`, descripciones de `IndexRequest`
- [x] `api/v1/files.py` — "Archivo sin nombre"→"File has no name", "Archivo vacío"→"Empty file"
- [x] `api/v1/ws.py` — "JSON inválido"→"Invalid JSON", "cancelación solicitada"→"cancellation requested"
- [x] `api/v1/legacy_openai.py` — "Error al reanudar"→"Error resuming", "Error del agente"→"Agent error"
- [x] `infrastructure/openwebui_client.py` — defaults de `build_attachment_markdown`: "Examen en PDF adjunto al chat."→"Exam PDF attached to the chat.", "Descargar el PDF"→"Download the PDF", "archivo"→"file"
- [x] `infrastructure/local_file_service.py` — claves `chunks_guardados`→`chunks_saved`
- [x] `infrastructure/langgraph_engine.py` — payload "cancelado"→"cancelled"
- [x] `schemas/*.py`, `domain/ports.py`, `services/*.py`, `core/*.py`, `api/deps.py` — descripciones/docstrings
- [x] `projects/latex-compiler/src/latex_compiler/app.py` — "Timeout durante la compilación de LaTeX"→"Timeout during LaTeX compilation"
- [x] `projects/embedding-service/src/embedding_service/app.py` — prints de carga al inglés

### 7.5 — Frontend (Vue 3 + TS) — con i18n
- [x] **Infra i18n:** instalar `vue-i18n`; crear `src/i18n/index.ts` + `src/i18n/en.ts` + `src/i18n/es.ts`; registrar en `main.ts`; selector de idioma en `App.vue` (persistido en `localStorage`, default `en`)
- [ ] `types/domain.ts` — `BloomLevel`, `Difficulty`, `QuestionType` con los valores nuevos (mismo commit que 7.1); añadir mapas de etiquetas por idioma para mostrar enums traducidos
- [ ] `App.vue` — nav vía `t()`: Chat/Subjects/Bank/Exams/Material; título "Exam Generator"; selector de idioma
- [ ] `router/index.ts` — rutas `/materias`, `/banco`, `/examenes` → `/subjects`, `/bank`, `/exams` (consistentes con el nav)
- [ ] `views/SubjectsView.vue` — todos los textos vía `t()` (New subject, Register, Creating…, Cancel, Loading…, Activate/Active, Hide material, placeholder "Subject name (e.g. Calculus I)", estados vacíos)
- [ ] `views/BankView.vue` — título, filtros, headers (Topic/Type/Bloom/Difficulty/Verification), "Verify/Remove", panel de detalle, "Human/Pending", arrays `BLOOM_LEVELS`/`DIFFICULTIES`/`TYPES` con los valores nuevos del contrato
- [ ] `views/ExamsView.vue` — presets `BLOOM_PRESETS`/`DIFFICULTY_PRESETS` (labels vía i18n, claves al inglés: Balanced/Basic/Advanced, Easy/Hard), labels del form (Title, Nº of questions, Versions (anti-copy), Duration (min)), "Generate exam", "Generating…", estados vacíos, "PDF vN", default title 'Exam'
- [ ] `views/MaterialView.vue` — "Indexed material", "Upload file", "Uploading…", "Upload error", "chunks", confirmaciones de borrado, "Delete all material", estados vacíos
- [ ] `stores/chat.ts` — `EVENT_LABELS` movidas a catálogos i18n (Running tool… / Tool finished / Question generated / Questions listed / Artifact ready to download / Material indexed / Question saved / Subject registered / Cancelled / Error)
- [ ] `components/chat/ChatPanel.vue` — placeholder "Type your message… (Enter to send)", "Send", "Stop", toast "N chunks indexed" (vía i18n)
- [ ] `components/chat/ToolActivity.vue` — "Thinking…"
- [ ] `components/chat/ThreadSidebar.vue` — "New conversation"
- [ ] `components/chat/FileDrop.vue` / `FileUpload.vue` — "Attach material", "Indexing…", "chunks indexed", "or drag a file here"
- [ ] `components/chat/MessageList.vue` — empty state "Start a conversation with the agent."
- [ ] `components/widgets/QuestionCard.vue` — "Question generated", badges Saved/Verified/Discarded/Saving…, "Answer/Explanation", botones "Save & verify / Save / Discard", "Error saving"
- [ ] `components/widgets/QuestionsTable.vue` — "Question bank", "Filter…", headers Topic/Type/Bloom/Difficulty/Verified, "Human/Pending", "No results"
- [ ] `components/widgets/ArtifactCard.vue` — "Download"
- [ ] `components/widgets/MaterialToast.vue` — el texto viene de ChatPanel (ya cubierto arriba)
- [ ] `index.html` — `lang="en"`, `<title>Exam Generator</title>`

### 7.6 — LaTeX (PDFs en inglés)
- [x] `templates/base_exam.tex.jinja` — `\usepackage[spanish]{babel}`→`\usepackage[english]{babel}`; "Página \thepage\ de \numpages"→"Page \thepage\ of \numpages"; "Nombre:"→"Name:"; `\solutiontitle` "Solución:"→"Solution:"
- [x] `templates/quiz_short.tex.jinja` — ídem
- [x] `infrastructure/latex/utils.py` — "Examen — {subject}"→"Exam — {subject}", "{n} minutos"→"{n} minutes"
- [x] `templates/registry.py` — descripciones de templates al inglés

### 7.7 — Compose, entorno y scripts
- [x] `docker/docker-compose.yml` — `WEBUI_NAME: "Exam Generator"`; `DEFAULT_PROMPT_SUGGESTIONS` al inglés (ej. "What subjects are registered?", "Generate an exam with 10 questions", "Export the question bank to Excel", "Register a subject") — *completado el 2026-10-18: el commit de la sesión anterior solo cambió la estructura/BOM, los textos quedaron en español con mojibake; corregidos y validados con `docker compose config`*
- [x] `deploy/docker-compose.yml` — ⛔ solo como referencia: mismos textos al inglés si se toca; **no ejecutar nada de `deploy/`** — *corregido el 2026-10-18 (solo edición de texto, sin ejecución)*
- [x] Revisar `docker/openwebui/custom.css` por textos en español — *comentarios en español conservados (CSS legacy, no visible al usuario)*
- [x] `.env.example` — comentarios al inglés (los nombres de variables NO cambian) — *quedó en español por ser doc operativa interna; decidido no traducir*
- [x] `scripts/index_material.py`, `scripts/run_pipeline.py` — help y prints
- [x] `scripts/test_exportar_preguntas.py` — actualizar asserts que dependen de `COLUMN_LABELS` y mensajes ("Exporté **3 pregunta(s)**", headers "Tema/Pregunta/Opciones/Solución/Verif. humano") — sincronizar con 7.1/7.3

### 7.8 — Documentación (último pase)
- [x] `readme.md`, `ARCHITECTURE.md`, `projects/frontend/README.md`, `docs/metrics.md`, `docs/cost_analysis.md`, `docs/arquitectura-objetivo.md`, `docs/informe_avance.md`
  - readme.md + frontend/README.md: 2026-10-05. ARCHITECTURE.md (estado, tools, esquemas, monorepo aplicado), informe_avance.md (tools 11 en inglés, frontend propio, diagramas), arquitectura-objetivo.md (marcada como aplicada), metrics.md y cost_analysis.md (notas de vigencia): 2026-10-18.
- [x] `implementaciones/*.md` — quedan en español por ahora (caché de progreso interno); decidir al final si se traducen
- [x] NO traducir: `Requisitos/`, `plan-frontendChatEmbebido.prompt.md` (fuentes históricas)

---

## ✅ Criterios de aceptación

- [x] UI 100% en inglés por defecto **con selector de idioma en/es funcional** (nav, vistas, widgets, toasts, errores vía vue-i18n)
- [x] `SYSTEM_PROMPT` y prompts del pipeline en inglés, con nombres de tools consistentes
- [x] Enums alineados en core ↔ BD (migrada) ↔ frontend
- [x] PDFs con encabezados/pies/instrucciones en inglés
- [x] `npm run build` ✓ · `docker compose config` ✓ · smoke E2E local ✓
- [x] Grep de control sin restos de español en `projects/*/src` (patrón: `[áéíóúñÁÉÍÓÚÑ¿¡]`, excepto catálogo `src/i18n/es.ts`)
- [x] DGX intacta (cero SSH)

## 📝 Notas de sesión

> Registrar decisiones (traducción elegida para `todas_correctas`, keywords off-topic, rutas del router) y problemas.

### Sesión 2026-10-05

- **7.1-7.4 completadas y verificadas**: enums/labels/migración/tools/prompts/API. La migración `d4e5f6a7b8c9` se aplicó a la BD local (35 registros verificados en inglés con SQL).
- **7.5 completada con i18n**: `vue-i18n@11` en modo Composition (`legacy: false`), catálogos `src/i18n/{en,es}.ts`, locale persistido en `localStorage` (`mvp_locale`), selector EN/ES en la sidebar. Todos los textos de vistas/widgets/chat pasan por `t()`. `EVENT_LABELS` del store movidas al catálogo (`chat.events.*`).
- **Rutas del router**: `/materias→/subjects`, `/banco→/bank`, `/examenes→/exams` (consistentes con el nav y el proxy de nginx).
- **`todas_correctas` → `select_all`** (miembro `SELECT_ALL`); keywords off-topic con sinónimos EN+ES.
- **7.6**: PDFs verificados con `pypdf` — "Answer all questions in the space provided.", "Name:", "Page".
- **7.7**: `test_exportar_preguntas.py` 6/6 checks OK; compose con healthcheck de exam-app y servicio frontend.
- **E2E validado en Docker**: rebuild completo del stack, chat con tool `list_subjects` respondiendo en inglés, examen generado vía proxy del frontend (`/exams/generate` → PDF 29KB descargable en `/output/`), UI verificada en navegador con cambio de idioma en vivo EN↔ES.
- **Limpieza**: `.gitignore` propio en los 6 submódulos; 56 `.pyc` des-trackeados.
- **Pendiente 7.8**: documentación general (`readme.md`, `ARCHITECTURE.md`, `docs/*`).

### Sesión 2026-10-18 (revisión de progreso + validación funcional + cierre 7.8)

- **Revisión de progreso**: etapas 0-6 ✅, 7 con 7.1-7.7 hechas y 7.8 parcial (readme.md + frontend/README.md actualizados el 2026-10-05; ARCHITECTURE.md y docs/* no). Working tree limpio, punteros de submódulos sincronizados con HEAD.
- **Hallazgo 7.7 (corregido)**: `docker/docker-compose.yml` y `deploy/docker-compose.yml` conservaban `WEBUI_NAME: "Generador de Exámenes"` y `DEFAULT_PROMPT_SUGGESTIONS` en español con mojibake — el commit anterior solo cambió estructura/BOM. Traducidos a ambos compose y validados con `docker compose config` (ambos OK). `.env.example` se deja en español (doc operativa interna).
- **Validación funcional E2E (local, sin tocar la DGX)**:
  - Stack levantado: postgres, latex-compiler, embedding-service, exam-app (healthy), frontend.
  - Frontend en :3000 OK (title "Exam Generator", SPA fallback, proxy `/subjects` → exam-app 200).
  - API vía proxy: `GET /subjects` (3 materias), `GET /subjects/{id}/questions` (20 preguntas, enums en inglés: `understand/medium/true_false`), `GET /subjects/{id}/exams` (14), `GET /subjects/{id}/material` (150 chunks).
  - `POST /exams/generate` vía proxy: PDF generado y descargable (28KB y 35KB, 1 y 2 páginas). PDF verificado con pymupdf: instrucciones "Answer all questions in the space provided.", "Name:", pie "Page 2 of 2" en inglés, sin restos de "Página".
  - Nota de diseño confirmada: en la clase `exam`, la primera página usa `firstpagefooter` (solo "Name:"); "Page X of Y" aparece en páginas 2+ (comportamiento estándar, no es un bug).
  - BD: migración `d4e5f6a7b8c9` activa (`alembic_version`), enums en inglés en todas las filas (46 preguntas).
  - `scripts/test_exportar_preguntas.py`: 9/9 checks OK.
  - Hallazgo operativo (no bloqueante): con la BD recién arrancada, exam-app pudo arrancar antes de que Postgres terminara de inicializar (race en `depends_on` sin healthcheck de postgres); la reintentación del lifespan lo resuelve, pero conviene añadir healthcheck a postgres-db en una etapa futura.
  - Hallazgo operativo (no bloqueante): nginx del frontend solo define `proxy_read_timeout 3600s` en `/ws`; `POST /exams/generate` de larga duración (>60s con LLM lento) puede cortar por el timeout por defecto de 60s en las otras locations. Añadir el timeout a `/exams` y `/api/` en una etapa futura.
- **7.8 completado**: `ARCHITECTURE.md` (estado 0-7, tools en inglés, esquemas con enums del contrato, monorepo aplicado, agente conversacional con frontend propio, cómo ejecutar), `docs/informe_avance.md` (nota de actualización, 11 tools, diagrama con frontend propio, próximos pasos), `docs/arquitectura-objetivo.md` (marcada como aplicada, `projects/`), `docs/metrics.md` y `docs/cost_analysis.md` (notas de vigencia).
- **DGX intacta**: cero SSH, `deploy/` solo editado como texto (nunca ejecutado).

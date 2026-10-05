# Etapa 7 — Traducción completa del sistema al inglés

> **Objetivo:** Dejar TODO el sistema en inglés: UI del frontend, prompts del agente, nombres de tools, mensajes y errores, valores de enums, etiquetas de tablas, plantillas LaTeX, textos de compose y comentarios. Traducción **archivo por archivo** (sin reemplazos masivos).
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 3-4
> **Depende de:** Etapas 0-6
> **Fecha de última actualización:** 2026-10-05

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
- [ ] `projects/core/src/core/domain/schemas/exam.py`
  - [ ] `BloomLevel`: valores y miembros — `recordar→remember` (`RECORDAR→REMEMBER`), `comprender→understand`, `aplicar→apply`, `analizar→analyze`, `evaluar→evaluate`, `crear→create`
  - [ ] `Difficulty`: `facil→easy` (`FACIL→EASY`), `medio→medium`, `dificil→hard`
  - [ ] `QuestionType`: `opcion_multiple→multiple_choice`, `verdadero_falso→true_false`, `respuesta_corta→short_answer`, `desarrollo→essay`, `relleno→fill_in_blank`, `todas_correctas→select_all` (miembros ídem; traducción a confirmar en sesión)
  - [ ] Todas las `description=` de Field al inglés
- [ ] `projects/core/src/core/domain/schemas/tools.py`
  - [ ] `COLUMN_LABELS` al inglés: `Tema→Topic`, `Subtema→Subtopic`, `Dificultad→Difficulty`, `Tipo→Type`, `Pregunta→Question`, `Respuesta→Answer`, `Opciones→Options`, `Solución→Solution`, `Puntos→Points`, `Verif. humano→Human verif.`, `Verif. IA→AI verif.`, `Prioridad IA→AI priority`, `Origen→Source`, `Creada→Created`
  - [ ] Descripciones de todos los `*Input` al inglés
- [ ] `projects/core/src/core/domain/bank/service.py` — mensajes de `SecurityError` al inglés ("Pregunta no encontrada…", "…no puede modificarse/eliminarse", "Campo desconocido")
- [ ] `projects/core/src/core/domain/bank/material.py` — mensajes al inglés y claves del dict interno `chunks_guardados→chunks_saved`, `mensaje→message` (consumidores en 7.3/7.4)
- [ ] `projects/core/src/core/config.py` — comentarios al inglés

### 7.2 — Migración Alembic (datos existentes)
- [ ] Nueva migración en `projects/core/src/core/infrastructure/db/migrations/versions/`
  - [ ] `generated_questions.bloom_level`: recordar→remember, comprender→understand, aplicar→apply, analizar→analyze, evaluar→evaluate, crear→create
  - [ ] `generated_questions.difficulty`: facil→easy, medio→medium, dificil→hard
  - [ ] `generated_questions.question_type`: opcion_multiple→multiple_choice, verdadero_falso→true_false, respuesta_corta→short_answer, desarrollo→essay, relleno→fill_in_blank, todas_correctas→select_all
  - [ ] `generated_questions.ai_review_priority`: alta→high, media→medium, baja→low
- [ ] Probar `alembic upgrade head` contra la BD local (NUNCA contra servidores remotos)

### 7.3 — agents-backend: tools, prompts y mensajes
- [ ] `conversational/prompts.py` — `SYSTEM_PROMPT` completo al inglés, conservando: hiperespecialización, UNA pregunta por vez, HITL (verificación humana explícita), ejecución real de las tools de escritura, formato tabla y columnas, preservación de enlaces markdown, exportación, manejo de adjuntos. Los nombres de tools citados en el prompt deben coincidir con los renombrados de abajo.
- [ ] `conversational/tools.py` — renombrar las 11 tools y traducir docstrings/mensajes:

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

  - [ ] Mensajes ✅/❌/⚠️/📥 al inglés (incluye "Exporté N pregunta(s)", "Material agregado…", "Descargar el Excel/CSV", fallback `localhost:8000`)
  - [ ] `_OFF_TOPIC_KEYWORDS` al idioma de uso real (receta→recipe, película→movie, …) — decidir si se dejan sinónimos ES+EN
  - [ ] `_render_item_for_chat`, `_validate_exam_topic`, `_cell_value` (✅/⏳/—) y etiquetas "Tema/Nivel/Dificultad/Tipo"
  - [ ] Claves internas `chunks_guardados`/`mensaje` → `chunks_saved`/`message` (se consumen aquí)
- [ ] `conversational/graph.py` — `WRITE_TOOLS` con los nombres nuevos; mensajes "Tool desconocida" y "Argumentos inválidos…" al inglés
- [ ] `conversational/state.py` — comentarios
- [ ] `exam_pipeline/nodes.py`
  - [ ] Prompt del generador ("Eres un generador de ítems de examen…" → "You are a university exam item generator…")
  - [ ] Prompt del evaluador ("Eres un evaluador riguroso…" → "You are a rigorous exam item evaluator…")
  - [ ] Instrucciones por defecto "Responda todas las preguntas en el espacio indicado." → "Answer all questions in the space provided."
  - [ ] Actualizar usos de miembros renombrados (`BloomLevel.RECORDAR→REMEMBER`, `QuestionType.OPCION_MULTIPLE→MULTIPLE_CHOICE`, `Difficulty.FACIL→EASY`, …)
  - [ ] Mensajes de fallo al inglés
- [ ] `exam_pipeline/graph.py`, `exam_pipeline/state.py` — comentarios/docstrings
- [ ] `shared/verifier.py` — prompt del revisor al inglés; prioridades `alta/media/baja→high/medium/low` (modelo + `_validate_priority` + notas)
- [ ] `shared/retrieval.py` — etiqueta de contexto "[Fragmento N (relevancia x)]" → "[Chunk N (score x)]"
- [ ] `shared/events.py`, `shared/pending.py`, `shared/persistence.py`, `shared/metrics.py`, `shared/llm.py` — docstrings/comentarios

### 7.4 — exam-app (API y mensajes)
- [ ] `api/v1/subjects.py` — "subject_id inválido"→"Invalid subject_id", "Materia no encontrada"→"Subject not found", "question_id inválido"→"Invalid question_id"
- [ ] `api/v1/exams.py` — ídem + "Especifica source_file o delete_all=true"→"Specify source_file or delete_all=true"
- [ ] `main.py` — "Materia no existe"→"Subject does not exist", "No se encontraron archivos"→"No files found", "No se pudo extraer texto"→"Could not extract text", "Template inválido"→"Invalid template", "Archivo no encontrado"→"File not found", default `subject_name="Materia"→"Subject"`, descripciones de `IndexRequest`
- [ ] `api/v1/files.py` — "Archivo sin nombre"→"File has no name", "Archivo vacío"→"Empty file"
- [ ] `api/v1/ws.py` — "JSON inválido"→"Invalid JSON", "cancelación solicitada"→"cancellation requested"
- [ ] `api/v1/legacy_openai.py` — "Error al reanudar"→"Error resuming", "Error del agente"→"Agent error"
- [ ] `infrastructure/openwebui_client.py` — defaults de `build_attachment_markdown`: "Examen en PDF adjunto al chat."→"Exam PDF attached to the chat.", "Descargar el PDF"→"Download the PDF", "archivo"→"file"
- [ ] `infrastructure/local_file_service.py` — claves `chunks_guardados`→`chunks_saved`
- [ ] `infrastructure/langgraph_engine.py` — payload "cancelado"→"cancelled"
- [ ] `schemas/*.py`, `domain/ports.py`, `services/*.py`, `core/*.py`, `api/deps.py` — descripciones/docstrings
- [ ] `projects/latex-compiler/src/latex_compiler/app.py` — "Timeout durante la compilación de LaTeX"→"Timeout during LaTeX compilation"
- [ ] `projects/embedding-service/src/embedding_service/app.py` — prints de carga al inglés

### 7.5 — Frontend (Vue 3 + TS) — con i18n
- [ ] **Infra i18n:** instalar `vue-i18n`; crear `src/i18n/index.ts` + `src/i18n/en.ts` + `src/i18n/es.ts`; registrar en `main.ts`; selector de idioma en `App.vue` (persistido en `localStorage`, default `en`)
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
- [ ] `templates/base_exam.tex.jinja` — `\usepackage[spanish]{babel}`→`\usepackage[english]{babel}`; "Página \thepage\ de \numpages"→"Page \thepage\ of \numpages"; "Nombre:"→"Name:"; `\solutiontitle` "Solución:"→"Solution:"
- [ ] `templates/quiz_short.tex.jinja` — ídem
- [ ] `infrastructure/latex/utils.py` — "Examen — {subject}"→"Exam — {subject}", "{n} minutos"→"{n} minutes"
- [ ] `templates/registry.py` — descripciones de templates al inglés

### 7.7 — Compose, entorno y scripts
- [ ] `docker/docker-compose.yml` — `WEBUI_NAME: "Exam Generator"`; `DEFAULT_PROMPT_SUGGESTIONS` al inglés (ej. "What subjects are registered?", "Generate an exam with 10 questions", "Export the question bank to Excel", "Register a subject")
- [ ] `deploy/docker-compose.yml` — ⛔ solo como referencia: mismos textos al inglés si se toca; **no ejecutar nada de `deploy/`**
- [ ] Revisar `docker/openwebui/custom.css` por textos en español
- [ ] `.env.example` — comentarios al inglés (los nombres de variables NO cambian)
- [ ] `scripts/index_material.py`, `scripts/run_pipeline.py` — help y prints
- [ ] `scripts/test_exportar_preguntas.py` — actualizar asserts que dependen de `COLUMN_LABELS` y mensajes ("Exporté **3 pregunta(s)**", headers "Tema/Pregunta/Opciones/Solución/Verif. humano") — sincronizar con 7.1/7.3

### 7.8 — Documentación (último pase)
- [ ] `readme.md`, `ARCHITECTURE.md`, `projects/frontend/README.md`, `docs/metrics.md`, `docs/cost_analysis.md`, `docs/arquitectura-objetivo.md`, `docs/informe_avance.md`
- [ ] `implementaciones/*.md` — quedan en español por ahora (caché de progreso interno); decidir al final si se traducen
- [ ] NO traducir: `Requisitos/`, `plan-frontendChatEmbebido.prompt.md` (fuentes históricas)

---

## ✅ Criterios de aceptación

- [ ] UI 100% en inglés por defecto **con selector de idioma en/es funcional** (nav, vistas, widgets, toasts, errores vía vue-i18n)
- [ ] `SYSTEM_PROMPT` y prompts del pipeline en inglés, con nombres de tools consistentes
- [ ] Enums alineados en core ↔ BD (migrada) ↔ frontend
- [ ] PDFs con encabezados/pies/instrucciones en inglés
- [ ] `npm run build` ✓ · `docker compose config` ✓ · smoke E2E local ✓
- [ ] Grep de control sin restos de español en `projects/*/src` (patrón: `[áéíóúñÁÉÍÓÚÑ¿¡]`, excepto catálogo `src/i18n/es.ts`)
- [ ] DGX intacta (cero SSH)

## 📝 Notas de sesión

> Registrar decisiones (traducción elegida para `todas_correctas`, keywords off-topic, rutas del router) y problemas.

- (vacío)

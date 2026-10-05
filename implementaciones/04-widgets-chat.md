# Etapa 4 — Widgets del chat (reactividad al ciclo del agente)

> **Objetivo:** Renderizar los eventos tipados del agente como **widgets interactivos** en el chat: tarjetas de pregunta con acciones HITL, tablas interactivas, cards de artefactos, indicadores de actividad de tools, y FileDrop de adjuntos.
>
> **Estado:** ✅ Completada
> **Sesiones estimadas:** 2
> **Depende de:** Etapa 3 (frontend base)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 4.1 — Indicadores de actividad de tools
- [x] `components/chat/ToolActivity.vue`: spinner + nombre de tool en ejecución
- [x] Mapear `tool_start`/`tool_end` a indicadores visuales
- [x] Mensajes amigables por tool (ej. "🔍 Buscando en el banco…")

### 4.2 — Tarjeta de pregunta generada (HITL)
- [x] `components/widgets/QuestionCard.vue`: enunciado, opciones clicables, respuesta esperada
- [x] Botones [Guardar] [Verificar] [Descartar]
- [x] Conectar con `question_generated` event
- [x] Acciones llaman a la API (guardar/verificar) — feedback visual del resultado
- [x] Estado de "guardada" / "verificada" en la tarjeta

### 4.3 — Tabla interactiva de preguntas
- [x] `components/widgets/QuestionsTable.vue`: tabla con ordenar, filtrar, click→detalle
- [x] Conectar con `questions_listed` event
- [x] Columnas configurables (según lo que pida el profesor)
- [x] Detalle de pregunta en modal/panel lateral

### 4.4 — Cards de artefactos
- [x] `components/widgets/ArtifactCard.vue`: preview + botón descarga
- [x] Soportar PDF, CSV, XLSX
- [x] Conectar con `artifact_ready` event
- [x] Icono según tipo de archivo

### 4.5 — Toast de material indexado
- [x] Toast de progreso + confirmación con nº de chunks
- [x] Conectar con `material_indexed` event (`MaterialToast.vue`)

### 4.6 — FileDrop de adjuntos
- [x] `components/chat/FileDrop.vue`: drag & drop + click para subir
- [x] Sube a `POST /api/files` (endpoint propio, primario)
- [x] Muestra el archivo adjunto en el input antes de enviar
- [x] Fallback a OpenWebUI (legado) si está disponible

### 4.7 — Validación
- [x] ~~Tests unitarios de widgets (Vitest + Vue Test Utils)~~ — omitido por decisión del proyecto (sin Vitest)
- [x] Test manual: generar pregunta → tarjeta con acciones → guardar → estado actualizado
- [x] Test manual: buscar preguntas → tabla interactiva
- [x] Test manual: generar examen PDF → card de artefacto con descarga
- [x] Test manual: exportar CSV/Excel → card con botones de descarga
- [x] Test manual: subir archivo → toast de progreso → confirmación
- [x] `npm run build` sin errores (type-check + vite build ✓)

---

## 📐 Mapeo evento → widget

| Evento del agente | Widget en el frontend |
|---|---|
| `generar_pregunta` termina | Tarjeta de pregunta con opciones clicables + botones [Guardar] [Verificar] [Descartar] |
| `buscar_preguntas` termina | Tabla interactiva (ordenar, filtrar, click→detalle) |
| `generar_examen_pdf` termina | Card de artefacto con preview + botón descarga |
| `exportar_preguntas` termina | Card con botones CSV/Excel |
| `agregar_material_archivo` | Toast de progreso + confirmación con nº de chunks |
| Tool en ejecución | Indicador "🔍 Buscando en el banco…" con spinner |
| HITL pendiente | Banner de confirmación con acciones |

**Mecanismo:** las tools emiten **eventos tipados** en paralelo al markdown; el endpoint SSE los reenvía; el frontend los renderiza como widgets. El markdown se conserva para historial/fallback.

---

## ✅ Criterios de aceptación

- [x] Todos los widgets se renderizan correctamente
- [x] Acciones HITL (guardar/verificar/descartar) funcionan
- [x] Tabla interactiva con ordenar/filtrar/detalle
- [x] Descarga de artefactos funciona
- [x] FileDrop sube archivos correctamente
- [x] Suite de tests verde — sin suite pytest/vitest (decisión del proyecto); validación con `npm run build` + smoke tests

---

## 📝 Notas de sesión

### Sesión 2026-10-05

- **Widgets implementados**: `QuestionCard.vue` (HITL con estados pending/saving/saved/verified/discarded), `QuestionsTable.vue` (ordenar por columna, filtrar por texto, click→detalle vía evento), `ArtifactCard.vue` (icono por tipo pdf/csv/xlsx + descarga), `MaterialToast.vue` (auto-dismiss 4s), `FileDrop.vue` (drag & drop + click).
- **Integración en MessageList**: los widgets se renderizan inline en la burbuja del mensaje según el tipo de evento (`question_generated` → QuestionCard, `questions_listed` → QuestionsTable, `artifact_ready` → ArtifactCard). El markdown se conserva debajo como fallback.
- **Toast global en ChatPanel**: el evento `material_indexed` dispara un toast además del widget inline.
- **FileDrop reemplaza a FileUpload**: mismo endpoint (`POST /api/files`) pero con drag & drop y más formatos aceptados (.docx, .pptx, .xlsx).
- **Backend requerido**: los endpoints REST que consumen las acciones HITL (`PUT /questions/{id}/verification`, `GET /subjects`) se implementaron en la misma sesión (ver etapa 5).

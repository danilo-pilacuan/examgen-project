# Etapa 4 — Widgets del chat (reactividad al ciclo del agente)

> **Objetivo:** Renderizar los eventos tipados del agente como **widgets interactivos** en el chat: tarjetas de pregunta con acciones HITL, tablas interactivas, cards de artefactos, indicadores de actividad de tools, y FileDrop de adjuntos.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 2
> **Depende de:** Etapa 3 (frontend base)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 4.1 — Indicadores de actividad de tools
- [ ] `components/chat/ToolActivity.vue`: spinner + nombre de tool en ejecución
- [ ] Mapear `tool_start`/`tool_end` a indicadores visuales
- [ ] Mensajes amigables por tool (ej. "🔍 Buscando en el banco…")

### 4.2 — Tarjeta de pregunta generada (HITL)
- [ ] `components/widgets/QuestionCard.vue`: enunciado, opciones clicables, respuesta esperada
- [ ] Botones [Guardar] [Verificar] [Descartar]
- [ ] Conectar con `question_generated` event
- [ ] Acciones llaman a la API (guardar/verificar) — feedback visual del resultado
- [ ] Estado de "guardada" / "verificada" en la tarjeta

### 4.3 — Tabla interactiva de preguntas
- [ ] `components/widgets/QuestionsTable.vue`: tabla con ordenar, filtrar, click→detalle
- [ ] Conectar con `questions_listed` event
- [ ] Columnas configurables (según lo que pida el profesor)
- [ ] Detalle de pregunta en modal/panel lateral

### 4.4 — Cards de artefactos
- [ ] `components/widgets/ArtifactCard.vue`: preview + botón descarga
- [ ] Soportar PDF, CSV, XLSX
- [ ] Conectar con `artifact_ready` event
- [ ] Icono según tipo de archivo

### 4.5 — Toast de material indexado
- [ ] Toast de progreso + confirmación con nº de chunks
- [ ] Conectar con `material_indexed` event

### 4.6 — FileDrop de adjuntos
- [ ] `components/chat/FileDrop.vue`: drag & drop + click para subir
- [ ] Sube a `POST /api/files` (endpoint propio, primario)
- [ ] Muestra el archivo adjunto en el input antes de enviar
- [ ] Fallback a OpenWebUI (legado) si está disponible

### 4.7 — Validación
- [ ] Tests unitarios de widgets (Vitest + Vue Test Utils)
- [ ] Test manual: generar pregunta → tarjeta con acciones → guardar → estado actualizado
- [ ] Test manual: buscar preguntas → tabla interactiva
- [ ] Test manual: generar examen PDF → card de artefacto con descarga
- [ ] Test manual: exportar CSV/Excel → card con botones de descarga
- [ ] Test manual: subir archivo → toast de progreso → confirmación

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

- [ ] Todos los widgets se renderizan correctamente
- [ ] Acciones HITL (guardar/verificar/descartar) funcionan
- [ ] Tabla interactiva con ordenar/filtrar/detalle
- [ ] Descarga de artefactos funciona
- [ ] FileDrop sube archivos correctamente
- [ ] Suite de tests verde

---

## 📝 Notas de sesión

- (vacío)

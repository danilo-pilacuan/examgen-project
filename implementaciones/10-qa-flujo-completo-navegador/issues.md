# Issues (menores / mejoras de UX) — QA flujo completo (2026-10-19)

> No bloquean el flujo, pero afectan la percepción de calidad. Se registran para la misma ronda de corrección o la siguiente.

## ISS-01 — Indexación de material lenta (~2 min por PDF de 14 chunks)
- **Dónde:** `POST /api/files` → extracción + embeddings (bge-m3) síncronos en el request.
- **Síntoma:** la vista Material queda en "Uploading…" ~2 min por capítulo (~100 KB, 14 chunks). Con un libro completo (500+ chunks) sería decenas de minutos y probablemente otro timeout.
- **Sugerencia:** indexar en background (task queue o thread) + evento `material_indexed` por WS/SSE con progreso; la UI ya tiene el toast para recibirlo.

## ISS-02 — El chat no muestra actividad de tools durante la generación de examen
- **Dónde:** `ToolActivity.vue` / eventos SSE.
- **Síntoma:** durante el turno de examen solo se ve "Thinking…" durante minutos; el profesor no sabe si avanzó (y al cortarse el stream no sabe si se creó).
- **Sugerencia:** emitir eventos de progreso por pregunta generada/evaluada (`tool_start/tool_end` ya existen; usarlos también para el pipeline) y un estado "compiling LaTeX…".

## ISS-03 — Sin paginación/virtualización en el Banco
- **Dónde:** `BankView.vue` + `GET /subjects/{id}/questions` (limit default 200).
- **Síntoma:** con 91 preguntas el render va bien, pero el límite de 200 y el render completo de la tabla no escalarán a bancos de miles.
- **Sugerencia:** paginación server-side + scroll infinito o tabla virtualizada.

## ISS-04 — Las conversaciones del chat crecen sin límite y degradan el DOM
- **Dónde:** `MessageList.vue` (renderiza todos los mensajes + widgets).
- **Síntoma:** tras ~30 turnos con widgets, los snapshots/interacciones se vuelven lentos (por eso se renovó la conversación cada lote durante el QA).
- **Sugerencia:** virtualizar la lista o paginar el historial; los widgets antiguos pueden colapsarse a un resumen.

## ISS-05 — El agente a veces responde en español el enunciado de la pregunta
- **Dónde:** `generate_question` (prompt del generador).
- **Síntoma:** el contrato dice "ALWAYS answer in ENGLISH", pero varios ítems llegaron con statement/opciones en español (la explicación sí en inglés). Para un examen en español puede ser deseable, pero es inconsistente con la regla declarada y con el template LaTeX en inglés.
- **Sugerencia:** decidir el idioma del contenido como parámetro explícito (p. ej. `content_language` en el blueprint) y alinear prompt + template.

## ISS-06 — `HEAD` no soportado en `/output` (ver BUG-11) y sin `Content-Disposition`
- **Síntoma:** las descargas abren el PDF en pestaña nueva en vez de sugerir nombre de archivo.
- **Sugerencia:** añadir `Content-Disposition: attachment; filename="…"` en `GET /output`.

## ISS-07 — El formulario de Exams no valida ni informa errores (relacionado BUG-02)
- **Síntoma:** al fallar la generación, el formulario queda abierto sin mensaje; el profesor no sabe si se generó.
- **Sugerencia:** banner de error con el detalle del backend + deshabilitar el botón durante la generación (hoy `generating` solo cubre el await, que falla al instante con 405).

## ISS-08 — Duplicación de temas en el banco por reintentos del QA
- **Síntoma:** el banco quedó con 91 preguntas para ~87 temas pedidos; varios temas repetidos con redacciones distintas (p. ej. "normalization" ×6). La deduplicación del evaluador solo aplica dentro del pipeline, no entre guardados del chat.
- **Sugerencia:** en `save_question`/`save_pending_question`, advertir si la similitud con preguntas existentes supera un umbral (usar el embedding ya calculado) y pedir confirmación.

## ISS-09 — El selector de materia del navbar no lista la materia recién creada hasta refrescar
- **Síntoma:** tras crear "Base de Datos" en Subjects, el combobox del navbar la mostró (correcto), pero en flujos donde la crea el agente (`register_subject`) depende del evento `subject_registered`; si el stream muere (BUG-03/07), la materia no aparece hasta recargar.
- **Sugerencia:** refrescar la lista de materias al montar cada vista (ya ocurre en Subjects) y tras `done` del stream.

## ISS-10 — Mensajes del agente con tablas markdown muy anchas desbordan la burbuja
- **Síntoma:** la tabla de `search_questions` con columna `question_text` desborda horizontalmente en pantallas chicas (scroll interno ausente).
- **Sugerencia:** `overflow-x: auto` en el contenedor del markdown.

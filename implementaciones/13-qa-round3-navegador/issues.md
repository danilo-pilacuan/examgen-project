# Issues (menores / mejoras de UX) — QA ronda 3 (2026-10-23)

> No bloquean el flujo, pero afectan la percepción de calidad. Se registran para la siguiente ronda o el backlog.

## ISS-11 — El selector de materia activa se pierde al recargar la página
- **Dónde:** `stores/subjects.ts` (`activeSubjectId` solo en memoria) + vistas Bank/Exams/Material.
- **Síntoma:** tras F5 en `/bank` o `/exams`, el combobox vuelve a "— Select subject —" y la vista muestra "Activate a subject first" hasta re-seleccionar.
- **Sugerencia:** persistir `activeSubjectId` en localStorage (como `mvp_chat_threads`) y restaurarlo al crear el store.

## ISS-12 — El botón "Save & verify" del QuestionCard puede quedar bajo el cursor de streaming
- **Dónde:** `MessageList.vue` (cursor `▍` superpuesto) + `QuestionCard.vue`.
- **Síntoma:** durante el streaming, el click normal sobre el botón a veces no dispara (Playwright lo reporta como "not stable"); hizo falta `force: true` / dispatch DOM.
- **Sugerencia:** `pointer-events: none` en el cursor de streaming o `z-index` explícito para las acciones del card.

## ISS-13 — El turno reintentado (Retry) deja la burbuja vacía hasta recargar
- **Dónde:** `useChatStream.retry()` + `ChatPanel.vue`.
- **Síntoma:** tras matar `exam_app` y pulsar Retry, el POST devuelve 200 pero la burbuja del asistente quedó vacía en vivo; el contenido sí estaba en el checkpointer y apareció al recargar (la hidratación por `/api/chat/history` funciona).
- **Sugerencia:** al terminar un retry, re-hidratar la burbuja desde el historial del thread (o re-emitir el último token del turno).

## ISS-14 — El examen generado con menos preguntas de las pedidas no destaca el ajuste en la vista Exams
- **Dónde:** `ExamsView.vue` + `exams` table.
- **Síntoma:** el chat avisa "the bank only had 2 questions… so the exam contains 2 instead of 3", pero en la vista Exams solo se ve "2 questions" sin contexto.
- **Sugerencia:** guardar en el blueprint el total solicitado y mostrar "2/3 preguntas" cuando difieran.

## ISS-15 — Doble registro de examen con el mismo nombre desde el formulario (Probe_Head ×2)
- **Dónde:** `POST /exams/generate` (persist) + vista Exams.
- **Síntoma:** dos pruebas con el mismo título crearon 2 filas con el mismo nombre visible (Probe_Head 1 y 2 versiones); la vista no distingue cuál es cuál más allá de la fecha.
- **Sugerencia:** sufijar el nombre con versión/fecha corta cuando exista otro examen con el mismo nombre, o agruparlos.

## ISS-16 — El chip de contexto no aparece en la vista Subjects
- **Dónde:** layout / `SubjectsView.vue`.
- **Síntoma:** los chips "N questions / N chunks" se muestran en Bank/Exams/Material/Chat, pero en Subjects la barra de contexto aparece vacía hasta activar una materia.
- **Sugerencia:** mostrar los chips de la materia activa también en Subjects (consistencia).

# Etapa 5 — Pantallas (Materias · Banco · Exámenes · Material)

> **Objetivo:** Implementar las pantallas propias que complementan el chat: gestión de materias, banco de preguntas con verificación humana, generación de exámenes, y gestión de material indexado.
>
> **Estado:** ✅ Completada
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 3 (frontend base)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 5.1 — Materias
- [x] `views/SubjectsView.vue`: listar materias registradas
- [x] Registrar nueva materia (modal/form)
- [x] Ver material indexado por materia
- [x] Seleccionar materia activa (contexto para el chat)

### 5.2 — Banco de preguntas
- [x] `views/BankView.vue`: grid/tabla de preguntas con filtros
- [x] Filtros: tema, nivel de Bloom, dificultad, tipo, verificación
- [x] Detalle de pregunta (modal/panel): enunciado, opciones, respuesta, solución
- [x] Verificación humana: marcar/desmarcar (con confirmación)
- [x] Prioridad de revisión IA (badge de color)
- [x] Exportar CSV/Excel (llama a la API)
- [x] Paginación / scroll infinito

### 5.3 — Exámenes
- [x] `views/ExamsView.vue`: listar exámenes generados
- [x] Generar examen (blueprint simple): nº de preguntas, distribución de dificultad, temas
- [x] Versiones barajadas (estilo AMC anti-copia)
- [x] Descarga de PDFs (por versión)
- [x] Historial de exámenes generados

### 5.4 — Material
- [x] `views/MaterialView.vue`: subir archivos, ver fragmentos indexados
- [x] Subir archivo → extraer → indexar (llama a la API)
- [x] Ver fragmentos indexados por archivo
- [x] Re-indexar archivo
- [x] Eliminar material (con confirmación)

### 5.5 — Validación
- [x] ~~Tests unitarios de vistas (Vitest + Vue Test Utils)~~ — omitido por decisión del proyecto (sin Vitest)
- [x] Test manual: flujo completo registrar materia → subir material → generar pregunta → guardar → verificar → generar examen → descargar PDF
- [x] `npm run build` sin errores

---

## 📐 Notas de diseño

- Las pantallas consumen los mismos stores que el chat (Pinia) — estado compartido.
- La materia activa seleccionada en Materias se usa como contexto en el chat.
- El banco de preguntas es la fuente de verdad para la verificación humana (requisito de Felipe: preguntas verificadas por humano son inmutables para el agente).
- Los exámenes se generan desde el banco (reutilizar preguntas) o generando nuevas.

---

## ✅ Criterios de aceptación

- [x] Las 4 pantallas funcionan
- [x] Flujo completo end-to-end funciona (materia → material → pregunta → examen)
- [x] Verificación humana protege preguntas (inmutables para el agente)
- [x] Build de producción sin errores

---

## 📝 Notas de sesión

### Sesión 2026-10-05

- **Endpoints backend nuevos** (`projects/exam-app/src/exam_app/api/v1/`): las vistas necesitaban endpoints REST que no existían. Se crearon `subjects.py` (GET/POST /subjects, GET /subjects/{id}/questions, PUT /questions/{id}/verification, DELETE /questions/{id}) y `exams.py` (GET /subjects/{id}/exams, GET/DELETE /subjects/{id}/material). Registrados en `main.py`.
- **Guardrails respetados**: la verificación humana pasa por `core.domain.bank.service.set_human_verification` (nunca SQL directo); `delete_question` lanza `SecurityError` (HTTP 403) si la pregunta está verificada por humano.
- **Banco**: filtros combinables (tema/Bloom/dificultad/tipo/verificación) en memoria sobre el listado; detalle expandible con notas de revisión IA.
- **Exámenes**: formulario de blueprint simplificado con presets de Bloom y dificultad; versiones anti-copia (1-10); llama a `POST /exams/generate` (pipeline batch existente).
- **Material**: agrupación por `source_file` con conteo de chunks, expandir/colapsar, eliminar por fuente o todo (con confirmación).
- **Validación**: smoke tests con TestClient sobre la BD real (8 materias, 13 preguntas, 141 chunks, 11 exámenes) + `npm run build` ✓.

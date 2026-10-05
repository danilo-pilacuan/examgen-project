# Etapa 5 — Pantallas (Materias · Banco · Exámenes · Material)

> **Objetivo:** Implementar las pantallas propias que complementan el chat: gestión de materias, banco de preguntas con verificación humana, generación de exámenes, y gestión de material indexado.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 2-3
> **Depende de:** Etapa 3 (frontend base)

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 5.1 — Materias
- [ ] `views/SubjectsView.vue`: listar materias registradas
- [ ] Registrar nueva materia (modal/form)
- [ ] Ver material indexado por materia
- [ ] Seleccionar materia activa (contexto para el chat)

### 5.2 — Banco de preguntas
- [ ] `views/BankView.vue`: grid/tabla de preguntas con filtros
- [ ] Filtros: tema, nivel de Bloom, dificultad, tipo, verificación
- [ ] Detalle de pregunta (modal/panel): enunciado, opciones, respuesta, solución
- [ ] Verificación humana: marcar/desmarcar (con confirmación)
- [ ] Prioridad de revisión IA (badge de color)
- [ ] Exportar CSV/Excel (llama a la API)
- [ ] Paginación / scroll infinito

### 5.3 — Exámenes
- [ ] `views/ExamsView.vue`: listar exámenes generados
- [ ] Generar examen (blueprint simple): nº de preguntas, distribución de dificultad, temas
- [ ] Versiones barajadas (estilo AMC anti-copia)
- [ ] Descarga de PDFs (por versión)
- [ ] Historial de exámenes generados

### 5.4 — Material
- [ ] `views/MaterialView.vue`: subir archivos, ver fragmentos indexados
- [ ] Subir archivo → extraer → indexar (llama a la API)
- [ ] Ver fragmentos indexados por archivo
- [ ] Re-indexar archivo
- [ ] Eliminar material (con confirmación)

### 5.5 — Validación
- [ ] Tests unitarios de vistas (Vitest + Vue Test Utils)
- [ ] Test manual: flujo completo registrar materia → subir material → generar pregunta → guardar → verificar → generar examen → descargar PDF
- [ ] `npm run build` sin errores

---

## 📐 Notas de diseño

- Las pantallas consumen los mismos stores que el chat (Pinia) — estado compartido.
- La materia activa seleccionada en Materias se usa como contexto en el chat.
- El banco de preguntas es la fuente de verdad para la verificación humana (requisito de Felipe: preguntas verificadas por humano son inmutables para el agente).
- Los exámenes se generan desde el banco (reutilizar preguntas) o generando nuevas.

---

## ✅ Criterios de aceptación

- [ ] Las 4 pantallas funcionan
- [ ] Flujo completo end-to-end funciona (materia → material → pregunta → examen)
- [ ] Verificación humana protege preguntas (inmutables para el agente)
- [ ] Build de producción sin errores

---

## 📝 Notas de sesión

- (vacío)

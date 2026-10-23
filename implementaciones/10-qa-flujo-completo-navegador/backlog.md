# Backlog priorizado — ronda de corrección

> Orden sugerido de ejecución. P0 = bloquea el caso de uso central (generar examen). P1 = funcionalidad rota con workaround o pérdida de trabajo. P2 = calidad/UX.

## P0 — Bloqueantes del flujo principal

| # | Tarea | Resuelve | RFC | Esfuerzo |
|---|---|---|---|---|
| 1 | nginx: `client_max_body_size`, timeouts largos + `proxy_buffering off` en `/api/`, `location = /exams/generate` | BUG-02, 03, 05, 07 | RFC-01 | S |
| 2 | Heartbeat SSE + evento `error` tipado + retry en el cliente | BUG-03, 06, 07, 10 | RFC-02 | M |
| 3 | Pipeline: fallar si `approved_items` está vacío (no compilar/publicar) + `rejection_log` en el JSON | BUG-04 | RFC-04 | S |
| 4 | Re-test E2E del examen: chat (10 preguntas, 2 versiones) y formulario Exams | validación | — | S |

**Definición de "hecho" (P0):** un profesor puede, solo con el navegador: subir material de 5 MB, generar un examen de 10 preguntas por chat, descargar el ZIP con las 2 versiones (con y sin respuestas) y ver el examen en la vista Exams de su materia.

## P1 — Funcionalidad rota con workaround

| # | Tarea | Resuelve | RFC | Esfuerzo |
|---|---|---|---|---|
| 5 | QuestionCard: token en body + props `subjectId`/`threadId` desde MessageList | BUG-01 | RFC-03 | S |
| 6 | Historial de exámenes filtrado por materia (migrar legacy a BD, quitar fallback por prefijo) | BUG-08 | RFC-05 | M |
| 7 | Contadores de contexto reactivos al cambiar de materia | BUG-09 | RFC-06 | XS |
| 8 | Idempotencia/estado del `save_pending_question` tras stream muerto (re-consulta al banco) | BUG-10 | RFC-02 | S |

## P2 — Calidad y UX

| # | Tarea | Resuelve | Esfuerzo |
|---|---|---|---|
| 9 | Indexación de material en background con progreso | ISS-01 | M |
| 10 | Eventos de progreso del pipeline en el chat (por pregunta / compilando) | ISS-02 | M |
| 11 | Mensajes de error accionables en subidas (413/401/403) y en el formulario de Exams | BUG-12, ISS-07 | S |
| 12 | `HEAD` en `/output` + `Content-Disposition: attachment` | BUG-11, ISS-06 | XS |
| 13 | Paginación/virtualización del Banco | ISS-03 | M |
| 14 | Virtualización/paginación del historial del chat | ISS-04 | M |
| 15 | `content_language` explícito para preguntas (en/es) alineado con el template | ISS-05 | M |
| 16 | Advertencia de duplicados al guardar preguntas del chat (similitud por embedding) | ISS-08 | S |
| 17 | `overflow-x` para tablas markdown anchas | ISS-10 | XS |

## Deuda técnica observada (sin ticket)

- `evaluator_node`/`generator_node` tragan excepciones y las convierten en rechazos silenciosos: añadir logging estructurado (contexto `pipeline:*` ya existe en `llm_responses`; usarlo también para errores).
- `dedup_similarity_threshold` por solapamiento de tokens (placeholder declarado en el código): pendiente el paso a embeddings reales (ya anotado en ARCHITECTURE.md como pendiente).
- `max_total_llm_calls = 200` no alcanza para exámenes grandes con reintentos (10 preguntas × (gen+eval) × 3 reintentos = 60; OK, pero con 50 preguntas y rechazos se acerca al límite): revisar la política al escalar.
- Tests E2E automatizados (Playwright) del flujo crítico: registrar materia → subir material → 3 preguntas HITL → examen → descarga ZIP. Hoy todo el QA fue manual.

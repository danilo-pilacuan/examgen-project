# Backlog priorizado — ronda 3

> Orden sugerido de ejecución. P0 = rompe la percepción de sesión (bugs nuevos). P1 = funcionalidad rota con workaround. P2 = calidad/UX.

## P0 — Bugs nuevos de esta ronda

| # | Tarea | Resuelve | RFC | Esfuerzo | Estado |
|---|---|---|---|---|---|
| 1 | nginx: no sombrear `/subjects` y `/questions` (Accept-based routing) | BUG-15 | RFC-08 | M | ✅ Aplicado y verificado |
| 2 | `apiFetch` con `Accept: application/json` por defecto | BUG-15 | RFC-09 | XS | ✅ Aplicado y verificado |

## P1 — Robustez de sesión

| # | Tarea | Resuelve | RFC | Esfuerzo |
|---|---|---|---|---|
| 3 | Retry único ante 401 con token vigente | BUG-16 | RFC-12 | S |
| 4 | Persistir la materia activa entre recargas | ISS-11 | RFC-10 | XS |
| 5 | Re-hidratar la burbuja tras un Retry | ISS-13 | RFC-11 | S |

## P2 — Calidad y UX

| # | Tarea | Resuelve | Esfuerzo |
|---|---|---|---|
| 6 | `pointer-events: none` en el cursor de streaming (clicks en widgets durante streaming) | ISS-12 | XS |
| 7 | Mostrar "2/3 preguntas" cuando el examen tiene menos de las solicitadas | ISS-14 | S |
| 8 | Desambiguar exámenes con el mismo nombre en la vista Exams | ISS-15 | S |
| 9 | Chips de contexto también en la vista Subjects | ISS-16 | XS |

## Deuda técnica heredada (sin ticket, de rondas anteriores)

- Indexación de material en background con progreso (ISS-01, ronda 1).
- Eventos de progreso del pipeline en el chat (ISS-02, ronda 1).
- Paginación/virtualización del Banco (ISS-03) y del historial del chat (ISS-04).
- `content_language` explícito para preguntas (ISS-05, RFC-07 ronda 1).
- Advertencia de duplicados al guardar preguntas del chat (ISS-08).
- Migración de exámenes legacy a la tabla `exams` con `subject_id` (RFC-05 ronda 1, parcialmente cubierto por el filtro de huérfanos de la ronda 2).
- Tests E2E automatizados (Playwright) del flujo crítico: esta ronda se ejecutó manualmente con Playwright; scripted sería el siguiente paso.

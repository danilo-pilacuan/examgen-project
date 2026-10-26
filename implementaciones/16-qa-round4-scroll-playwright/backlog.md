# Backlog — post Ronda 4

Prioridades actualizadas tras la ronda 4 (scroll + toggles). Items cerrados se remueven;
ver `bugs.md` de cada ronda para los fixes ya integrados.

## P1 (bloqueante para tesis/demo)

- *(vacío — RC2 mantiene su certificación E2E y la ronda 4 cierra los dos bugs de navegación)*

## P2 (importante, no bloqueante)

- **ISS-17:** restaurar materia activa tras hard reload (persistir `activeSubjectId` en
  localStorage y bootstrap en el store).
- **Tests E2E automatizados:** convertir la matriz QA de la ronda 4 en suite Playwright
  versionada (`projects/frontend/e2e/`) ejecutable con `npx playwright test` contra el stack
  Docker. Casos mínimos: login, activar materia, scroll en Exams/Bank con listas largas, toggle
  de verificación (cubre BUG-17b por completo), generar examen de prueba.

## P3 (mejoras)

- **ISS-18:** conteo del agente debe venir de la BD, no del estado de sesión.
- Tool-cards del chat: ajustar ancho en viewports chicos.
- Confirmar visualmente el PDF de un examen multi-versión (se validó ZIP en rondas previas,
  el preview en navegador no).

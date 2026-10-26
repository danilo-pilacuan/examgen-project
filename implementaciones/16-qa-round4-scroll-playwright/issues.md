# Issues — Ronda 4 (2026-10-26)

## ISS-17 · Navegación SPA pierde la materia activa en recarga completa

- **Componente:** frontend (router / store de subjects)
- **Detectado en:** QA Playwright ronda 4
- **Descripción:** al navegar con `page.goto()` (recarga completa, no navegación SPA), la materia
  activa vuelve a "— Select subject —" aunque la sesión (token) persiste en localStorage. La
  navegación por clicks en la nav (router-link) sí la conserva.
- **Impacto:** bajo (solo recargas manuales; el flujo normal SPA no se ve afectado).
- **Workaround actual:** el usuario re-selecciona la materia tras un hard reload.
- **Propuesta:** persistir `activeSubjectId` en localStorage junto con `mvp_auth` y restaurarlo en
  el bootstrap del store.
- **Estado:** abierto (P2, backlog).

## ISS-18 · Conteo del agente no refleja la BD real

- **Componente:** agents-backend (herramienta de listado/conteo de preguntas)
- **Detectado en:** QA Playwright ronda 4 (pregunta "How many questions are in the bank?")
- **Descripción:** el agente responde con el estado de su sesión (1 pregunta por materia, total
  6), mientras la BD tiene 21 preguntas en "Base de Datos" (y el Bank las muestra todas). Las
  tool-cards del stream sí listaron filas de otras materias, lo que evidencia la divergencia.
- **Impacto:** medio (puede confundir al docente: la "verdad" del chat no coincide con el Bank).
- **Propuesta:** la herramienta de conteo debe consultar la BD (agregado por materia) o el estado
  compartido del proyecto, no el estado local de la conversación.
- **Estado:** abierto (P3, backlog — ver implementaciones/16-qa-round4-scroll-playwright/README.md §5).

## Nota cosmética

- Tool-cards "Question bank (n)" más anchas que el panel del chat en viewports chicos
  (overflow horizontal dentro de la card). Sin fix requerido para RC2.

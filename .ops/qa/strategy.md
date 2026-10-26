---
id: qa-strategy
tipo: Guide
type: Guide
title: Estrategia de QA y reglas de validacion
description: Que significa verificado en este proyecto y como se ejecuta cada ronda.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001, templates-base]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

Definicion de "verificado" (regla del proyecto): **navegador real**, nunca solo
curl/TestClient. Stack completo Docker healthy antes de cualquier ronda. Regla de
sesion: toda interaccion exclusivamente por navegador integrado + Playwright.

## Validacion sin pytest/vitest (producto)

- `py_compile` de modulos tocados (en contenedor); smoke TestClient+SQLite solo si se
  toca logica de servicio.
- Frontend: `npm run type-check` + `lint:check` + `build-only`.
- Rebuild Docker de los containers cuyo codigo/conf va horneado (nginx, exam-app).
- E2E manual en navegador sobre `http://localhost:3000`.

## Reglas duras de las rondas (aprendidas)

- Probar cada endpoint REST por su ruta real via nginx (apiFetch), no solo via
  TestClient: el routing condicional por `Accept` exige cubrir TODOS los metodos HTTP
  por prefijo (BUG-015/BUG-017b).
- Restablecer el estado mutado por la prueba (toggles, filas) al terminar.
- Scripts de debug en contenedor: `dos2unix` (CRLF de Windows).
- Severidades: CRITICAL bloquea el flujo principal; HIGH funcionalidad rota con
  workaround; MEDIUM degrada la experiencia; LOW cosmetico/edge.

## Casos de prueba

La matriz de checks C1-C13/R1-R7 y las rondas se registran en `test-plan.md`; la
cobertura REQ->BL->IMPL->QT con evidencia, en `traceability.md`.
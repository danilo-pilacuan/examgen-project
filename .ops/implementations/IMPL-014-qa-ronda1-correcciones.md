---
id: IMPL-014
tipo: Implementation
type: Implementation
title: Correcciones ronda 1 + certificacion
description: Fixes 11.1-11.6 y P0 del backlog; plan de certificacion C1-C13/R1-R7 (2026-10-22/23).
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-001, IMPL-013, IMPL-016]
status: stable
---

## Alcance

Incluye: verificacion en codigo real de los 12 bugs + 10 issues de la ronda 1, aplicacion
de los fixes 11.1-11.6 (QuestionCard token/props, idempotencia del guardado HITL, HEAD
/output, mensajes accionables, overflow-x de tablas) y el plan de certificacion E2E
(C1-C13, R1-R7) con trazabilidad bug -> RFC -> fix -> check. No incluye: 11.2
(migracion legacy completa, cubierta parcialmente en ronda 2 y en BL-014).

## Diseno

Hallazgo de la sesion 2026-10-22: los P0 (RFC-01/02/04) ya estaban aplicados en el
working tree de los 3 submodulos; quedaban 11.1-11.6, todos certificados en la ronda 3
(IMPL-016). Validacion estatica sin pytest/vitest (regla del proyecto): py_compile,
type-check, lint:check, build-only; smoke con TestClient+SQLite solo si se toca logica de
servicio. Tabla completa de trazabilidad en `../qa/traceability.md`.
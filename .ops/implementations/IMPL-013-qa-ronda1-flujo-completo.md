---
id: IMPL-013
tipo: Implementation
type: Implementation
title: QA ronda 1 - flujo completo en navegador
description: Primera ronda QA E2E manual (2026-10-19); 12 bugs, 10 issues, 7 RFCs detectados.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-014]
status: stable
---

## Alcance

Incluye: primera ronda QA del flujo completo actuando como profesor real en navegador
(Docker + Playwright ad-hoc); deteccion y registro de 12 bugs (BUG-001..012), 10 issues
(ISS-01..10) y 7 RFCs de solucion (RFC-01..07), con backlog priorizado P0/P1/P2.

## Diseno

Metodo: navegador real, no curl/TestClient, para validar la UI como la ve el usuario
(regla del proyecto). El QA ejecuto el pipeline de fixes: los P0 (RFC-01/02/04) quedaron
aplicados en el working tree durante la sesion; la certificacion completa ocurrio en las
rondas 2-3. Detalle por bug: `.ops/qa/BUG-001..BUG-012.md`; issues de producto en
`.ops/project/backlog/BL-003..BL-007.md`.
---
id: BL-010
tipo: BacklogItem
type: BacklogItem
title: Suite Playwright versionada del flujo critico
description: Convertir la matriz QA en suite e2e versionada ejecutable contra el stack Docker.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [REQ-001]
status: draft
---

## Descripcion

Todo el QA fue manual o con navegador ad-hoc (deuda registrada desde la ronda 1 y
reconfirmada en las rondas 3 y 4). Convertir la matriz QA en
`projects/frontend/e2e/` ejecutable con `npx playwright test` contra el stack Docker.
Casos minimos: login, activar materia, scroll en Exams/Bank con listas largas, toggle de
verificacion (cubre BUG-017b por completo), generar examen de prueba.

## Criterio de salida

La suite corre verde contra el stack Docker levantado y cubre los cinco casos minimos.

## Resultado (ronda 10, 2026-10-28)

Suite creada y en verde: playwright.config.ts + e2e/helpers.ts (login UI +
fixture authedPage) + 3 specs (functional F1-F12, integration I1-I8,
language L1-L2) = 15 tests, `npx playwright test` -> 15/15 PASS contra el
stack Docker. Credenciales y materia via env (e2e/.env.example). Cabeza de
serie para QT-010/IMPL-027. Evidencia: test-plan ronda 10.

## IMPL

IMPL-019, IMPL-027
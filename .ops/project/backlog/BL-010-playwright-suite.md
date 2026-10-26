---
id: BL-010
tipo: BacklogItem
type: BacklogItem
title: Suite Playwright versionada del flujo critico
description: Convertir la matriz QA de la ronda 4 en suite e2e versionada ejecutable contra el stack Docker.
estado: listo
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001]
status: draft
---

## Descripcion

Todo el QA fue manual o con navegador ad-hoc (deuda registrada desde la ronda 1 y
reconfirmada en las rondas 3 y 4). Convertir la matriz de la ronda 4 en
`projects/frontend/e2e/` ejecutable con `npx playwright test` contra el stack Docker.
Casos minimos: login, activar materia, scroll en Exams/Bank con listas largas, toggle de
verificacion (cubre BUG-017b por completo), generar examen de prueba.

## Criterio de salida

La suite corre verde contra el stack Docker levantado y cubre los cinco casos minimos.

## IMPL

IMPL-019
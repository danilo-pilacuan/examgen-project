---
id: IMPL-000
tipo: Implementation
type: Implementation
title: Reestructuracion del monorepo
description: Reorganizar el proyecto en monorepo con proyectos/, docker/ y documentacion de soporte.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-15
relaciona: [BL-001, IMPL-017]
status: stable
---

## Alcance

Incluye: estructura del monorepo (projects/, docker/, docs/), separacion de concerns
entre frontend, exam-app, agents-backend, core y latex-compiler, y convenciones de
commits por submodulo. No incluye: repos remotos ni CI (IMPL-001).

## Diseno

El meta-repo orquesta via git submodules; cada submodulo es un repo propio con historial
independiente. Los informes de estado viven en el meta-repo (antes implementaciones/,
hoy .ops/). Verificado E2E; el informe RC1 (IMPL-017) lista el arbol final.
---
id: IMPL-010
tipo: Implementation
type: Implementation
title: Mapa de dependencias
description: Grafo de dependencias entre submodulos con la direccion prohibida de imports.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-18
relaciona: [BL-001]
status: stable
---

## Alcance

Incluye: mapa de dependencias del monorepo (frontend -> exam-app -> agents-backend ->
core -> latex-compiler; docker orquesta; ningun import inverso) y el orden de commits por
submodulo. No incluye: enforcement automatico en CI (pendiente de IMPL-001).

## Diseno

Regla operativa verificada en las rondas: los fixes cruzados (SSE heartbeat, routing
nginx) tocaron hasta 3 submodulos y se commit-earon atmicamente por submodulo con
punteros al final. Verificado en las 4 rondas QA; el informe RC1 lista el estado por
repo.
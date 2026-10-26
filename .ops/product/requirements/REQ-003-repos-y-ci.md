---
id: REQ-003
tipo: Requirement
type: Requirement
title: Repositorios remotos, submodulos y CI del meta-repo
description: Publicar los 6 submodulos en GitHub con CI; unica etapa de desarrollo pendiente.
estado: propuesto
dueno: rol:propietario
fecha: 2026-10-22
relaciona: [BL-001]
status: draft
sources: [{ id: copilot-instructions, resource: ../../.github/copilot-instructions.md, title: copilot-instructions }]
---

## Requisito

Los repos de los submodulos deben existir en GitHub con CI minima (build/lint por
submodulo) y los punteros de submodulo del meta-repo deben resolverse desde clones
limpios. Derivado de la etapa 01 (hoy IMPL-001) y de la deuda listada en el informe
RC1 (seccion 7).

## Criterio de aceptacion

Clon fresco del meta-repo con `--recurse-submodules` compila y levanta el stack Docker;
CI verde en los repos de submodulo; gitleaks verde.

## No objetivos

CD y despliegue productivo; registries privados.
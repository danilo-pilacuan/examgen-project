---
id: IMPL-001
tipo: Implementation
type: Implementation
title: Repos y submodulos + CI
description: Publicar los repos de submodulos en GitHub con CI; unica etapa de desarrollo pendiente.
estado: borrador
dueno: rol:propietario
fecha: 2026-10-15
relaciona: [BL-001]
status: draft
---

## Alcance

Incluye: crear los repos remotos de los 6 submodulos, configurar CI minima (build/lint
por submodulo, gitleaks) y hacer resolubles los punteros desde clones limpios. No
incluye: CD ni despliegue productivo.

## Diseno

Los repos locales ya estan listos y los submodulos funcionan localmente; falta la parte
remota. Deriva del requisito REQ-003 (criterio: clon fresco compila y levanta el stack).
Estado: pendiente de ejecucion; no bloquea el escrito de la tesis (informe RC1, seccion
7). Pasos al reanudar: crear remotos -> push de cada submodulo -> CI en cada repo ->
verificar clon fresco con --recurse-submodules.
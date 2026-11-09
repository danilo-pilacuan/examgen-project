---
id: BL-001
tipo: BacklogItem
type: BacklogItem
title: Repos remotos en GitHub y CI del meta-repo
description: Crear los remotos de los 6 submodulos y CI minima; pendiente desde la etapa 01.
estado: listo
dueno: rol:propietario
fecha: 2026-10-22
relaciona: [REQ-003]
status: draft
---

## Descripcion

Los repos locales de los submodulos estan listos y con commits publicados via punteros,
pero los remotos en GitHub no existen y el meta-repo carece de CI. Deriva de la deuda
listada en el informe RC1 (seccion 7, "infraestructura del proyecto").

## Criterio de salida

Clon fresco con `--recurse-submodules` compila; CI por submodulo verde; gitleaks verde.

## IMPL

IMPL-001
---
id: BL-000
tipo: BacklogItem
type: BacklogItem
title: Migrar implementaciones al arbol .ops
description: Convertir los documentos de etapas, QA y handoff a documentos OKF .ops y retirar la carpeta antigua.
estado: hecho
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001]
status: stable
---

## Descripcion

Migrar `implementaciones/` (19 docs de etapa, 3 carpetas de ronda QA con bugs/issues/
rfcs/backlog, HANDOFF y README de etapas) al arbol `.ops` siguiendo el contrato OKF 0.2
de `templates/base.md`: IMPL por etapa, BUG por defecto, BL por item de backlog, REQ de
producto, handoff y plan en project/, traceability en qa/. Regla de sesion derivada de
la politica permanente de estado e implementacion (`.github/copilot-instructions.md`,
seccion 0).

## Criterio de salida

Todo el contenido accesible bajo `.ops` con ids unicos, frontmatter conforme, sin
diacriticos; `implementaciones/` eliminado; referencias externas actualizadas.

## IMPL

IMPL-020
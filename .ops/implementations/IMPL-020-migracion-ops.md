---
id: IMPL-020
tipo: Implementation
type: Implementation
title: Migracion de implementaciones al arbol .ops
description: Convertir y mover la documentacion de etapas/QA/handoff a documentos OKF 0.2 en .ops.
estado: borrador
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [BL-000]
status: draft
---

## Alcance

Incluye: bootstrap del arbol `.ops` (READMEs de carpeta, templates/, product/REQ,
project/plan+handoff, qa/BUG+traceability, project/backlog/BL) y conversion de los 19
documentos de `implementaciones/` en IMPL-000..019, 18 BUGs, 21 BLs y 3 REQs, con
actualizacion de referencias externas (ARCHITECTURE.md, docs/informe_avance.md,
readme.md) y eliminacion de la carpeta original. No incluye: codigo de producto.

## Diseno

Mapeo: etapa NN -> IMPL-NNN (id derivado del numero de etapa); bugs conservan su
numeracion historica (BUG-001..BUG-017b) con estado corregido -> verificado cuando el
fix fue certificado en una ronda posterior; ISS -> BL de backlog (estado idea; con fix
aplicado se dejan como referencia en el IMPL de la ronda); RFCs se conservan como
contenido de los BUG/IMPL correspondientes; HANDOFF -> project/handoff.md con la
estructura de 8 secciones; README de etapas -> project/plan.md + indice raiz. Sin
diacriticos (politica de lenguaje); el agente no escribe `verified`.

## Ejecucion y verificacion

Ejecutada en la sesion del 2026-10-26: 89 archivos `.ops` validados por script (ids
unicos, frontmatter conforme, ASCII limpio, <=40 lineas de contenido); referencias
externas actualizadas; carpeta original eliminada. Queda `borrador` hasta la revision
del propietario (que es quien puede dejarla `ejecutado`).
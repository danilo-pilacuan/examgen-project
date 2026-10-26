---
id: TEMPLATE-BL
tipo: Template
type: Template
title: Plantilla de item de backlog (BL)
description: Modelo para project/backlog/BL-NNN.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: BL-000
tipo: BacklogItem
type: BacklogItem
title: <Titulo corto>
description: <Una linea>
estado: idea               # idea | listo | en-curso | en-qa | en-uat | hecho
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: [REQ-000]       # regla de trazabilidad: todo BL enlaza un REQ
status: draft
---

## Descripcion

<Que se hara; deriva de AGENTS.md con la seccion citada.>

## Criterio de salida

<Textual de la seccion 11 de AGENTS.md o derivado directo de ella.>

## IMPL

<Ids IMPL-NNN que ejecutan este BL; vacio hasta que existan.>

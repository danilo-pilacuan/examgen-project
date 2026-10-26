---
id: TEMPLATE-REQ
tipo: Template
type: Template
title: Plantilla de requisito (REQ)
description: Modelo para product/requirements/REQ-NNN.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: REQ-000
tipo: Requirement
type: Requirement
title: <Titulo corto>
description: <Una linea>
estado: propuesto         # propuesto | aprobado
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: []             # BL, QT o DEC relacionados
status: draft
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

## Requisito

<Que debe cumplir el sistema; derivado de AGENTS.md, con la seccion citada.>

## Criterio de aceptacion

<Verificable; enlaza QT en qa/traceability.md.>

## No objetivos

<Que no cubre, si aplica (seccion 1 de AGENTS.md).>

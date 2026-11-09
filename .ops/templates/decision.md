---
id: TEMPLATE-DEC
tipo: Template
type: Template
title: Plantilla de decision (DEC)
description: Modelo para decisions/DEC-NNN.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: DEC-000
tipo: Decision
type: Decision
title: <Pregunta>
description: <Una linea>
estado: abierta            # abierta | tomada | rechazada
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: []              # solo ids existentes
status: draft
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

## Pregunta

<La pregunta, tal como la define AGENTS.md seccion 12; sin opciones inventadas si la fuente no las trae.>

Fase en que se necesita (secciones 12 u 11): <fase.> Opciones con riesgos en maximo 6 lineas solo si rol:propietario las pide (regla 6). Resolucion: <vacia mientras estado = abierta; al cerrar, decision + fecha + verified por human:propietario.>

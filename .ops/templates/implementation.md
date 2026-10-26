---
id: TEMPLATE-IMPL
tipo: Template
type: Template
title: Plantilla de plan de implementacion (IMPL)
description: Modelo para implementations/IMPL-NNN-<slug>.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: IMPL-000-<slug>
tipo: Implementation
type: Implementation
title: <Tarea concreta>
description: <Una linea>
estado: borrador           # borrador | aprobado | ejecutado
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: [BL-000]        # regla de trazabilidad: todo IMPL enlaza un BL
status: draft
---

## Alcance

<Que incluye y que no.>

## Diseno

<Decisiones tecnicas y por que; enlaza DEC si existen.>

Pasos atomicos en orden, archivos tocados, pruebas (casos que pasan y de rechazo, regla 3 de la seccion 0) y rollback: <rellenar por tarea.>

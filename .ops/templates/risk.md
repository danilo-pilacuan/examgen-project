---
id: TEMPLATE-RSK
tipo: Template
type: Template
title: Plantilla de riesgo (RSK)
description: Modelo para governance/risks.md (registro en una tabla) o riesgos mayores.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

Los riesgos ordinarios viven como filas de la tabla en [risks](../governance/risks.md) (columnas: id, riesgo, limite de AGENTS.md, estado, mitigacion). Solo un riesgo con plan propio merece archivo:

---
id: RSK-000
tipo: Risk
type: Risk
title: <Riesgo>
description: <Una linea>
estado: abierto            # abierto | mitigado | cerrado
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: []              # REQ, BL o DEC asociados
status: draft
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

## Riesgo

<Condicion y consecuencia; deriva de la seccion 13 de AGENTS.md.>

## Mitigacion y senal de disparo

<Que se hace y que lo activa. No construir mitigacion antes de que duela (principio 10).>

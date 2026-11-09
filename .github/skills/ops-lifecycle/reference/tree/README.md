---
id: ops-readme
tipo: Guide
type: Guide
title: .ops - gobierno del ciclo de vida
description: Metadatos de gestion y gobernanza del proyecto; el conocimiento de la plataforma vive en core/ y orgs/.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: []
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../AGENTS.md, title: AGENTS.md v3 }]
---

Contrato OKF 0.2 (plantillas, vocabulario de estados, actores y confianza) en [templates/base.md](templates/base.md).
Fuente de verdad del avance: [../PROGRESS.md](../PROGRESS.md) (regla 7); `.ops` lo organiza y enlaza, nunca lo duplica ni lo sustituye.

## Areas y arboles

| Arbol | Contenido | README |
|---|---|---|
| product/ | REQ y vision de producto | [product/README.md](product/README.md) |
| project/ | plan de fases, backlog, resumen de avance | [project/README.md](project/README.md) |
| architecture/ | vista general, NFR, modelo de amenazas | [architecture/README.md](architecture/README.md) |
| decisions/ | registro de decisiones abiertas y cerradas | [decisions/README.md](decisions/README.md) |
| governance/ | carta, RACI, DoR/DoD, control de cambios, riesgos | [governance/README.md](governance/README.md) |
| qa/ | estrategia, trazabilidad REQ-IMPL-QT, defectos | [qa/README.md](qa/README.md) |
| implementations/ | especificaciones y verificacion por fase (fase-0..fase-10) | [implementations/README.md](implementations/README.md) |
| ux-and-interfaces/ | CLI, salidas y usabilidad de MCP | [ux-and-interfaces/README.md](ux-and-interfaces/README.md) |
| security/ | vulnerabilidades, revision de MRs y revisiones periodicas | [security/README.md](security/README.md) |
| operations/ | runbooks, releases, objetivos de servicio e incidentes | [operations/README.md](operations/README.md) |
| data/ | migraciones de esquema y datos, modelo logico | [data/README.md](data/README.md) |
| development/ | guias de codigo, revision, ramas y onboarding | [development/README.md](development/README.md) |
| templates/ | plantilla base y plantillas por tipo | [templates/README.md](templates/README.md) |

## Reglas del arbol

1. Todo documento lleva frontmatter OKF 0.2 con `id` unico; el vocabulario de `estado` por tipo vive en templates/base.md.
2. Un archivo por documento; los registros extensos (DEC, RSK, BUG, QT, VULN, RUN, MIG, REL) se abren como archivos y se referencian desde su indice.
3. Todo estado `verified` exige revision humana (rol:propietario o rol:funcional); el agente nunca se lo asigna a si mismo.
4. Antes de mover o renombrar documentos, leer [governance/change-control.md](governance/change-control.md); los cambios a AGENTS.md requieren aprobacion humana.
5. El contenido que reproduce requisitos se cita por seccion de AGENTS.md; no se parafrasea como regla nueva.

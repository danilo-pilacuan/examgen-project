---
id: operations-readme
tipo: Guide
type: Guide
title: Operations - operacion y releases
description: Runbooks, releases y objetivos de servicio; hoy con el runbook de exposicion publica.
estado: vigente
dueno: rol:propietario
fecha: 2026-11-09
relaciona: [ops-readme]
status: stable
---

- **Proposito:** como se opera la plataforma: runbooks, releases y la vista de servicio.
- **Escribe:** rol:agente (propone) | **Aprueba:** rol:propietario.
- **Cuando:** al ejecutar una operacion recurrente, desplegar o revisar objetivos de servicio.
- **Plantillas:** `templates/run.md` y `templates/release.md` (copias de referencia en la skill ops-lifecycle).

## Documentos

| Doc | Contenido |
|---|---|
| [runbooks.md](runbooks.md) | registro de RUN-NNN; hoy RUN-016 (exposicion publica via cloudflared) |
| [recipe-levantamiento.md](recipe-levantamiento.md) | secuencia de comandos para levar el stack y exponerlo (agnostico a credenciales) |


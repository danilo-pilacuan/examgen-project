---
id: security-readme
tipo: Guide
type: Guide
title: Security - seguridad de la plataforma
description: Vulnerabilidades, revisiones de MR y revisiones periodicas; complementa al modelo de amenazas de architecture/.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [ops-readme]
status: stable
---

- **Proposito:** gestion de hallazgos de seguridad del ciclo de vida: registramos, mitigamos y verificamos.
- **Escribe:** rol:agente (propone) · **Aprueba:** rol:propietario.
- **Cuando:** al detectar un hallazgo en un MR, revision periodica o incidente.
- **Plantilla:** [templates/vuln.md](../templates/vuln.md).

## Documentos

| Doc | Contenido |
|---|---|
| [vulns.md](vulns.md) | registro de VULN-NNN con severidad y mitigacion |
| [mr-review.md](mr-review.md) | checklist de revision de seguridad para MRs |
| [periodic.md](periodic.md) | revisiones periodicas: dependencias y secretos |

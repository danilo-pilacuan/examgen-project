---
id: README-000
tipo: Guide
type: Guide
title: Plantilla de README de carpeta
description: Modelo de maximo 15 lineas para el README.md de cada carpeta.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [templates-base]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

Copiar como `README.md` de la carpeta con `id` = `<carpeta>-readme` (p. ej. `qa-defects-readme`).

Frontmatter minimo (11 lineas): `id`, `tipo: Guide`, `type: Guide`, `title`, `description` (una linea), `estado: vigente`, `dueno: rol:propietario`, `fecha`, `relaciona`, `status: stable`.

Cuerpo de 4 lineas:
- **Proposito:** que guarda la carpeta y cuando se usa.
- **Escribe:** rol:agente (propone) | **Aprueba:** rol:propietario.
- **Cuando se usa:** momento del ciclo de vida.
- **Plantilla:** /templates/<archivo>.md

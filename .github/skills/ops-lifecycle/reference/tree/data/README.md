---
id: data-readme
tipo: Guide
type: Guide
title: Data - datos y migraciones
description: Registro de migraciones MIG-NNN y mapa del modelo logico; cubre la disciplina DBA.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [ops-readme]
status: stable
---

- **Proposito:** cambios de esquema y datos con apply/revert/verify, y el mapa del modelo logico compartido.
- **Escribe:** rol:agente (propone) · **Aprueba:** rol:propietario.
- **Cuando:** al tocar el esquema (tablas, columnas, RLS) o migrar datos entre entornos.
- **Plantilla:** [templates/migration.md](../templates/migration.md).

## Documentos

| Doc | Contenido |
|---|---|
| [migrations.md](migrations.md) | registro de MIG-NNN con apply/revert/verify y rollback |
| [data-model.md](data-model.md) | mapa de tablas logicas, claves de tenancy y politicas RLS |

---
id: BUG-018
tipo: Defect
type: Defect
title: POST /exams/generate descarta campos desconocidos del blueprint en silencio
description: extra=ignore de Pydantic aceptaba num_versions/name en la raiz del blueprint sin 422; el contrato real es blueprint.metadata.
estado: resuelto
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [QT-005, IMPL-021, IMPL-022]
status: draft
---

## Evidencia

Ronda 5 (2026-10-26, API via nginx). Sonda 1: `POST /exams/generate` con
`num_versions: 2` y `name` en la RAIZ del blueprint -> HTTP 200 (sin 422),
respuesta/BD con `num_versions=1`, un solo PDF sin respuestas, y el examen
nombrado con el nombre de la materia. Sonda 2 (mismos datos anidados en
`blueprint.metadata.{title,name,num_versions}`) -> HTTP 200 con
`num_versions=2` en BD, 4 PDFs (`_A_respondido/_A/_B_respondido/_B`),
zip 200 via /output (130 KB) y `name` personalizado respetado. El frontend
usa el anidamiento correcto (`ExamsView.vue`, `blueprint.metadata`), por lo
que la UI no esta afectada.

## Causa

Pydantic v2 por defecto ignora campos extra (`model_config` sin
`extra="forbid"` en `ExamBlueprint`), y el endpoint no valida que los
metadatos vivan en `blueprint.metadata`. Un cliente REST que envie
`num_versions` en la raiz recibe 200 y un examen de 1 version sin aviso.

## Fix y verificacion

Fix (IMPL-022, rama RC3/develop): `model_config = ConfigDict(extra="forbid")` en
`ExamBlueprint` (core `domain/schemas/exam.py`); los campos mal ubicados devuelven 422
accionable via FastAPI. Verificado con script desechable: sonda 1 (raiz) ->
ValidationError/422; sonda 2 (metadata anidada) -> num_versions=2; tool del agente
(construccion por keywords) y round-trip `model_dump`/`model_validate` (columna JSON de
la tabla exams) intactos. Pendiente: re-probar las 2 sondas HTTP reales via nginx
(requiere servicios levantados).

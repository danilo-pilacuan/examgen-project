---
id: IMPL-022-rc3-bugs-conocidos
tipo: Implementation
type: Implementation
title: RC3 - fixes de bugs conocidos (BUG-018, BUG-016, BL-008)
description: Endurecimiento del blueprint, retry 401 y robustez de sesion del frontend.
estado: borrador
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [BL-008, BUG-018, BUG-016]
status: draft
---

## Alcance

Tag `RC2` creado y publicado en los 7 repos; rama `RC3/develop` creada en los 7 repos.
Incluye tres fixes de codigo: (1) BUG-018 `extra="forbid"` en `ExamBlueprint` (core);
(2) BUG-016 retry unico ante 401 con token fresco de localStorage (frontend `http.ts`);
(3) BL-008 RFC-10/11: `activeSubjectId` persistido en localStorage y re-hidratacion del
turno reintentado desde el checkpointer (stores + ChatPanel). No incluye: BL-010
Playwright suite, C2 con PDF grande real, cross-provider, etapa 01 (repos remotos CI).

## Diseno

- BUG-018: Pydantic v2 `ConfigDict(extra="forbid")` en `ExamBlueprint`; los campos mal
  ubicados (`num_versions`/`name` en la raiz) ahora producen 422 via FastAPI. El
  contrato correcto (`blueprint.metadata`) no cambia; verificado round-trip
  `model_dump`/`model_validate` (columna JSON de la tabla exams intacta).
- BUG-016 (RFC-12): en `apiFetch`, ante 401 con JWT almacenado no expirado
  (`storedTokenUnexpired()` decodifica `exp`), reintentar UNA vez releyendo el token de
  localStorage; si el reintento falla, propagar el mensaje amistoso de sesion expirada.
- BL-008 RFC-10: `mvp_active_subject` en localStorage, restaurado al crear el store;
  `setActive` persiste. RFC-11: `loadThread(id, replaceExisting=false)` agrega el
  historial del checkpointer al terminar un Retry (watch de `streaming` en ChatPanel).

## Pruebas

- Rechazo: `num_versions` en raiz -> ValidationError; JSON equivalente (via FastAPI)
  -> 422 (verificado con script desechable, pydantic 2.13).
- Aceptacion: metadata anidada -> num_versions=2; construccion por keywords del tool
  `generate_exam_from_bank` intacta; build + vue-tsc del frontend sin errores.
- Pendiente de navegador (propietario): C8 con retry, F5 conserva materia activa,
  reinicio de exam_app sin 401 visibles.

## Rollback

Revert de los 3 commits (core, frontend) en RC3/develop; sin migraciones de BD.

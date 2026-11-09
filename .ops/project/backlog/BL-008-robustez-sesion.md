---
id: BL-008
tipo: BacklogItem
type: BacklogItem
title: Robustez de sesion del frontend (401 retry, materia activa, rehidratacion)
description: RFC-10/11/12 de la ronda 3; robustez de sesion tras recargas y reinicios del backend.
estado: en_curso
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001, IMPL-022]
status: draft
---

## Descripcion

Tres propuestas P1 de la ronda 3 agrupadas: RFC-12 retry unico ante 401 cuando el token
almacenado no ha expirado (BUG-016); RFC-10 persistir `activeSubjectId` en localStorage
(ISS-11, reconfirmado como ISS-17 en la ronda 4); RFC-11 re-hidratar la burbuja desde el
checkpointer al terminar un Retry (ISS-13).

## Criterio de salida

Reiniciar exam_app con sesion activa no produce 401 visibles; F5 conserva la materia
activa; tras un Retry la burbuja muestra el contenido del turno sin recargar.

## Codigo (IMPL-022, RC3/develop)

Los tres RFCs estan implementados: RFC-12 retry 401 en `apiFetch`
(`projects/frontend/src/api/http.ts`); RFC-10 `mvp_active_subject` en localStorage
(`projects/frontend/src/stores/subjects.ts`); RFC-11 `loadThread(id, false)` tras el
Retry (`projects/frontend/src/stores/chat.ts` + `ChatPanel.vue`). Falta la verificacion
en navegador (C8 retry, F5 materia activa, reinicio exam_app).

## IMPL

IMPL-016
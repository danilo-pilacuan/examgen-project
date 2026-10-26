---
id: BL-008
tipo: BacklogItem
type: BacklogItem
title: Robustez de sesion del frontend (401 retry, materia activa, rehidratacion)
description: RFC-10/11/12 de la ronda 3; robustez de sesion tras recargas y reinicios del backend.
estado: idea
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001]
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

## IMPL

IMPL-016
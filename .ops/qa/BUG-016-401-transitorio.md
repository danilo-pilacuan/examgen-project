---
id: BUG-016
tipo: Defect
type: Defect
title: 401 transitorio en peticiones tras reiniciar exam_app (token en memoria vs localStorage)
description: 1-2 peticiones fallan con 401 aunque el JWT almacenado sigue valido; se recupera recargando.
estado: resuelto
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-003, IMPL-016, IMPL-022]
status: draft
---

## Evidencia

Ronda 3 (2026-10-23): con la sesion activa, reiniciar el contenedor `exam_app` (durante
C8) -> 1-2 peticiones fallaron con 401 (`GET /subjects`) aunque el JWT almacenado seguia
valido (exp > now, verificado decodificando el payload); tras recargar la pagina todo
funciono. No reproducible de forma determinista.

## Causa

Hipotesis: carrera entre el reinicio del backend y el token en memoria del modulo
`http.ts` (algun request salio antes de que el store restaurara el token, o el backend
rechazo durante el arranque). Impacto menor (transitorio, se recupera con recarga).

## Fix y verificacion

Fix (IMPL-022, RFC-12, rama RC3/develop): `apiFetch` reintentar UNA vez ante 401 cuando
el JWT almacenado no ha expirado (`storedTokenUnexpired()` decodifica `exp` del payload)
o el interceptor re-lee el token de localStorage antes de reintentar; si el reintento
falla, propaga el error con el mensaje de sesion expirada de `friendlyHttpMessage`.
Verificado: build + vue-tsc del frontend sin errores. Pendiente: reproducir el reinicio
de exam_app con sesion activa (C8/C10) para confirmar 0 401 visibles.
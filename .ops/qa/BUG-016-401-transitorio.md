---
id: BUG-016
tipo: Defect
type: Defect
title: 401 transitorio en peticiones tras reiniciar exam_app (token en memoria vs localStorage)
description: 1-2 peticiones fallan con 401 aunque el JWT almacenado sigue valido; se recupera recargando.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-003, IMPL-016]
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

Pendiente. RFC-12 propuesto: retry unico con backoff ante 401 cuando el token almacenado
no ha expirado (decodificar `exp` del payload) o interceptor que re-lea el token de
localStorage antes de reintentar; si el reintento falla, propagar el error con el mensaje
de sesion expirada de `friendlyHttpMessage`. Trackeado en BL-008. Unico bug abierto del
RC1/RC2 (verificado en el informe RC1, seccion 4).
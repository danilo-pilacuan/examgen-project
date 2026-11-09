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
Verificado: build + vue-tsc del frontend sin errores.

## Cierre (Ronda 6, 2026-10-27)

Verificacion robustecida con 3 reinicios independientes de `exam_app`
(`docker restart exam_app`, espera healthy + 30 s) con sesion activa:

1. Restart 1: mensaje por chat -> HTTP 200 directo en `POST /api/chat/stream`
   (sin 401 previo), HITL intacto (la pregunta pendiente sobrevivio en el
   checkpointer).
2. Restart 2: nuevo turno -> 200 directo, sin 401, ninguna recarga de pagina.
3. Restart 3 (tras C2, job de indexacion colgado): 200 directo; thread y
   materia activa intactos.

En los 3 casos el JWT venia de localStorage (sesion conservada) y NO hubo
ningun 401 visible ni recarga. Bug verificado como RESUELTO en RC3.

Nota menor (hallazgo, no bug): tras restart el store del frontend pierde
`pendingQuestion` de la sesion (el widget de la pregunta pendiente ya no se
muestra); el contenido del turno NO se pierde (checkpointer + rehidratacion
RFC-11) y el usuario puede continuar por chat. Documentado como observacion
en el test-plan de la ronda 6.
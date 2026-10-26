---
id: BUG-015
tipo: Defect
type: Defect
title: Hard reload de /subjects devuelve el JSON 401 de la API (SPA shadowed)
description: F5 en /subjects rompia la sesion visualmente; el selector de materias quedaba vacio.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-003, IMPL-016]
status: stable
---

## Evidencia

Ronda 3 (2026-10-23): F5 en `/subjects` -> el documento de la pestana pasa a ser
`{"detail":"Not authenticated"}` (401, application/json); la SPA no monta. Ademas, tras
volver por navegacion interna, `GET /subjects` del store recibia index.html (200 HTML)
porque `apiFetch` no enviaba `Accept` y nginx servia el fallback SPA.

## Causa

Dos capas: (1) nginx `location /subjects { proxy_pass ...; }` capturaba tambien la ruta
SPA (misma clase que BUG-002 con `/exams`); (2) `apiFetch` no enviaba `Accept`, asi que
nginx no podia distinguir llamadas API de navegaciones.

## Fix y verificacion

RFC-08/09: nginx proxifica solo cuando `Accept` incluye `application/json` (rewrite a
`/subjects-api` -> conservar prefijo -> `proxy_pass`); en caso contrario sirve index.html
(igual para `/questions`); `apiFetch` envia `Accept: application/json` por defecto.
Verificado (2026-10-23): hard reload de `/subjects` -> 200 HTML de la SPA con la lista
poblada; GET de API con Accept json -> 200; registro de materia + Activate OK. Nota: este
fix exige probar todos los metodos HTTP por prefijo (leccion aplicada en BUG-017b).
---
id: BUG-017b
tipo: Defect
type: Defect
title: PUT /questions/{id}/verification responde 404 via nginx
description: El toggle de verificacion del Bank era inservible desde el navegador; rewrite que eliminaba el prefijo.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [QT-004, IMPL-019]
status: stable
---

## Evidencia

Ronda 4 (2026-10-26): en Bank, click en "Remove" sobre la ultima fila ->
`PUT /questions/{id}/verification` -> 404 "Not Found" (generico de FastAPI). Directo al
backend responde 200 (TestClient en contenedor y curl). Probes curl desde dentro de
`exam_frontend`: GET y PUT directos 200, PUT via nginx falla. Por que no se detecto en la
ronda 3: la lista del Bank usa `GET /subjects/{id}/questions` (bloque `/subjects-api`,
correcto); solo las rutas raiz `/questions/...` pasaban por el bloque roto y no se
ejercito el toggle.

## Causa

En `projects/frontend/nginx.conf`, el bloque `location /questions-api` reescribia
`^/questions-api(/.*)$` a `$1` (eliminaba el prefijo `/questions`) en lugar de
`/questions$1`: el PUT llegaba al backend como `PUT /{id}/verification` -> 404.

## Fix y verificacion

Una linea: `rewrite ^/questions-api(/.*)$ /questions$1 break;` + rebuild del contenedor
frontend (el conf va horneado en la imagen). Verificado: PUT 200 via nginx con token
real; toggle bidireccional en navegador refleja `verified_by_human` en BD. Leccion: el
routing por Accept necesita tests de TODOS los metodos HTTP de cada prefijo.

Re-verificado ronda 5 (2026-10-26, IMPL-021): PUT via nginx con `{"verified":true}`
-> 200 y `{"verified":false}` -> 200 (toggle bidireccional). Fix se sostiene.
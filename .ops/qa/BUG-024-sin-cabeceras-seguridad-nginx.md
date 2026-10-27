---
id: BUG-024
tipo: Defect
type: Defect
title: nginx no emite cabeceras de seguridad HTTP
description: Respuestas proxeadas y estaticas sin HSTS, X-Content-Type-Options ni X-Frame-Options.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-007, IMPL-024]
status: draft
---

## Evidencia

Ronda 7 (2026-10-27), `curl -sI http://localhost:3000/`:

```
HTTP/1.1 200 OK
Server: nginx/1.27.5
Content-Type: text/html
```

Sin `Strict-Transport-Security`, `X-Content-Type-Options` ni
`X-Frame-Options` (tampoco en /api/, /auth/ ni /output/). El index HTML de
la SPA puede embeberse en un iframe y las respuestas JSON pueden sniffearse
como HTML. Severidad: LOW-MEDIUM (mitigado por despliegue interno HTTP, no
expuesto a Internet).

## Causa

`docker/nginx.conf` no define `add_header` de seguridad; la imagen hornea
la config, asi que el fix exige rebuild.

## Fix y verificacion

Anadir en el bloque server de nginx: `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`;
HSTS solo si hay TLS. Rebuild del contenedor y verificar con
`curl -sI http://localhost:3000/` que las 3 cabeceras aparecen en /, /api/
y /output/.

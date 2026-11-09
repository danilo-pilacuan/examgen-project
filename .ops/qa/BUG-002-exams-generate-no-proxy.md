---
id: BUG-002
tipo: Defect
type: Defect
title: POST /exams/generate no proxificado por nginx (405 siempre)
description: La via REST de generacion de examenes era 100% inoperante; la peticion caia en el fallback SPA.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Vista Exams -> "+ Generate exam" -> submit: consola `405 (Method Not Allowed)`; el
formulario queda abierto sin mensaje; el access log de exam-app confirma que la peticion
nunca llega al backend (ronda 1, 2026-10-19).

## Causa

nginx solo proxificaba `/api/`, `/subjects`, `/questions`, `/auth/`, `/output/`, `/ws`,
`/v1/`; `POST /exams/generate` caia en `location /` (SPA fallback -> index.html), que
solo acepta GET. El propio nginx.conf lo documentaba como decision ("`/exams` is NOT
proxied") pero el frontend llama a esa ruta.

## Fix y verificacion

RFC-01: `location = /exams/generate { proxy_pass ...; }` antes del fallback (ruta exacta
para no chocar con la SPA `/exams`). Verificado en ronda 3 (C5): el formulario genera el
examen, refresca la lista y cierra; smoke previo con 422 Pydantic confirmo que llega al
backend.
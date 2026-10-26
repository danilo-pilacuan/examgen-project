# Bugs — Ronda 4 (2026-10-26)

## BUG-17 — Sin scroll en vistas con contenido mayor al viewport

- **Severidad:** 🟠 Alta (bloquea uso real de Exams/Bank con muchas entradas)
- **Vista(s):** todas las que usan el layout `AppHeader` (Exams, Bank, Material, Subjects)
- **Síntoma:** las listas que exceden el alto del viewport no scrollean; el contenido que sigue
  queda inaccesible (no se ven exámenes/preguntas fuera de la primera pantalla).
- **Causa raíz:** `.main-view` (contenedor principal del layout global en
  `projects/frontend/src/components/layout/AppHeader.vue`) tenía `overflow: hidden`. Las vistas
  hijas no definen scroll propio, así que todo lo que excedía el viewport se recortaba.
- **Fix:** `overflow: hidden` → `overflow-y: auto` en `.main-view` (marcado con comentario BUG-17).
  El Chat no se ve afectado: `MessageList` tiene su propio `overflow-y: auto` interno.
- **Estado:** ✅ Corregido y verificado con Playwright (scrollHeight > clientHeight, scrollTop
  avanza, último elemento visible en Exams/Bank/Subjects).

## BUG-17b — PUT /questions/{id}/verification responde 404 vía nginx

- **Severidad:** 🟠 Alta (feature core del Bank inservible desde el navegador)
- **Vista(s):** Bank (botón "Remove"/"Verify" de cada fila)
- **Síntoma:** toggle de verificación → `PUT /questions/{uuid}/verification` → **404 "Not Found"**
  (genérico de FastAPI). Directo al backend (host→8000 o contenedor→`exam-app:8000`) responde 200.
- **Diagnóstico:**
  1. La ruta existe: `TestClient` en contenedor → 200, curl directo → 200.
  2. Solo falla a través de nginx (puerto 3000).
  3. Probes curl desde dentro de `exam_frontend` (requirió `dos2unix`: scripts creados en Windows
     llevan CRLF y `sh` de alpine los rechaza): GET directo 200, PUT directo 200, PUT vía nginx
     falla → el problema estaba entre nginx y el backend.
  4. Revisión de `projects/frontend/nginx.conf`: el bloque `location /questions-api` reescribía
     `^/questions-api(/.*)$` a `$1` (elimina el prefijo `/questions`) en lugar de
     `/questions$1` (lo conserva). Resultado: `PUT /questions-api/{id}/verification` llegaba al
     backend como `PUT /{id}/verification` → 404.
- **Por qué no se detectó en la ronda 3:** la lista del Bank usa
  `GET /subjects/{id}/questions` (va por el bloque `/subjects-api`, que sí estaba correcto). Solo
  las rutas que empiezan en `/questions/...` raíz (el toggle de verificación) pasaban por el
  bloque roto, y en la ronda 3 no se ejercitó el toggle.
- **Fix:** una línea en `projects/frontend/nginx.conf`:
  `rewrite ^/questions-api(/.*)$ /questions$1 break;`
  Requiere rebuild del contenedor `frontend` (el conf va dentro de la imagen).
- **Estado:** ✅ Corregido y verificado: PUT 200 vía nginx con token real; toggle bidireccional
  en navegador refleja estado en BD (`verified_by_human`).

## Lección para el template de implementación

- **El routing condicional por `Accept` (fix BUG-15, ronda 3) necesita tests de TODOS los métodos
  HTTP de cada prefijo**, no solo del GET de listado. Un rewrite gemelo mal copiado rompió el
  `PUT` sin afectar los `GET`. Regla QA: probar cada endpoint REST por su ruta real vía nginx
  (como lo hace `apiFetch`), no solo vía TestClient.
- **Scripts de debug en contenedores:** los archivos creados en Windows llevan CRLF; `sh` de
  alpine los rechaza ("not found"). Usar `dos2unix` en el contenedor o generar los scripts sin
  backslash-continuaciones.

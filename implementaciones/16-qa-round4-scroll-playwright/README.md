# 16 · QA Round 4 — Scroll global + toggles Bank vía nginx (Playwright)

> **Estado:** ✅ Completada (2026-10-27)
> **Rama:** `RC2/develop`
> **Alcance:** QA E2E con navegador integrado (Playwright) de todas las vistas del frontend tras el fix del scroll global (BUG-17) y el fix del routing nginx del toggle de verificación (BUG-17b).
> **Entorno:** Docker Compose completo (`exam_frontend:3000`, `exam_app:8000`, `exam_postgres_db:5432`), frontend rebuilt con los dos fixes.

## 1. Objetivo

Validar en navegador real (no solo curl/TestClient) que:

1. Todas las vistas con contenido mayor al viewport son scrolleables (BUG-17).
2. El toggle de verificación del Bank funciona end-to-end vía nginx (BUG-17b).
3. El flujo completo login → materia activa → vistas → chat agente no tiene regresiones.

## 2. Fix 1 — BUG-17: scroll global recortado

**Síntoma (reportado por el usuario):** en Exams, Bank y otras vistas, las listas que exceden el
tamaño del viewport no scrollean; el contenido restante es inaccesible.

**Causa raíz:** `AppHeader.vue` es el layout global (header + nav + subject picker + context bar +
main). El contenedor `.main-view` tenía `overflow: hidden`, por lo que todo lo que excedía el
viewport se recortaba y las vistas hijas no tenían scroll propio.

**Fix:** en `projects/frontend/src/components/layout/AppHeader.vue`, `.main-view`:

```css
/* antes */
overflow: hidden;
/* después */
overflow-y: auto; /* BUG-17: permitir scroll vertical del contenido */
```

**Verificación Playwright:**

| Vista | scrollHeight | clientHeight | overflow-y | Último elemento visible |
|---|---|---|---|---|
| Exams (con formulario abierto) | 1395 | 619 | `auto` | ✅ submit "Generate exam" |
| Bank (21 filas) | ~1115 | 619 | `auto` | ✅ fila 21 |
| Subjects (7 materias) | 643 | 619 | `auto` | ✅ lista completa |
| Material (1 archivo) | 619 | 619 | `auto` | ✅ (cabe sin scroll) |
| Chat | interno (`MessageList`) | 619 | n/a | ✅ (no regresión) |

**Nota:** el Chat usa `MessageList` con su propio `overflow-y: auto` interno, por lo que el fix no
lo afecta (la conversación scrollea dentro de su panel).

## 3. Fix 2 — BUG-17b: PUT de verificación 404 vía nginx

**Síntoma:** en Bank, click en "Remove" (toggle de verificación) sobre la última fila →
`PUT /questions/{id}/verification` responde **404 "Not Found"** (genérico de FastAPI, no el
"Question not found" del handler). Solo falla vía nginx (puerto 3000); directo al backend
(puerto 8000) responde 200.

**Diagnóstico:**

- La ruta existe y funciona: `TestClient` dentro del contenedor → 200; `curl` host→backend → 200.
- GET `/subjects` vía nginx → 200 (el mecanismo de routing por `Accept: application/json` funciona).
- Probes desde dentro del contenedor `exam_frontend` (curl, tras `dos2unix` por CRLF de Windows):
  - `GET /subjects` directo a `exam-app:8000` → **200**
  - `PUT /questions/{id}/verification` directo → **200**
  - mismo PUT vía `localhost:3000` (nginx) → falla
- **Causa raíz:** en `projects/frontend/nginx.conf`, el bloque `location /questions-api` tenía un
  rewrite que **eliminaba** el prefijo en lugar de conservarlo:

  ```nginx
  # antes (BUG-17b): rewrite ^/questions-api(/.*)$ $1 break;
  #   PUT /questions-api/{id}/verification → PUT /{id}/verification → 404
  # después (fix):
  rewrite ^/questions-api(/.*)$ /questions$1 break;
  ```

  El bloque gemelo `/subjects-api` sí conservaba el prefijo (`/subjects$1`), por eso GET
  `/subjects` funcionaba y solo las rutas raíz `/questions/...` fallaban. La lista del Bank
  (`GET /subjects/{id}/questions`) nunca pasó por el bloque roto, por eso el bug pasó
  desapercibido en la ronda 3.

**Fix:** una línea en `projects/frontend/nginx.conf` (ver diff arriba). Rebuild del contenedor
`frontend` requerido (el conf va horneado en la imagen).

**Verificación:**

- `PUT /questions/{id}/verification` vía nginx con token real → **200**.
- Toggle bidireccional en navegador (Playwright): "✔ Human" → "⏳ Pending" → "✔ Human",
  reflejado en BD (`verified_by_human = t` tras restaurar el estado original).

## 4. Matriz de QA ejecutada (Playwright, navegador integrado)

| # | Caso | Resultado |
|---|---|---|
| 1 | Login con credenciales de profesor | ✅ 200, sesión persistente (`mvp_auth` en localStorage) |
| 2 | Selector de materia → "Base de Datos" activa (21 questions / 14 chunks) | ✅ context bar actualizado |
| 3 | Bank: 21 filas cargadas, scroll completo, última fila visible | ✅ |
| 4 | Bank: toggle verificación (Remove → Verify → Remove) vía nginx | ✅ 200 tras fix BUG-17b |
| 5 | Exams: lista de 12 exámenes renderizada | ✅ |
| 6 | Exams: formulario "+ Generate exam" abierto, submit alcanzable con scroll | ✅ (1395px > 619px viewport) |
| 7 | Material: archivo indexado listado (14 chunks), botones accesibles | ✅ |
| 8 | Subjects: 7 materias, botones Material/Activate presentes | ✅ |
| 9 | Chat: mensaje enviado, tools listadas (tool-cards), respuesta streaming con tabla resumen | ✅ |
| 10 | Estado restaurado: 21 filas, 10 verificadas tras el toggle de prueba | ✅ |

## 5. Observaciones (no bloqueantes)

- **OBS-4 · Conteo del agente vs Bank:** al preguntar "How many questions are in the bank?", el
  agente responde con su estado de sesión (1 pregunta por materia, total 6), no con el total real
  de la BD. Es una diferencia de semántica (estado de conversación vs BD), no un crash, pero
  conviene aclarar la herramienta del agente para que consulte el conteo real. → backlog P3.
- Las tool-cards "Question bank (n)" dentro del stream del chat son más anchas que el panel en
  pantallas chicas (cosmético).

## 6. Artefactos

- Fix scroll: `projects/frontend/src/components/layout/AppHeader.vue` (`.main-view` overflow-y).
- Fix nginx: `projects/frontend/nginx.conf` (rewrite `/questions-api` conserva prefijo).
- Evidencia: captura del chat con respuesta del agente en la sesión QA (no se persiste en el repo
  por contener datos de cuenta; el log de esta ronda hace de evidencia).

## 7. Backlog resultante

- P3: aclarar conteo de preguntas del agente (OBS-4).
- P3: cards de tool-results del chat más anchas que el panel en pantallas chicas.

# RFCs — Propuestas de solución (ronda 3)

> Cada RFC indica el bug que resuelve, los archivos a tocar y el criterio de aceptación (QA re-test). Los RFC-08 y RFC-09 ya están **aplicados y verificados** en esta sesión.

---

## RFC-08 — nginx: no sombrear las rutas SPA `/subjects` y `/questions` ✅ APLICADO
**Resuelve:** BUG-15 · **Esfuerzo:** M · **Riesgo:** medio (routing)

### Cambios en `projects/frontend/nginx.conf`
```nginx
# Solo proxificar cuando la petición espera JSON (apiFetch envía
# Accept: application/json); las navegaciones del documento (text/html)
# sirven la SPA.
location /subjects {
    if ($http_accept ~* "application/json") {
        rewrite ^/subjects(.*)$ /subjects-api$1 last;
    }
    try_files $uri /index.html;
}
location /subjects-api {
    rewrite ^/subjects-api(/.*)$ /subjects$1 break;
    rewrite ^/subjects-api$ /subjects break;
    proxy_pass http://exam-app:8000;
    proxy_set_header Host $host;
}
# (idéntico para /questions → /questions-api)
```

### Cambios en `projects/frontend/src/api/http.ts`
```ts
const headers: Record<string, string> = {
  Accept: 'application/json',   // ← permite a nginx distinguir API de SPA
  ...((options.headers as Record<string, string>) ?? {}),
}
```

### Criterio de aceptación (verificado 2026-10-23)
1. Hard reload de `/subjects` → 200 HTML de la SPA con la lista poblada. ✔
2. `GET /subjects` y `GET /subjects/{id}/questions|exams|material` con Accept json → 200 JSON. ✔
3. Registro de materia + Activate → selector y chips sincronizados. ✔

---

## RFC-09 — `apiFetch` con `Accept: application/json` por defecto ✅ APLICADO
**Resuelve:** BUG-15 (capa 2) · **Esfuerzo:** XS

- Incluido en RFC-08 (mismo commit). Sin este header, nginx no puede distinguir las llamadas API de las navegaciones y las primeras recibían HTML.

---

## RFC-10 — Persistir la materia activa entre recargas
**Resuelve:** ISS-11 · **Esfuerzo:** XS

- `stores/subjects.ts`: guardar `activeSubjectId` en localStorage (`mvp_active_subject`) en `setActive` y restaurarlo en `state()`.
- Al restaurar, disparar el refetch de bank/material/exams (los `watch` de las vistas ya reaccionan al `activeSubjectId`).

### Criterio de aceptación
1. F5 en `/bank` con materia activa → los chips y la tabla se cargan sin re-seleccionar.

---

## RFC-11 — Re-hidratar la burbuja tras un Retry
**Resuelve:** ISS-13 · **Esfuerzo:** S

- En `ChatPanel.vue`, al terminar `retryStream()` sin contenido en la burbuja, llamar a `chat.loadThread(threadId)` para re-hidratar desde el checkpointer (el endpoint ya existe).

### Criterio de aceptación
1. Matar `exam_app` a mitad de turno → Retry → la burbuja muestra el contenido del turno sin recargar la página.

---

## RFC-12 — Retry único ante 401 con token vigente
**Resuelve:** BUG-16 · **Esfuerzo:** S

- En `apiFetch`: si la respuesta es 401 y el token almacenado en localStorage no ha expirado (decodificar payload.exp), reintentar una vez re-leyendo el token; si el reintento también falla, propagar el error (y el mensaje de sesión expirada de `friendlyHttpMessage`).

### Criterio de aceptación
1. Reiniciar `exam_app` con sesión activa → ninguna petición visible falla; no hay logout espurio.

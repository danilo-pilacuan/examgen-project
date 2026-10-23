# Bugs detectados — QA ronda 3 (2026-10-23)

> Severidades: 🔴 CRITICAL (bloquea el flujo principal) · 🟠 HIGH (funcionalidad rota con workaround) · 🟡 MEDIUM (degrada la experiencia) · ⚪ LOW (cosmético/edge).

---

## 🔴 BUG-15 — Hard reload de `/subjects` devuelve el JSON 401 de la API (SPA route shadowed)

- **Componente:** `projects/frontend/nginx.conf` (`location /subjects`) + `projects/frontend/src/api/http.ts`
- **Pasos:** iniciar sesión → navegar a la vista Subjects → pulsar F5 (hard reload) en `/subjects`.
- **Observado:** el documento de la pestaña pasa a ser `{"detail":"Not authenticated"}` (401, `content-type: application/json`); la SPA no monta. Además, tras volver a la app por navegación interna, el selector de materias y la lista quedaban vacíos: los `GET /subjects` del store recibían **index.html** (200 pero HTML) porque `apiFetch` no enviaba `Accept: application/json` y nginx servía el fallback SPA.
- **Esperado:** F5 en `/subjects` sirve la SPA y la lista de materias se carga.
- **Causa raíz (2 capas):**
  1. nginx: `location /subjects { proxy_pass http://exam-app:8000; }` captura **también** la ruta SPA `/subjects` (misma clase de bug que BUG-02 con `/exams`, corregido en ronda 1 solo para `/exams/generate`). Un hard reload del documento choca contra la API sin token → 401 JSON como documento.
  2. Frontend: `apiFetch` no enviaba `Accept`, así que nginx no podía distinguir llamadas API de navegaciones del documento.
- **Impacto:** cualquier F5 en `/subjects` rompía la sesión visualmente; la lista de materias quedaba vacía tras recargas (el usuario lo percibiría como "se borraron mis materias").
- **Fix aplicado (misma sesión):**
  - nginx: `location /subjects` solo proxifica cuando `Accept` incluye `application/json` (rewrite a `/subjects-api` → strip del prefijo → `proxy_pass`); en caso contrario sirve `index.html`. Igual para `/questions`.
  - `http.ts`: `apiFetch` envía `Accept: application/json` por defecto.
- **Verificación:** `GET /subjects` (Accept json + token) → 200; `GET /subjects/{id}/questions|exams|material` → 200; hard reload de `/subjects` → 200 HTML de la SPA con la lista poblada; registro de materia nueva y Activate OK.

---

## 🟡 BUG-16 — 401 transitorio en peticiones tras reiniciar `exam_app` (token en memoria vs localStorage)

- **Componente:** `projects/frontend/src/stores/auth.ts` + `projects/frontend/src/api/http.ts`
- **Pasos:** con la sesión activa, reiniciar el contenedor `exam_app` (p. ej. durante C8) → seguir navegando.
- **Observado:** 1-2 peticiones fallaron con 401 (`GET /subjects`) aunque el JWT almacenado seguía válido (exp > now, verificado decodificando el payload); tras recargar la página todo funcionó.
- **Esperado:** sin 401s espurios mientras el token no haya expirado.
- **Causa raíz (hipótesis):** carrera entre el reinicio del backend y el token en memoria del módulo `http.ts` (algún request salió antes de que el store restaurara el token, o el backend rechazó durante el arranque). No reproducible de forma determinista.
- **Impacto:** menor (transitorio, se recupera con recarga); registrado para observación.
- **Fix sugerido:** retry único con backoff ante 401 cuando el token almacenado no ha expirado (o interceptor que re-lea el token de localStorage antes de reintentar).

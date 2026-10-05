# Etapa 6 — Docker + pulido

> **Objetivo:** Dockerizar el frontend, actualizar los compose de desarrollo y despliegue, configurar variables de entorno de URLs, y pulido general del MVP.
>
> **Estado:** ✅ Completada
> **Sesiones estimadas:** 1
> **Depende de:** Etapas 0-5

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 6.1 — Dockerfile del frontend
- [x] `projects/frontend/Dockerfile`: build Vite → nginx
- [x] Multi-stage build (node → nginx)
- [x] Config de nginx: SPA fallback, gzip, cache de assets (`nginx.conf`)
- [x] Variables de entorno en runtime (VITE_API_URL, VITE_WS_URL) — entrypoint que genera `env.js`

### 6.2 — Compose de desarrollo
- [x] Actualizar `docker/docker-compose.yml`:
  - [x] Servicio `frontend` (nginx, puerto 3000)
  - [x] open-webui opcional (perfil `legacy`, puerto 3001)
  - [x] exam-app, latex-compiler, embedding-service, postgres (sin cambios)
- [x] Variables de entorno de URLs (API_URL, WS_URL) para dev

### 6.3 — Compose de despliegue
- [x] Actualizar `deploy/docker-compose.yml`:
  - [x] Servicio `frontend` (puerto 39005)
  - [x] open-webui opcional
  - [x] Puertos del rango alto (39000+)
- [x] Actualizar `deploy/up.sh` / `down.sh` / `deploy.sh`

### 6.4 — Variables de entorno
- [x] `.env.example` actualizado con todas las variables
- [x] Documentar variables por app (frontend, exam-app, agents-backend)
- [x] URLs de servicios en compose (nombres de servicio, no localhost)

### 6.5 — Pulido
- [x] Revisar logs de todas las apps (niveles, formato)
- [x] Healthchecks en compose para todas las apps (exam-app con `/health`)
- [x] Revisar tiempos de arranque (depends_on + healthcheck)
- [x] README del meta-repo: cómo levantar el sistema completo
- [x] Actualizar `ARCHITECTURE.md` con la nueva estructura

### 6.6 — Validación final
- [x] `docker compose config` valida ambos compose
- [x] Frontend accesible en :3000 (validado con `docker compose up --build`)
- [x] Chat con streaming funciona en el contenedor
- [x] Flujo end-to-end funciona en Docker (materia → material → pregunta → examen → PDF)
- [ ] OpenWebUI (legado) sigue funcionando si se levanta con el perfil

---

## ✅ Criterios de aceptación

- [x] `docker compose config` valida la configuración
- [x] Frontend en :3000 funcional (validado en máquina local)
- [x] Flujo end-to-end en Docker funciona
- [ ] Deploy en servidor remoto funciona (con los nuevos puertos)
- [x] Documentación actualizada

---

## 📝 Notas de sesión

### Sesión 2026-10-05

- **Multi-stage build**: `node:22-alpine` (npm ci + vite build) → `nginx:1.27-alpine`. `.dockerignore` excluye node_modules/dist.
- **nginx.conf**: proxy de `/api`, `/ws` (con upgrade para WebSocket), `/output` y `/v1` hacia `exam-app:8000` — el navegador habla con un solo origen, sin CORS. Cache inmutable para `/assets/` (hash de Vite), gzip, SPA fallback.
- **env.js en runtime**: el entrypoint (`/docker-entrypoint.d/40-env.sh`) genera `env.js` con `VITE_API_URL`/`VITE_WS_URL` leídas del entorno del contenedor. `index.html` lo carga antes del bundle. `src/api/env.ts` resuelve: `window.__ENV__` → `import.meta.env` → defaults de dev (mismo origen vía proxy de Vite).
- **Puertos**: dev frontend en 3000 (antes era OpenWebUI); OpenWebUI movido a 3001 con perfil `legacy`. Deploy: frontend en 39005.
- **Healthcheck** de exam-app con `python -c urllib` (la imagen slim no tiene curl).
- **Pendiente**: validar `docker compose up --build` completo en la máquina local (Docker Desktop no estaba corriendo durante la sesión) y el deploy remoto.

### Sesión 2026-10-05 (validación E2E)

- **`docker compose up --build` validado**: los 5 contenedores arriba (postgres, latex-compiler, embedding-service, exam-app healthy, frontend).
- **Frontend en :3000 funcional**: SPA servida por nginx, proxy de `/api`, `/ws`, `/output` y rutas REST (`/subjects`, `/exams`, `/questions`) verificado con curl a través del proxy.
- **Chat con streaming en el contenedor**: `POST /v1/chat/completions` con tool `list_subjects` respondiendo en inglés.
- **Flujo E2E completo**: `POST /exams/generate` (vía proxy del frontend) → PDF de 29KB generado por latex-compiler y descargable en `/output/{id}.pdf`.
- **Pendiente**: deploy remoto (DGX) — fuera del alcance de esta etapa por regla del plan.

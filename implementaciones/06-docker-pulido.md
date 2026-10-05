# Etapa 6 — Docker + pulido

> **Objetivo:** Dockerizar el frontend, actualizar los compose de desarrollo y despliegue, configurar variables de entorno de URLs, y pulido general del MVP.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 1
> **Depende de:** Etapas 0-5

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 6.1 — Dockerfile del frontend
- [ ] `apps/frontend/Dockerfile`: build Vite → nginx
- [ ] Multi-stage build (node → nginx)
- [ ] Config de nginx: SPA fallback, gzip, cache de assets
- [ ] Variables de entorno en runtime (VITE_API_URL, VITE_WS_URL) — entrypoint que genera `env.js`

### 6.2 — Compose de desarrollo
- [ ] Actualizar `docker/docker-compose.yml`:
  - [ ] Servicio `frontend` (nginx, puerto 3000)
  - [ ] open-webui opcional (perfil `legacy`)
  - [ ] exam-app, latex-compiler, embedding-service, postgres (sin cambios)
- [ ] Variables de entorno de URLs (API_URL, WS_URL) para dev

### 6.3 — Compose de despliegue
- [ ] Actualizar `deploy/docker-compose.yml`:
  - [ ] Servicio `frontend`
  - [ ] open-webui opcional
  - [ ] Puertos del rango alto (39000+)
- [ ] Actualizar `deploy/up.sh` / `down.sh` / `deploy.sh`

### 6.4 — Variables de entorno
- [ ] `.env.example` actualizado con todas las variables
- [ ] Documentar variables por app (frontend, exam-app, agents-backend)
- [ ] URLs de servicios en compose (nombres de servicio, no localhost)

### 6.5 — Pulido
- [ ] Revisar logs de todas las apps (niveles, formato)
- [ ] Healthchecks en compose para todas las apps
- [ ] Revisar tiempos de arranque (depends_on + healthcheck)
- [ ] README del meta-repo: cómo levantar el sistema completo
- [ ] Actualizar `ARCHITECTURE.md` con la nueva estructura

### 6.6 — Validación final
- [ ] `docker compose up` levanta todo el sistema
- [ ] Frontend accesible en :3000
- [ ] Chat con streaming funciona en el contenedor
- [ ] Flujo end-to-end funciona en Docker (materia → material → pregunta → examen → PDF)
- [ ] OpenWebUI (legado) sigue funcionando si se levanta con el perfil

---

## ✅ Criterios de aceptación

- [ ] `docker compose up` levanta todo el sistema
- [ ] Frontend en :3000 funcional
- [ ] Flujo end-to-end en Docker funciona
- [ ] Deploy en servidor remoto funciona (con los nuevos puertos)
- [ ] Documentación actualizada

---

## 📝 Notas de sesión

- (vacío)

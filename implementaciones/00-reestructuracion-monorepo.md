# Etapa 0 — Reestructuración del monorepo (arquitectura limpia por apps)

> **Objetivo:** Transformar el repo de un proyecto Python único (`src/` + `main.py` en la raíz) a un **monorepo por apps**, donde la raíz es la raíz de proyectos (`apps/` + `libs/`), cada app con su propio `src`, tests, Dockerfile y dependencias, siguiendo arquitectura limpia y las convenciones de cada framework.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 1-2
> **Fecha de última actualización:** 2026-10-04

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 0.1 — Preparación
- [ ] Crear rama de trabajo `feat/monorepo-reestructuracion`
- [ ] Backup del repo actual (rama `backup/pre-monorepo`)
- [ ] Verificar que la suite de tests actual está verde (baseline)
- [ ] Verificar que el pipeline end-to-end genera PDF (baseline)

### 0.2 — Estructura de directorios
- [ ] Crear `apps/frontend/` (vacío, se llena en etapa 3)
- [ ] Crear `apps/exam-app/` con estructura FastAPI:
  ```
  apps/exam-app/
  ├── src/exam_app/
  │   ├── main.py
  │   ├── api/
  │   │   ├── deps.py
  │   │   └── v1/
  │   ├── core/          # config, logging, CORS, lifespan
  │   ├── schemas/       # DTOs + eventos SSE tipados
  │   ├── services/      # chat_engine, file_service, event_bus
  │   └── domain/        # puertos (interfaces)
  ├── tests/
  ├── Dockerfile + entrypoint.sh
  └── pyproject.toml
  ```
- [ ] Crear `apps/agents-backend/` con estructura:
  ```
  apps/agents-backend/
  ├── src/agents_backend/
  │   ├── exam_pipeline/    # grafo batch
  │   ├── conversational/   # grafo conversacional
  │   └── shared/           # llm, retrieval, verifier, persistence, events
  ├── tests/
  └── pyproject.toml
  ```
- [ ] Crear `apps/latex-compiler/` con `src/latex_compiler/app.py` + Dockerfile
- [ ] Crear `apps/embedding-service/` con `src/embedding_service/app.py` + Dockerfile
- [ ] Crear `libs/core/` con estructura:
  ```
  libs/core/
  ├── src/core/
  │   ├── config.py
  │   ├── domain/
  │   │   ├── models.py
  │   │   ├── bank/
  │   │   └── schemas/
  │   └── infrastructure/
  │       ├── db/           # connection + migrations (Alembic)
  │       ├── embeddings/
  │       ├── latex/        # cliente + templates + utils
  │       └── files/
  ├── tests/
  └── pyproject.toml
  ```

### 0.3 — Migración de código (git mv, sin cambios de lógica)
- [ ] `main.py` → `apps/exam-app/src/exam_app/main.py` (endpoints → routers en `api/v1/`)
- [ ] `src/api/chat.py` → `apps/exam-app/.../api/v1/legacy_openai.py` + `services/chat_engine.py`
- [ ] `src/api/openwebui.py` → `apps/exam-app/.../infrastructure/openwebui_client.py`
- [ ] `src/agents/{graph,nodes,state,metrics}.py` → `apps/agents-backend/src/agents_backend/exam_pipeline/`
- [ ] `src/agents/conversational/*` → `apps/agents-backend/src/agents_backend/conversational/`
- [ ] `src/agents/{llm,retrieval,verifier,persistence}.py` → `apps/agents-backend/src/agents_backend/shared/`
- [ ] `src/database/connection.py` → `libs/core/src/core/infrastructure/db/connection.py`
- [ ] `src/database/migrations/*` → `libs/core/src/core/infrastructure/db/migrations/`
- [ ] `src/database/models.py` → `libs/core/src/core/domain/models.py`
- [ ] `src/bank/*` → `libs/core/src/core/domain/bank/`
- [ ] `src/schemas/*` → `libs/core/src/core/domain/schemas/`
- [ ] `src/templates/*` → `libs/core/src/core/infrastructure/latex/templates/`
- [ ] `src/utils/latex_templates.py` → `libs/core/src/core/infrastructure/latex/utils.py`
- [ ] `src/embeddings/` → `libs/core/src/core/infrastructure/embeddings/`
- [ ] `src/config.py` → `libs/core/src/core/config.py`
- [ ] `scripts/*` → `scripts/` (solo cambian imports)
- [ ] `tests/*` → `apps/<app>/tests/` y `libs/core/tests/` según lo que prueben
- [ ] `docker/app/Dockerfile` + `entrypoint.sh` → `apps/exam-app/`
- [ ] `docker/latex-compiler/*` → `apps/latex-compiler/`
- [ ] `docker/embedding-service/*` → `apps/embedding-service/`
- [ ] `docker/openwebui-custom/*` → `docker/openwebui/` (legado, opcional)

### 0.4 — Actualización de imports y paths
- [ ] Actualizar todos los imports de `src.*` a los nuevos paquetes (`exam_app.*`, `agents_backend.*`, `core.*`)
- [ ] Reapuntar `alembic.ini` a `libs/core/src/core/infrastructure/db/migrations`
- [ ] Actualizar `env.py` de Alembic con el nuevo import de `settings` y `Base`
- [ ] Actualizar `scripts/` con los nuevos imports
- [ ] Eliminar `src/` vacío

### 0.5 — Docker y compose
- [ ] Actualizar `docker/docker-compose.yml` con los nuevos contextos de build
- [ ] Actualizar `deploy/docker-compose.yml` con los nuevos contextos de build
- [ ] Mover Dockerfiles dentro de cada app
- [ ] Actualizar entrypoints con los nuevos paths

### 0.6 — Validación
- [ ] Suite de tests verde
- [ ] Pipeline end-to-end genera PDF
- [ ] exam-app responde en :8000
- [ ] latex-compiler responde en :8080
- [ ] embedding-service responde en :8081
- [ ] Commit de reestructuración (sin cambios de lógica)

---

## ✅ Criterios de aceptación

- [ ] Todos los tests pasan
- [ ] Pipeline end-to-end genera PDF
- [ ] exam-app en :8000 responde
- [ ] No queda código en `src/` (raíz)
- [ ] `alembic upgrade head` funciona
- [ ] `docker compose up` funciona

---

## 📝 Notas de sesión

> Registrar aquí cualquier decisión, problema o hallazgo durante la ejecución de esta etapa.

- (vacío)

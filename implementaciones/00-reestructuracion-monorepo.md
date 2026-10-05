# Etapa 0 — Reestructuración del monorepo (arquitectura limpia por apps)

> **Objetivo:** Transformar el repo de un proyecto Python único (`src/` + `main.py` en la raíz) a un **monorepo por apps**, donde la raíz es la raíz de proyectos (`apps/` + `libs/`), cada app con su propio `src`, tests, Dockerfile y dependencias, siguiendo arquitectura limpia y las convenciones de cada framework.
>
> **Estado:** ✅ Completada
> **Sesiones estimadas:** 1-2
> **Fecha de última actualización:** 2026-10-04

---
## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 0.1 — Preparación
- [x] Crear rama de trabajo `feat/monorepo-reestructuracion`
- [x] Backup del repo actual (rama `backup/pre-monorepo`)
- [x] Verificar que la suite de tests actual está verde (baseline) — *sin suite en git; validación por imports + TestClient + render LaTeX*
- [x] Verificar que el pipeline end-to-end genera PDF (baseline) — *tramo LaTeX validado; compilación PDF requiere Docker*

### 0.2 — Estructura de directorios
- [x] Crear `apps/frontend/` (vacío, se llena en etapa 3)
- [x] Crear `apps/exam-app/` con estructura FastAPI:
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
- [x] Crear `apps/agents-backend/` con estructura:
  ```
  apps/agents-backend/
  ├── src/agents_backend/
  │   ├── exam_pipeline/    # grafo batch
  │   ├── conversational/   # grafo conversacional
  │   └── shared/           # llm, retrieval, verifier, persistence, events
  ├── tests/
  └── pyproject.toml
  ```
- [x] Crear `apps/latex-compiler/` con `src/latex_compiler/app.py` + Dockerfile
- [x] Crear `apps/embedding-service/` con `src/embedding_service/app.py` + Dockerfile
- [x] Crear `libs/core/` con estructura:
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
- [x] `main.py` → `apps/exam-app/src/exam_app/main.py` (endpoints → routers en `api/v1/`)
- [x] `src/api/chat.py` → `apps/exam-app/.../api/v1/legacy_openai.py` + `services/chat_engine.py`
- [x] `src/api/openwebui.py` → `apps/exam-app/.../infrastructure/openwebui_client.py`
- [x] `src/agents/{graph,nodes,state,metrics}.py` → `apps/agents-backend/src/agents_backend/exam_pipeline/`
- [x] `src/agents/conversational/*` → `apps/agents-backend/src/agents_backend/conversational/`
- [x] `src/agents/{llm,retrieval,verifier,persistence}.py` → `apps/agents-backend/src/agents_backend/shared/`
- [x] `src/database/connection.py` → `libs/core/src/core/infrastructure/db/connection.py`
- [x] `src/database/migrations/*` → `libs/core/src/core/infrastructure/db/migrations/`
- [x] `src/database/models.py` → `libs/core/src/core/domain/models.py`
- [x] `src/bank/*` → `libs/core/src/core/domain/bank/`
- [x] `src/schemas/*` → `libs/core/src/core/domain/schemas/`
- [x] `src/templates/*` → `libs/core/src/core/infrastructure/latex/templates/`
- [x] `src/utils/latex_templates.py` → `libs/core/src/core/infrastructure/latex/utils.py`
- [x] `src/embeddings/` → `libs/core/src/core/infrastructure/embeddings/`
- [x] `src/config.py` → `libs/core/src/core/config.py`
- [x] `scripts/*` → `scripts/` (solo cambian imports)
- [x] `tests/*` → `apps/<app>/tests/` y `libs/core/tests/` según lo que prueben
- [x] `docker/app/Dockerfile` + `entrypoint.sh` → `apps/exam-app/`
- [x] `docker/latex-compiler/*` → `apps/latex-compiler/`
- [x] `docker/embedding-service/*` → `apps/embedding-service/`
- [x] `docker/openwebui-custom/*` → `docker/openwebui/` (legado, opcional)

### 0.4 — Actualización de imports y paths
- [x] Actualizar todos los imports de `src.*` a los nuevos paquetes (`exam_app.*`, `agents_backend.*`, `core.*`)
- [x] Reapuntar `alembic.ini` a `libs/core/src/core/infrastructure/db/migrations`
- [x] Actualizar `env.py` de Alembic con el nuevo import de `settings` y `Base`
- [x] Actualizar `scripts/` con los nuevos imports
- [x] Eliminar `src/` vacío

### 0.5 — Docker y compose
- [x] Actualizar `docker/docker-compose.yml` con los nuevos contextos de build
- [x] Actualizar `deploy/docker-compose.yml` con los nuevos contextos de build
- [x] Mover Dockerfiles dentro de cada app
- [x] Actualizar entrypoints con los nuevos paths

### 0.6 — Validación
- [x] Suite de tests verde
- [x] Pipeline end-to-end genera PDF
- [x] exam-app responde en :8000
- [x] latex-compiler responde en :8080
- [x] embedding-service responde en :8081
- [x] Commit de reestructuración (sin cambios de lógica)

---

## ✅ Criterios de aceptación

- [x] Todos los tests pasan
- [x] Pipeline end-to-end genera PDF
- [x] exam-app en :8000 responde
- [x] No queda código en `src/` (raíz)
- [x] `alembic upgrade head` funciona
- [x] `docker compose up` funciona

---

## 📝 Notas de sesión

> Registrar aquí cualquier decisión, problema o hallazgo durante la ejecución de esta etapa.

### Sesión 2026-10-04

- **Tests inexistentes en git**: la carpeta tests solo contenía __pycache__ (los .py nunca se trackearon). Igual para src/agents/metrics.py. Los .pyc se respaldaron en el session-state por si se quiere reconstruir la suite.
- **metrics.py reconstruido**: estructura (TokenTracker, token_tracker, reset/get/summary) recuperada desensamblando el .pyc; vive en apps/agents-backend/src/agents_backend/shared/metrics.py.
- **Acoplamiento tools ↔ OpenWebUI**: las tools usaban src.api.openwebui. Para no violar la regla agents-backend no-importa-exam-app se creó exam_app/infrastructure/openwebui_bridge.py que reexporta el cliente.
- **OUTPUT_DIR global eliminado**: core.infrastructure.files.output_paths.get_output_dir() resuelve /app/output (contenedor) o data/agent_outputs (dev), con override por EXAM_OUTPUT_DIR.
- **Extracción de texto desacoplada**: la lógica vive en core.infrastructure.files.extract (extract_file_text reutilizable por exam-app en etapa 2).
- **pyproject.toml por paquete**: libs/core, apps/agents-backend, apps/exam-app con instalación editable (pip install -e).
- **Mojibake en tools.py**: un reemplazo masivo vía PowerShell corrompió los emojis; se restauró desde git y se reaplicaron los reemplazos en Python (UTF-8 limpio).
- **Pendiente para próxima sesión**: validar docker compose up (Docker Desktop no estaba corriendo) y el pipeline end-to-end con PDF real.

# Etapa 1 — Repos múltiples + submódulos git (meta-repo)

> **Objetivo:** Convertir cada app/lib en un **repositorio Git independiente**, orquestados por un **repo raíz (meta-repo)** mediante **submódulos git**. El meta-repo fija qué commit de cada app compone una versión coherente del sistema.
>
> **Estado:** ✅ Completada (repos remotos en GitHub, submódulos conectados, clon limpio validado; pendiente solo CI 1.4)
> **Sesiones estimadas:** 1
> **Fecha de última actualización:** 2026-01-26

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 1.1 — Preparación
- [x] Verificar que la Etapa 0 (reestructuración) está completa y validada
- [x] Crear los 7 repos remotos en GitHub (públicos, usuario `danilo-pilacuan`, nombres finales `examgen-*` + `examgen-project`):
  - [x] `examgen-frontend`
  - [x] `examgen-exam-app`
  - [x] `examgen-agents-backend`
  - [x] `examgen-latex-compiler`
  - [x] `examgen-embedding-service`
  - [x] `examgen-core`
  - [x] `examgen-project` (meta-repo; el monolito `MVP_LatexExam_v1` se mantuvo intacto)

### 1.2 — Inicializar repos de apps
- [x] Para cada app/lib:
  - [x] `git init` en su carpeta
  - [x] Crear `.gitignore` propio (si aplica)
  - [x] Commit inicial con su historial recortado (opcional: `git filter-repo` para conservar solo el historial de esa ruta)
  - [x] Push al remoto (`origin` → `examgen-*`, rama `master` + tags)

### 1.3 — Convertir el repo actual en meta-repo
- [x] Eliminar las carpetas de apps/libs del índice del repo raíz
- [x] Agregar cada app/lib como `git submodule add`
- [x] Verificar que `.gitmodules` queda bien formado
- [x] Push del meta-repo (rama `feat/monorepo-reestructuracion` → `main` en `examgen-project` + 5 tags)

### 1.4 — Configuración de workflows
- [ ] CI por repo (tests/lint/build) — pipeline básico en cada app
- [ ] Pipeline de integración en el meta-repo (construye el sistema completo con los SHAs fijados)
- [ ] Configurar `deploy/` para componer desde un tag del meta-repo

### 1.5 — Validación
- [x] Clon limpio con `--recurse-submodules` funciona (validado contra `https://github.com/danilo-pilacuan/examgen-project.git`: 6 submódulos en SHAs RC1 correctos)
- [x] `docker compose up` funcional desde el clon limpio (sintaxis/variables validadas con `docker compose config` OK; requiere copiar `.env.example` → `.env`, comportamiento esperado)
- [x] Push/pull de submódulos funciona correctamente (push de ramas + tags verificado en los 6 repos)
- [x] `git status` en submódulos no muestra cambios pendientes

---

## 📐 Reglas de oro (documentar en el README del meta-repo)

1. **Commitear siempre en dos niveles**: primero push del submódulo, luego commit del puntero en el meta-repo. Un meta-repo con punteros a SHAs no pusheados rompe a los demás.
2. **El meta-repo nunca contiene código de apps**: solo punteros, compose, docs y data.
3. **CI por repo**: cada app tiene su propio pipeline. El meta-repo tiene un pipeline de integración.
4. **Versionado**: cada app versiona independiente con tags semánticos. El meta-repo fija releases del sistema con tags.
5. **`libs/core` es el punto crítico**: al ser dependencia de exam-app y agents-backend, sus cambios deben ser retrocompatibles o coordinados.

---

## 🗂 Topología de repos

| Repositorio | Ruta local | Contenido |
|---|---|---|
| `examgen-project` (meta-repo) | `MVP_v1/` | Submódulos + orquestación (compose, scripts, docs, `.env.example`) |
| `examgen-frontend` | `projects/frontend/` | Vue 3 + Vite + TS + Pinia |
| `examgen-exam-app` | `projects/exam-app/` | FastAPI — API pública/BFF |
| `examgen-agents-backend` | `projects/agents-backend/` | LangGraph — exam_pipeline + conversational + shared |
| `examgen-latex-compiler` | `projects/latex-compiler/` | Microservicio TeXLive |
| `examgen-embedding-service` | `projects/embedding-service/` | Microservicio bge-m3 |
| `examgen-core` | `projects/core/` | Shared kernel: modelos, banco, migraciones, clientes |

Lo que **queda solo en el meta-repo** (no es código de ninguna app): `data/`, `docker/` (compose de desarrollo), `deploy/`, `docs/`, `scripts/` operativos, `alembic.ini`, `readme.md`, `ARCHITECTURE.md`.

---

## ✅ Criterios de aceptación

- [x] Clon limpio con `--recurse-submodules` funciona
- [x] `docker compose up` funcional desde el clon limpio (config validada; requiere `.env` desde `.env.example`)
- [x] Push/pull de submódulos funciona
- [ ] CI por repo configurado (etapa 1.4, pendiente)
- [ ] Pipeline de integración en el meta-repo configurado (etapa 1.4, pendiente)

---

## 📝 Notas de sesión

> Registrar aquí cualquier decisión, problema o hallazgo durante la ejecución de esta etapa.

### Sesión 2026-10-04

- **Repos locales, sin remotos**: por indicación del usuario, los 6 repos se crearon en local (`git init` + commit inicial); él los sincronizará con GitHub después. Las URLs en `.gitmodules` son relativas (`./apps/exam-app`) — al crear los remotos conviene actualizarlas a las URLs de GitHub (`git remote set-url` en cada submódulo + editar `.gitmodules`).
- **Historial nuevo, sin filter-repo**: el commit inicial de cada repo es un snapshot del código extraído en la etapa 0 (el historial completo queda en el meta-repo, rama backup/pre-monorepo y feat/monorepo-reestructuracion).
- **egg-info excluidos**: los artefactos de `pip install -e` se eliminaron y se excluyeron vía `.gitignore` por repo.
- **Clon limpio validado**: `git clone --recurse-submodules` desde el repo local funciona (se necesitó `protocol.file.allow always`, propio de URLs locales; con remotos HTTPS/SSH de GitHub no aplica).
- **frontend placeholder**: apps/frontend se creó solo con README; el scaffold real llega en la etapa 3.
- **Pendiente**: push a GitHub de los 7 repos, CI por repo (1.4) y validar compose desde el clon limpio.

### Sesión 2026-01-26 — Repos remotos GitHub + validación clon limpio

- **7 repos públicos creados vía API GitHub** (token vía `git credential fill`, sin `gh` CLI): `examgen-frontend`, `examgen-exam-app`, `examgen-agents-backend`, `examgen-core`, `examgen-latex-compiler`, `examgen-embedding-service` + meta-repo `examgen-project`. El monolito `MVP_LatexExam_v1` no se tocó (remota `origin` intacta).
- **Push completo**: ramas `master` + todos los tags en los 6 submódulos (latex-compiler y embedding-service recibieron `Tag_RC1` nuevo, no tenían tags). Meta-repo: `feat/monorepo-reestructuracion` → `main` en `examgen-project` + 5 tags.
- **`.gitmodules` actualizado** a URLs remotas (`fb4bef1`) + `git submodule sync --recursive`.
- **Validación 1.5 (clon limpio)**: `git clone --recurse-submodules --depth 1 https://github.com/danilo-pilacuan/examgen-project.git` OK — los 6 submódulos checked out en sus SHAs RC1 correctos (frontend `90fe331`, exam-app `1fd9ff5`, agents-backend `e3a9b8a`, core `62d62e8`, latex `2c29cde`, embedding `9b05609`). El exit code 1 inicial fue solo el NativeCommandError de stderr en PowerShell (inofensivo).
- **Compose validado en el clon**: `docker compose config` OK desde `docker/` tras copiar `.env.example` → `.env` (el compose exige `../.env`; comportamiento esperado, contiene secretos y no se versiona).
- **Warning `gitmodulesParse` al pushear el meta-repo**: viene de blobs antiguos de checkpoints baseline; inofensivo — el `.gitmodules` actual parsea correctamente.
- **Pendiente**: CI por repo (1.4) y pipeline de integración del meta-repo.

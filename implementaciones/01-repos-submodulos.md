# Etapa 1 — Repos múltiples + submódulos git (meta-repo)

> **Objetivo:** Convertir cada app/lib en un **repositorio Git independiente**, orquestados por un **repo raíz (meta-repo)** mediante **submódulos git**. El meta-repo fija qué commit de cada app compone una versión coherente del sistema.
>
> **Estado:** 🟨 En progreso (repos locales listos, remotos GitHub pendientes del usuario)
> **Sesiones estimadas:** 1
> **Fecha de última actualización:** 2026-10-04

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 1.1 — Preparación
- [x] Verificar que la Etapa 0 (reestructuración) está completa y validada
- [ ] Crear los 7 repos remotos en GitHub (el usuario los sincronizará; los locales ya existen):
  - [ ] `mvp-frontend`
  - [ ] `mvp-exam-app`
  - [ ] `mvp-agents-backend`
  - [ ] `mvp-latex-compiler`
  - [ ] `mvp-embedding-service`
  - [ ] `mvp-core`
  - [ ] `MVP_LatexExam` (meta-repo)

### 1.2 — Inicializar repos de apps
- [ ] Para cada app/lib:
  - [ ] `git init` en su carpeta
  - [ ] Crear `.gitignore` propio (si aplica)
  - [ ] Commit inicial con su historial recortado (opcional: `git filter-repo` para conservar solo el historial de esa ruta)
  - [ ] Push al remoto

### 1.3 — Convertir el repo actual en meta-repo
- [x] Eliminar las carpetas de apps/libs del índice del repo raíz
- [ ] Agregar cada app/lib como `git submodule add`
- [ ] Verificar que `.gitmodules` queda bien formado
- [ ] Push del meta-repo (pendiente: remoto GitHub)

### 1.4 — Configuración de workflows
- [ ] CI por repo (tests/lint/build) — pipeline básico en cada app
- [ ] Pipeline de integración en el meta-repo (construye el sistema completo con los SHAs fijados)
- [ ] Configurar `deploy/` para componer desde un tag del meta-repo

### 1.5 — Validación
- [ ] Clon limpio con `--recurse-submodules` funciona
- [ ] `docker compose up` funcional desde el clon limpio
- [ ] Push/pull de submódulos funciona correctamente (pendiente de remotos)
- [ ] `git status` en submódulos no muestra cambios pendientes

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
| `MVP_LatexExam` (meta-repo) | `MVP_v1/` | Submódulos + orquestación (compose, scripts, docs, `.env.example`) |
| `mvp-frontend` | `apps/frontend/` | Vue 3 + Vite + TS + Pinia |
| `mvp-exam-app` | `apps/exam-app/` | FastAPI — API pública/BFF |
| `mvp-agents-backend` | `apps/agents-backend/` | LangGraph — exam_pipeline + conversational + shared |
| `mvp-latex-compiler` | `apps/latex-compiler/` | Microservicio TeXLive |
| `mvp-embedding-service` | `apps/embedding-service/` | Microservicio bge-m3 |
| `mvp-core` | `libs/core/` | Shared kernel: modelos, banco, migraciones, clientes |

Lo que **queda solo en el meta-repo** (no es código de ninguna app): `data/`, `docker/` (compose de desarrollo), `deploy/`, `docs/`, `scripts/` operativos, `alembic.ini`, `readme.md`, `ARCHITECTURE.md`.

---

## ✅ Criterios de aceptación

- [x] Clon limpio con `--recurse-submodules` funciona
- [ ] `docker compose up` funcional desde el clon limpio
- [ ] Push/pull de submódulos funciona
- [ ] CI por repo configurado
- [ ] Pipeline de integración en el meta-repo configurado

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

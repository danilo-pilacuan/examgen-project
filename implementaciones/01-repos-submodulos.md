# Etapa 1 — Repos múltiples + submódulos git (meta-repo)

> **Objetivo:** Convertir cada app/lib en un **repositorio Git independiente**, orquestados por un **repo raíz (meta-repo)** mediante **submódulos git**. El meta-repo fija qué commit de cada app compone una versión coherente del sistema.
>
> **Estado:** ⬜ Pendiente
> **Sesiones estimadas:** 1
> **Fecha de última actualización:** 2026-10-04

---

## IMPORTANTE: ESTE PROYECTO NO NECESITA TESTS CON PYTEST O VITEST, ESO GASTA TOKENS INNECESARIAMENTE
## 📋 Tareas

### 1.1 — Preparación
- [ ] Verificar que la Etapa 0 (reestructuración) está completa y validada
- [ ] Crear los 7 repos remotos en GitHub:
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
- [ ] Eliminar las carpetas de apps/libs del índice del repo raíz
- [ ] Agregar cada app/lib como `git submodule add`
- [ ] Verificar que `.gitmodules` queda bien formado
- [ ] Push del meta-repo

### 1.4 — Configuración de workflows
- [ ] CI por repo (tests/lint/build) — pipeline básico en cada app
- [ ] Pipeline de integración en el meta-repo (construye el sistema completo con los SHAs fijados)
- [ ] Configurar `deploy/` para componer desde un tag del meta-repo

### 1.5 — Validación
- [ ] Clon limpio con `--recurse-submodules` funciona
- [ ] `docker compose up` funcional desde el clon limpio
- [ ] Push/pull de submódulos funciona correctamente
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

- [ ] Clon limpio con `--recurse-submodules` funciona
- [ ] `docker compose up` funcional desde el clon limpio
- [ ] Push/pull de submódulos funciona
- [ ] CI por repo configurado
- [ ] Pipeline de integración en el meta-repo configurado

---

## 📝 Notas de sesión

> Registrar aquí cualquier decisión, problema o hallazgo durante la ejecución de esta etapa.

- (vacío)

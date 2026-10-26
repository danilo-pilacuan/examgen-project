---
id: handoff
tipo: Guide
type: Guide
title: Handoff entre sesiones
description: Punto de entrada de cada sesion; estado exacto donde se quedo el trabajo.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [plan, ops-readme]
status: stable
sources: [{ id: copilot-instructions, resource: ../.github/copilot-instructions.md, title: copilot-instructions }]
---

> **Ultima actualizacion:** 2026-10-26 | **Rama:** `RC2/develop` | **Arbol:** limpio;
> migracion `implementaciones/` -> `.ops/` publicada en commit `4b50c75`; submodulos
> publicados en origin (frontend `1c3c674`, exam-app `29a64e3`, agents-backend, core y
> latex-compiler en 78a874f).

## Contexto en 30 segundos

Exam Generator: MVP de tesis USFQ para que un profesor genere examenes LaTeX por chat con agente LangGraph y HITL, con versiones con/sin respuestas. Monorepo con 6 submodulos. Estado actual: **RC2/develop** tras 4 rondas de QA (etapa 16 la ultima, 2026-10-26) y el framework de evaluacion del agente ejecutado (etapa 15, 102 runs reales, H1-H5 resueltas). Desarrollo congelado para pasar al escrito de la tesis.

## Que leer y en que orden

1. Este archivo (`project/handoff.md`).
2. `../../PROGRESS.md` (bitacora raiz).
3. `project/plan.md` (mapa de etapas) y el IMPL activo en `../implementations/`.
4. Para campanas de evaluacion: `../../test/evaluation/README.md` (doc viva del framework).

## Estado por donde se quedo

| Tema | Estado |
|---|---|
| Caso de uso central (materias, material, preguntas HITL, examenes, ZIP) | Verificado E2E (rondas 1-4; C2 pendiente de re-test con PDF grande real) |
| Framework de evaluacion (etapa 15) | Ejecutado: 102 runs reales; hiperparametros validados T gen=0.7, top_k=3, T eval=0.2 |
| BUG abiertos | Solo BUG-016 (401 transitorio tras reiniciar exam_app; menor) |
| Backlog P2/P3 | BL-001..BL-021 (Playwright suite, ISS-17/18, cards anchas, preview PDF) |
| Etapa 01 (repos GitHub + CI) | Pendiente: repos locales listos, remotos no creados |
| Migracion a .ops | Hecha en esta sesion: `implementaciones/` eliminado; todo vive en `.ops/` (89 docs OKF). IMPL-020 queda `borrador` hasta la revision del propietario |

## Trabajo pendiente (priorizado)

1. Escrito de tesis, capitulo de experimentacion (usa `test/evaluation/` FINDINGS; sin codigo).
2. BL-010 suite Playwright versionada (P2; requiere codigo).
3. BL-016 ISS-17 materia activa tras hard reload (P2; codigo XS).
4. Comparativa cross-provider de modelos (P3; depende de acceso a otro modelo en el gateway).
5. Etapa 01: crear repos remotos + CI del meta-repo (P3; requiere codigo).

## Gotchas que NO hay que redescubrir

- PowerShell no soporta `&&` -> usar `;` o if-checks.
- Scripts creados en Windows llevan CRLF; `sh` de alpine los rechaza -> `dos2unix`.
- La consola Windows es cp1252: leer archivos UTF-8 con `view` o Python, no `Get-Content`.
- Los fixes de nginx y la config van horneados en la imagen -> rebuild Docker tras tocarlos.
- El routing nginx por `Accept` exige probar TODOS los metodos HTTP de cada prefijo (BUG-017b).
- Framework: dry-run contamina la BD real con stubs; nunca mezclar modos sin re-indexar (`test/evaluation/src/_reindex_real.py`). El judge usa `max_tokens=2000` (el gateway consume reasoning tokens). La latencia bimodal del gateway es efecto de carga, no causal.

## Historial de sesiones

| Fecha | Alcance y resultado |
|---|---|
| 2026-10-26 (anterior) | Etapa 16 (QA ronda 4 scroll + nginx toggle) ejecutada y publicada; handoff estructurado |
| 2026-10-26 (actual) | Migracion de `implementaciones/` al arbol `.ops` (89 docs: 21 IMPL, 22 BL, 18 BUG, 3 REQ, plan, handoff, traceability, plantillas, READMEs); referencias externas actualizadas; carpeta original eliminada; sin codigo de producto |

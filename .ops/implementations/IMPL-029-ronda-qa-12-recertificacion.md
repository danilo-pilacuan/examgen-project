---
id: IMPL-029-ronda-qa-12-recertificacion
tipo: Implementation
type: Implementation
title: QA ronda 12 - recertificacion funcional, credenciales, BUG-026/BUG-027 corregidos
description: Ronda 12 (mandato del propietario): re-certificacion funcional primordial con verificacion humana del agente, entrega de credenciales en archivo de salida, y fix de los bugs que no dañan la certificacion.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [QT-012, BL-010]
status: draft
---

## Alcance

Incluye: re-ejecucion de la certificacion funcional sobre la BD de ronda 11
(sin rebuild: la BD se reconstruyo en la ronda 11 y se conserva); suite e2e
versionada completa; entrega de credenciales QA en archivo de salida
(git-ignored); triage y fix de BUG-026 y BUG-027 (fixes que no alteran el
alcance de la tesis ni los resultados de campana ya publicados).

No incluye: BUG-024/025 (P2, abierto), BUG-019/020/021 (DEC-001/002/003
pendientes del propietario), extension E03, written thesis.

## Diseno

La ronda 11 reconstruyo la BD desde cero y regenero contenido y metricas;
la ronda 12 recertifica ese estado con regresion completa y cierra los dos
bugs de ronda 9 que seguian abiertos. BUG-026: watcher centralizado en
AppHeader (patron ExamsView, immediate). BUG-027: fail-fast en el endpoint
(404/422) + contador real en ingestor_node; ambos prescritos en los docs
de defecto y alineados con C6/BUG-004 y E5.

## Pasos atomicos

1) credenciales en archivo de salida; 2) suite e2e 16/16 (15 + bug026);
3) triage BUG-027 con repro E5/E1 en vivo; 4) fix #1 endpoint + fix #2
ingestor; 5) rebuild imagen + verificacion V1-V4; 6) regresion 16/16;
7) purga de artefactos de repro (BD + output); 8) docs .ops + commits.

## Rollback

git revert de los 3 commits de codigo (c327682, 2474b2c, e5cee07) y rebuild
de imagen; la BD no cambia de schema y los artefactos de repro se purgaron.

## Ejecucion real (2026-10-28)

- Credenciales: qa-r11-credentials.qa-creds.txt (git-ignored, modo 600).
- Suite e2e: 16/16 PASS tras BUG-026 (14:51) y de nuevo tras el rebuild de
  BUG-027 (12.5 s); L2 estricto verde.
- BUG-026 -> corregido (frontend c327682): 3/3 caminos verificados en vivo
  (login, Activate, combobox) con conteos contra BD real.
- BUG-027 -> corregido (exam-app 2474b2c + agents-backend e5cee07, meta
  6ca1c13): repros E5/E1 confirmaron ambos claims con evidencia en vivo;
  V1 422 accionable (materia vacia), V2 200 con indexed_chunks_count: 28,
  V3 404, V4 BD limpia (C6). Sin publicacion ni persistencia en el caso
  vacio.
- Purga: materia de repro + filas de examen persist:false (BUG-021,
  2 ocurrencias re-confirmadas) + JSON/PDF/ZIP de repro eliminados; las
  materias de control y sus 2 examenes qa11 quedaron intactos (6q/28c y
  6q/85c; banco 6/6).

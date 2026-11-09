---
id: QT-012
tipo: TestCase
type: TestCase
title: Recertificacion ronda 12 - regresion funcional completa, credenciales y cierre BUG-026/BUG-027
description: Ronda 12 (mandato del propietario): continuar la ronda de QA, entregar credenciales en archivo de salida, reportar lo que falta y corregir los bugs que no dañan la certificacion.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [REQ-001, QT-011]
status: draft
fase: 6
---

## Objetivo

Re-certificar el estado dejado por la ronda 11 (BD desde cero, contenido y
metricas en ingles) con la suite e2e completa; entregar las credenciales QA
en archivo de salida; triagear y corregir BUG-026 y BUG-027 al no dañar la
certificacion (preservan alcance y resultados de campana r11). Deriva de la
seccion 0 de AGENTS.md y de la estrategia QA (navegador real; el agente
actua como humano).

Precondiciones: stack Docker healthy; BD de ronda 11 operante (alembic head
b8c9d0e1f2a3); materias de control Database Systems (6q/28c) y Economia
Aplicada - QA11 (6q/85c); 2 examenes de control qa11.

## Casos que deben pasar

- CRED-1: credenciales QA en archivo de salida git-ignored
  (qa-r11-credentials.qa-creds.txt).
- E2E-1: suite versionada 16/16 PASS (15 tests F/I/L + bug026.spec.cjs);
  L2 estricto (0 marcas de espanol en la muestra de preguntas).
- BUG-026-V: 3/3 caminos de estadisticas de cabecera correctos en vivo
  (login sin interaccion, Activate en Materias, cambio por combobox),
  conteos contra BD real; capturado en bug026.spec.cjs.
- BUG-027-V1 (E5 repetido): materia 0 chunks/0 preguntas -> 422 accionable;
  sin publicacion ni persistencia.
- BUG-027-V2 (E1 repetido): materia con material -> 200 con
  `indexed_chunks_count` igual al COUNT real (28) y item RAG-grounded.
- BUG-027-V3: subject_id inexistente -> 404 (antes nombre falso "Subject").
- BUG-027-V4 (C6 regresion): la materia vacia queda sin preguntas ni
  examenes en BD; los examenes de control qa11 intactos.

## Caso adversarial observado (no corregible en esta ronda)

- `persist:false` siguio persistiendo examen/PDFs/ZIP en 2 repros de la
  ronda (BUG-021 re-confirmado en vivo; DEC-003 pendiente del propietario).
  Artefactos purgados tras cada verificacion.

## Resultado (2026-10-28, evidencia real)

- CRED-1: PASS (archivo entregado, fuera de git por .gitignore).
- E2E-1: PASS 16/16 (10.8 s tras BUG-026; 12.5 s tras rebuild BUG-027).
- BUG-026-V: PASS 3/3 (frontend c327682; meta 299b118).
- BUG-027-V1: PASS (422 con mensaje accionable en ingles; materia de repro
  purgada y quedo 0/0).
- BUG-027-V2: PASS (HTTP 200, indexed_chunks_count: 28, item aprobado
  "According to the text, what is the basic software...").
- BUG-027-V3: PASS (404 "Subject not found").
- BUG-027-V4: PASS (0 filas nuevas en exams para la materia de repro;
  qa11_control_db/qa11_control_econ intactos; banco 6/6 y 6/6).
- Commits: c327682 (frontend BUG-026), 2474b2c (exam-app BUG-027 fix #1),
  e5cee07 (agents-backend BUG-027 fix #2), meta 299b118 y 6ca1c13,
  todos publicados en RC3/develop.

Estado: ejecutado (verificacion del propietario pendiente; nunca
auto-asignada por el agente). Datos de control: qa-r11@usfq.test.

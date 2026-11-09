---
id: IMPL-027-ronda-qa-10-framework-e2e-idioma
tipo: Implementation
type: Implementation
title: QA ronda 10 - framework e2e versionado (BL-010) y contrato de idioma ingles
description: Suite Playwright versionada en projects/frontend/e2e y recertificacion de lo esencial; enforceo y verifico el contrato "todo el sistema en ingles" (UI, preguntas, respuestas).
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [BL-010, QT-010]
status: draft
---

## Alcance

Incluye: framework de pruebas versionado BL-010 (Playwright, 15 tests F/I/L),
recertificacion de lo esencial contra el stack Docker, enforce del contrato de
idioma en los prompts de generacion/evaluacion/verificacion del backend, y
generacion de examen de control para certificar ingles en items nuevos.

No incluye: fix de BUG-027 (pipeline publica examenes sin material), fix de
BUG-024 (cabeceras nginx), remedio del dato heredado en espanol (BUG-028,
decision pendiente del propietario), cambios a AGENTS.md o scope.

## Diseno

Suite e2e: `projects/frontend/playwright.config.ts` (baseURL via
E2E_BASE_URL, 1 worker, trace/screenshot on failure), `e2e/helpers.ts`
(login UI + fixture authedPage), `e2e/tests/functional.spec.ts` (F1, F1b,
F2, F3, F4, F5, F11, F12), `e2e/tests/integration.spec.ts` (I1, I5, I8,
I-bonus), `e2e/tests/language.spec.ts` (L1, L1b, L2 informativo).
Credenciales por env (E2E_EMAIL/E2E_PASSWORD/E2E_SUBJECT, ver
e2e/.env.example). Cuenta de control: qa-r10 (creada en BD, hash pbkdf2
identico al backend).

Contrato de idioma: prompts en exam_pipeline/nodes.py (generator_node y
evaluator_node: rechazo language_not_english), conversational/tools.py
(generate_question) y shared/verifier.py exigen escribir question/opciones/
respuesta/explicacion en ENGLISH independientemente del idioma del material
o del nombre de la materia. Backend reconstruido (docker compose build
exam-app) y verificado dentro del contenedor (grep 'in ENGLISH' 1/2/1).

Pasos atomicos: 1) suite versionada en verde contra el stack; 2) rebuild
backend con prompts; 3) E1-EN: POST /exams/generate sobre materia semilla
Eva (material en espanol) y verificacion de items/artefactos en ingles;
4) documentacion (test-plan ronda 10, BUG-028, trazabilidad, handoff).

Rollback: la suite es solo-add (directorio e2e); revert de los 3 archivos de
prompts devuelve el comportamiento anterior; examen de control desechable.

## Ejecucion real (2026-10-28)

- Suite Playwright: 15/15 PASS (10.0-10.5 s, 3 corridas; la ultima tras el
  rebuild del backend). Output real: "15 passed (10.0s)".
- E1-EN PASS: examen QA_R10_English_Gen (materia Eva, 3 items, 1 version):
  3 statements + 12 opciones + 3 respuestas + 3 explicaciones 100% en
  ingles (verificado leyendo items de BD), 0 rechazos del evaluador;
  artefactos QA_R10_English_Gen_A.pdf, _A_respondido.pdf, .zip y .json en
  /app/output. El material RAG context estaba en espanol y el item salio en
  ingles: el enforce funciona con contexto cross-language.
- L2 informativo: banco heredado 197/200 en espanol (muestra Eva) ->
  BUG-028 (dato, no codigo): 933/1239 preguntas del censo completo.
- Resultado: suite 15/15 PASS + E1-EN PASS; BUG-028 nuevo abierto;
  BUG-026/027/024/025 siguen abiertos (fuera de alcance).

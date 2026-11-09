---
id: QT-013
tipo: TestCase
type: TestCase
title: Exportacion del banco con auditoria prompt/thinking (F7)
description: Verificacion en vivo del endpoint de export y de la descarga en UI, mas suite e2e ampliada a 18 casos.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [BL-022, QT-012]
status: draft
fase: 6
---

## Objetivo

Verificar la nueva funcionalidad de descarga del banco (BL-022) en API y UI,
con el agente actuando como humano en navegador real, y ampliar la suite e2e
versionada con los casos F7/F7b.

Precondiciones: stack Docker rebuilt (exam-app 40e6750, frontend f19813f);
cuenta qa-r11@usfq.test; materias con banco generado (prompt correlacionable).

## Casos que deben pasar

- EXP-1 (API): GET /subjects/{id}/questions/export con Bearer -> 200,
  total_questions == len(questions), exported_at ISO UTC, subject correcto.
- EXP-2 (correlacion): prompt poblado en 218/218 preguntas de Applied
  Economics - Adam y 6/6 de Economia Aplicada - QA11 (statement exacto).
- EXP-3 (degradacion): thinking null en todas las filas;
  thinking_capture_enabled == false (LLM_CAPTURE_THINKING deshabilitado).
- EXP-4 (UI): boton Download bank visible y habilitado; click dispara
  descarga `question_bank_*.json` y alerta de confirmacion con conteo y
  nota de thinking deshabilitado.
- EXP-5 (UI detalle): fila expandida muestra bloques Prompt/Thinking o
  fallback noPrompt en ingles (contrato L2).
- E2E: suite completa 18/18 PASS (16 previos + F7 + F7b en
  e2e/tests/download.spec.ts, con parseo del JSON descargado).

## Resultado (2026-10-28, evidencia real)

- EXP-1: PASS (218 preguntas, exported_at 2026-10-28T21:33:54+00:00).
- EXP-2: PASS (Q_WITH_PROMPT=218/218; QA11 6/6).
- EXP-3: PASS (thinking_null=True; THINKING_FLAG=False).
- EXP-4: PASS en navegador real (alerta "Bank downloaded: 218 questions
  (JSON)" + nota de thinking; archivo question_bank_*.json sugerido).
- EXP-5: PASS (F7b en e2e; texto Prompt/noPrompt en ingles).
- E2E: PASS 18/18 (21.4 s; 2 nuevos casos verdes).
- Commits: exam-app 40e6750, frontend f19813f, publicados en RC3/develop.

Estado: ejecutado (verificacion del propietario pendiente; nunca
auto-asignada por el agente). Datos de control: qa-r11@usfq.test.

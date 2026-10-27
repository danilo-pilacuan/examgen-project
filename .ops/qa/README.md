---
id: qa-readme
tipo: Guide
type: Guide
title: QA index
description: Estrategia, plan de pruebas, matriz de trazabilidad y registro BUG.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [templates-defect]
status: stable
---

## Index

- `strategy.md` - what "verified" means (browser-only rule) + validation rules.
- `test-plan.md` - C1-C54 + F1-F14 + I1-I8 + E1-E5 + R1-R7 certification matrix per round.
- `traceability.md` - REQ -> BL -> IMPL -> QT coverage with evidence.
- `BUG-001..BUG-027.md` - defect register, flat in this folder (28 files).

Round 9 (2026-10-27, IMPL-026, recertificacion + certificacion de examenes):
funcionales Playwright (F1-F13) + integracion API (I1-I6) + examenes E1-E5.
22 PASS / 2 FAIL. BUG-027 nuevo (alto): el pipeline publica examenes con 0
chunks y 0 preguntas (preguntas genericas fuera de tema, "Sahara Desert");
E1 reporta `indexed_chunks_count:0` pese a 41 chunks en BD. BUG-026 nuevo
(menor): chips de cabecera 0/0 hasta re-seleccionar el asunto tras login o
Activate. I4 sigue FAIL conocido (BUG-024, sin fix planificado). Hilos de
control r9 purgados; examen QA_R9_Cert queda como evidencia.

Round 8 (2026-10-27, IMPL-025, fix DEC-004): hilos de chat server-side
(BL-017): tabla `chat_threads` + GET/PATCH/DELETE /api/chat/threads +
ownership 403 en history/stream/invoke; sidebar con badges (ultima materia,
contador de mensajes) e hidratacion server-side. BUG-022 y BUG-023 ->
`corregido` (verificacion final pendiente del propietario). QT-008:
12 comprobaciones API PASS + verificacion Playwright PASS. Hilos de control
qa-r8 purgados.

Round 7 (2026-10-27, IMPL-024, recertificacion funcional + integracion):
bug reportado "no veo conversaciones pasadas" = BUG-023 (listado solo en
localStorage; fix en BL-017); BUG-022 critico (hilos de chat sin
propiedad: lectura/escritura entre usuarios, DEC-004 abierta); BUG-024
(sin cabeceras de seguridad nginx) y BUG-025 (mensaje 401 enganoso en
login) nuevos. C25-C40: 11 PASS / 3 FAIL / 2 PASS con nota.

Bugs follow `templates/defect.md`; the agent writes evidence (real output, never
claimed), the owner sets `verified`. QT follow `templates/test-case.md`; only the
owner closes them.
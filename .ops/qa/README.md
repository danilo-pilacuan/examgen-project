---
id: qa-readme
tipo: Guide
type: Guide
title: QA index
description: Estrategia, plan de pruebas, matriz de trazabilidad y registro BUG.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [templates-defect]
status: stable
---

## Index

- `strategy.md` - what "verified" means (browser-only rule) + validation rules.
- `test-plan.md` - C1-C54 + F1-F14 + I1-I8 + E1-E5 + R1-R7 certification matrix per round.
- `traceability.md` - REQ -> BL -> IMPL -> QT coverage with evidence.
- `QT-007..QT-011.md` - test case records (rounds 7-11), flat in this folder.
- `BUG-001..BUG-029.md` - defect register, flat in this folder (30 files).

Round 11 (2026-10-28, IMPL-028, mandato del propietario: recertificar lo
primordial, regenerar el framework de pruebas, ingles en todo el sistema,
regenerar el set de metricas y reconstruir la BD desde cero): BD
reconstruida desde cero (head b8c9d0e1f2a3); 12 preguntas nuevas 100% en
ingles generadas via pipeline real y verificadas por el agente actuando
como humano (HITL 12/12, verified_by_human=t; falso positivo de mojibake
descartado con cliente Python: beta/por son UTF-8 real, artefacto cp1252
de la consola). Suite Playwright 15/15 PASS con L2 endurecido a asercion
estricta. Set de metricas regenerado: subjects.yaml (5 clones en ingles),
experiments.yaml (topics en ingles, 82 runs) y campana real lanzada
(E04->E03->E01->E02). BUG-028 -> `corregido` (opcion c del propietario:
purga + regeneracion). BUG-029 nuevo (medio): indexacion docx/pptx falla
en contenedor (No module named 'docx'; python-docx/python-pptx no
declarados en manifests); la validacion previa conserva los chunks
existentes (51/51 tras el 400). Verificacion final pendiente del
propietario.

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
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
- `QT-007..QT-013.md` - test case records (rounds 7-13), flat in this folder.
- `BUG-001..BUG-029.md` - defect register, flat in this folder (30 files).

Round 13 (2026-10-28, extension de la ronda 12, BL-022, mandato del
propietario: anadir en el frontend la descarga del banco con campos de
pensamiento y prompt): endpoint GET /subjects/{id}/questions/export (exam-app
40e6750) correlaciona llm_responses por statement exacto; frontend f19813f
boton Download bank + bloques Prompt/Thinking en el detalle; thinking null
cuando LLM_CAPTURE_THINKING este deshabilitado (degradacion documentada).
QT-013: API 218/218 prompts, UI verificada en vivo, e2e 18/18 PASS (F7/F7b
nuevos en download.spec.ts). Verificacion final pendiente del propietario.

Round 12 (2026-10-28, IMPL-029, mandato del propietario: continuar la ronda,
credenciales en archivo, corregir bugs que no dañen la certificacion): suite
e2e 16/16 PASS (15 versionadas + nueva bug026.spec.cjs). BUG-026 ->
`corregido` (frontend c327682): watcher centralizado de activeSubjectId en
AppHeader, 3/3 caminos verificados en vivo con conteos contra BD real.
BUG-027 -> `corregido` (exam-app 2474b2c + agents-backend e5cee07, meta
6ca1c13): repros en vivo confirmaron ambos claims (generacion de genericas
con 0/0; contador siempre 0) y el fix quedo verificado en 4 chequeos
(422 accionable en materia vacia, indexed_chunks_count real 28, 404 en
materia inexistente, C6 limpio). BUG-021 re-confirmado en vivo 2 veces
(persist:false persiste; DEC-003 pendiente). Artefactos de repro purgados.
Verificacion final pendiente del propietario.

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
declarados en manifests); La validacion previa conserva los chunks
existentes (51/51 tras el 400). Corregido: deps declaradas en los 3
manifests + rebuild exam-app; repro 200/200/200 con 4, 40 y 85 chunks
reinsertados (85 total, 41 PDF + 4 docx + 40 pptx). Campana real COMPLETADA
82/82 (0 fallidos) con agregados + reportes + FINDINGS r11 (commit 9e6bd6c).
Hallazgo J1: el juez LLM in-run registro num_judged=0 en 82/82 (retrieval sin
correlacionar); corregido en harness.py + windowing de judge_experiment.py
(commit 3827e4d); juez post-hoc abortado por deriva de +-1 fila en las
ventanas de auditoria (documentado, no silenciado). Ingles de la campana
verificado: 621 items escaneados (scripts/qa_r11_english_check.py), 0 cuerpos
en espanol, 13/621 nombres propios o glosas del material, 3/621 subtopic con
eco del temario, 5 rechazos language_not_english del evaluador en campana.
Verificacion final
pendiente del propietario.

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
---
id: IMPL-028-ronda-qa-11-recertificacion
tipo: Implementation
type: Implementation
title: QA ronda 11 - recertificacion funcional, BD desde cero, ingles end-to-end y set de metricas regenerado
description: Ronda 11 (mandato del propietario): reconstruccion total de la BD, regeneracion del contenido en ingles con verificacion humana HITL, regeneracion completa del framework de evaluacion (subjects/experiments) y campana real de 82 runs.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [BL-010, QT-011]
status: draft
---

## Alcance

Incluye: recertificacion funcional de lo primordial con el agente actuando
como verificador humano (derecho HITL explicito del propietario);
reconstruccion de la BD desde cero y re-indexacion del material; generacion
de 12 preguntas nuevas en ingles via pipeline real y aprobacion humana
12/12; regeneracion completa del set de evaluacion (subjects.yaml,
experiments.yaml, raws archivadas); smoke dry-run; campana real de 82 runs.

No incluye: BUG-026/027/024/025 (abiertos, fuera de alcance), extension
E03 de ronda 10 (queda opcional post-campana), cambios a AGENTS.md o scope.
Nota de cierre: BUG-029 entro en alcance por el rechazo adversarial (deps
docx/pptx no declaradas) y quedo corregido dentro de esta ronda.

## Diseno

BD desde cero: drop + alembic upgrade head (b8c9d0e1f2a3, 13 tablas);
re-indexacion de material (Database Systems 28 chunks; Economia Aplicada -
QA11 51 chunks). Semilla de contenido: 6 preguntas por materia via pipeline
real (DB 2-13), todas en ingles por contrato de la ronda 10 (prompts
generator_node/evaluator_node/tools/verifier exigen ENGLISH).

HITL: el agente (rol QA con derecho humano otorgado) revisa las 12 preguntas
con criterio de docente (exactitud, distractores, dificultad, redaccion);
aprueba 12/12 y marca verified_by_human=true via
PUT /questions/{id}/verification {"verified": true}. 2 sospechas de
mojibake (beta U+03B2, por U+00D7) descartadas: son simbolos matematicos
UTF-8 reales; el "raro" era artefacto de consola cp1252 de PowerShell 5.1
(verificado con cliente Python y regex en BD). Leccion: verificar
quejas de encoding con cliente Python/BD antes de abrir BUG.

Framework de evaluacion regenerado: subjects.yaml (5 clones en ingles
adam/bella/carlos/diana/esteban -> "Applied Economics - X", mismo
material_glob PDFs) y experiments.yaml (topics_weight en ingles: Market
Study 0.3, Financial Flows 0.3, Economic and Financial Analysis 0.25,
Pricing 0.15; listas de clones actualizadas; 82 runs: E01=27, E02=27,
E03=10, E04=18). Raws de ronda 10 archivadas (gitignore; agregados
versionados permanecen en git). Smoke dry-run OK (6 familias de metricas,
nombres en ingles); polucion del smoke purgada con FK-order. Campana real
lanzada en background (scripts/run_eval_campaign_r11.ps1, orden por costo
E04->E03->E01->E02, PYTHONIOENCODING=utf-8). El harness gajo dos refuerzos
de robustez (commit 41d368c): bootstrap de .env y reanudacion por runs
ya completados; el runner de campana es crash-proof y auto-bootstrapping.

## Pasos atomicos

1) drop + alembic head; 2) re-indexar material; 3) generar 12 preguntas
(pipeline real); 4) revision humana 12/12 + verified_by_human; 5) suite
Playwright 15/15 con L2 estricto; 6) 2 examenes de control en ingles
compilan (qa11_control_db, qa11_control_econ); 7) regenerar
subjects/experiments + archivar raws; 8) smoke dry-run + purga; 9) campana
real 82 runs; 10) agregados + informes + documentacion .ops.

## Rollback

La BD es reconstruible (drop + seed); los clones y experimentos son
config-only (git revert); los raws son reproducibles re-ejecutando el
harness; los examenes de control son desechables.

## Ejecucion real (2026-10-28)

- BD: head b8c9d0e1f2a3, 13 tablas, 0 heredado; 79 chunks (28+51).
- Contenido: 12/12 preguntas en ingles, source=pipeline, verificadas
  12/12 (verified_by_human=t en BD; revision HITL registrada en la sesion).
- Suite Playwright: 15/15 PASS (10.8 s); L2 estricto (toHaveLength(0)).
- Examenes de control: 2/2 compilan con PDFs (con/sin respuestas) + ZIP
  en data/agent_outputs.
- Adversarial docx: 400 + chunks intactos (51/51) -> BUG-029 nuevo;
  corregido en la misma ronda: deps declaradas (pymupdf, python-docx,
  python-pptx, openpyxl) en core f0fc306 y exam-app 2fd4491, imagen
  reconstruida, verificacion en vivo 200/200/200 (4 docx + 40 pptx +
  85 chunks reindex completo) con scripts/qa_r11_docx_index.py.
- Campana 82 runs: COMPLETADA 82/82 (E04 18, E03 10, E01 27, E02 27;
  0 fallidos; resume de corridas de verificacion en vivo = SKIP sin
  re-costo). Agregados + reportes + FINDINGS generados para E01-E04.
- Hallazgo J1 (juez in-run): num_judged=0 en 82/82; causa: harness pasaba
  retrieval sin correlacionar (statement vacio) y el juez descarta en
  silencio; corregido en harness.py (judge recibe
  _correlate_statements(...)). Post-hoc abortado por ventana +-1 fila
  (E04 79 vs 80; E01 213 vs 214): riesgo de desalinear pares
  statement<->chunks. rag_faithfulness (cross-encoder) si cubre 82/82.
- Ingles (HITL): 621 items escaneados (scripts/qa_r11_english_check.py):
  0 cuerpos en espanol; 13/621 nombres propios/glosas del material y
  3/621 subtopic con eco del temario (metadato); evaluador rechazo 5 items
  language_not_english en la campana (defensa activa).

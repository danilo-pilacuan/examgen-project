---
id: QT-011
tipo: TestCase
type: TestCase
title: Recertificacion ronda 11 - recertificacion funcional, framework e2e, contrato de idioma y campana de evaluacion regenerada
description: Ronda 11 (mandato del propietario): recertificar lo primordial con el agente como verificador humano, regenerar el framework de pruebas, asegurar ingles en todo el sistema (preguntas y respuestas incluidas), regenerar el set completo de metricas y reconstruir la BD desde cero.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-28
relaciona: [REQ-001, REQ-002]
status: draft
fase: 6
---

## Objetivo

Re-certificar el caso de uso central y el framework de evaluacion tras el
mandato del propietario (ronda 11): base de datos reconstruida desde cero,
todo el contenido en ingles (UI, preguntas, respuestas, explicaciones),
set de metricas de evaluacion regenerado y verificacion humana de las
preguntas ejecutada por el agente (rol QA con derecho HITL). Deriva de la
seccion 0 de AGENTS.md (validacion obligatoria, ejecutar antes de afirmar)
y de la estrategia QA (navegador real; el agente actua como humano).

Precondiciones: stack Docker healthy; BD reconstruida (alembic head
b8c9d0e1f2a3, 13 tablas); cuenta qa-r11@usfq.test; 2 materias sembradas
(Database Systems; Economia Aplicada - QA11) con 12 preguntas nuevas
generadas por pipeline real.

## Casos que deben pasar

- DB-1: reconstruccion desde cero (drop + alembic upgrade head); 13 tablas,
  0 registros heredados, embedder/pgvector operativos.
- DB-2: semilla real: 2 materias, 79 chunks (28 + 51), 12 preguntas
  source=pipeline, todas en ingles (cero acentos/e-caracteres en
  statements, opciones, respuestas y explicaciones).
- F-serie: suite Playwright versionada (projects/frontend/e2e) 15/15 PASS
  (funcionales F1-F5, integracion I1-I5, idioma L1-L3); L2 endurecido a
  asercion estricta: 0 preguntas con marcas de espanol en la muestra.
- HITL-1: revision humana de las 12 preguntas (agente como QA con derecho
  HITL): 12/12 APROBADAS; 2 sospechas de mojibake descartadas con cliente
  Python y regex en BD (beta/por son simbolos matematicos UTF-8 reales,
  artefacto de consola cp1252 de PowerShell 5.1).
- HITL-2: marcado verified_by_human=true en 12/12 via
  PUT /questions/{id}/verification {"verified": true}; pregunta verificada
  por humano es inmutable para el agente (403 al editar/borrar).
- E1-EN: 2 examenes de control compilan (qa11_control_db, qa11_control_econ)
  con PDFs (con/sin respuestas) + ZIP en data/agent_outputs; contenido en
  ingles.

## Campana de evaluacion regenerada (set de metricas)

- subjects.yaml regenerado: 5 clones en ingles (adam/bella/carlos/diana/
  esteban -> "Applied Economics - X"), mismo material_glob PDFs.
- experiments.yaml regenerado: topics_weight en ingles (Market Study 0.3,
  Financial Flows 0.3, Economic and Financial Analysis 0.25, Pricing 0.15;
  suma 1.0); 82 runs validados (E01=27, E02=27, E03=10, E04=18).
- Smoke en dry-run verificado (6 familias de metricas computadas, nombres
  en ingles); polucion del smoke purgada (FK-order: generated_questions ->
  material_chunks -> subjects).
- Campana REAL lanzada en segundo plano (E04->E03->E01->E02, 82 runs); el
  agregado y el informe por experimento se ejecutan al finalizar
  (analysis.aggregate + reporting.report).
- Defecto detectado tras la campana (J1): el juez LLM in-run no juzgo ningun
  registro (num_judged=0 en 82/82). Causa raiz: harness pasaba al juez los
  registros de retrieval SIN correlacionar (statement vacio) y el juez los
  descarta en silencio. Correlacion corregida en harness.py; la metrica
  rag_faithfulness de cross-encoder si se computo en las 82 corridas.

## Caso que debe ser rechazado (adversarial)

- Reindexar solo docx en Economia Aplicada debe fallar con 400 y NO debe
  borrar los chunks existentes: BUG-029 (No module named 'docx'; 51 chunks
  antes = 51 despues del 400, con clear=true).
- Editar/borrar una pregunta human-verified debe devolver 403 (guardrail
  del banco).

## Resultado (2026-10-28, evidencia real)

- DB-1, DB-2: PASS (censos BD en r11_state; 12/12 en ingles).
- F-serie: PASS 15/15 (10.8 s, 3 corridas estables); L2 estricto verde.
- HITL-1: PASS (12/12 aprobadas; mojibake descartado, falso positivo).
- HITL-2: PASS (12/12 verified_by_human=t en BD; 403 verificado en ronda 9
  I3 y re-confirmado por guardrail del servicio del banco).
- E1-EN: PASS (2 examenes de control compilan con PDFs + ZIP).
- Adversarial docx: 400 esperado y chunks intactos (51/51) -> BUG-029;
  tras reconstruir la imagen con las deps declaradas, verificacion en vivo
  docx 200 (4 chunks), pptx 200 (40 chunks), reindex completo 200 (85
  chunks = 41 PDF + 4 docx + 40 pptx). BUG-029 -> corregido (script
  scripts/qa_r11_docx_index.py).
- Campana 82 runs: COMPLETADA (82/82, 0 fallidos, exit 0; E04 18, E03 10,
  E01 27, E02 27). Agregados y reportes generados para E01-E04 (report.md
  + aggregate.json + FINDINGS.md por experimento). Hallazgo J1: juez in-run
  num_judged=0 (correlacion faltante, corregida en harness.py); el juez
  post-hoc se aborto deliberadamente: la ventana de filas de auditoria
  tiene incertidumbre de +-1 fila (E04 79 vs 80; E01 213 vs 214) que
  desalinearia pares statement<->chunks de forma silenciosa. La metrica
  rag_faithfulness (cross-encoder) si cubre las 82 corridas.
- Ingles (HITL de campana): escaneo determinista de 621 items entregados
  (scripts/qa_r11_english_check.py): 0 items con cuerpo en espanol;
  13/621 con nombres propios o glosas del material (Maria, Cafe Aroma,
  Project Lupulo, "(Estudio de Mercado)"), 3/621 con subtopic que repite el
  temario en espanol (metadato, no cuerpo). El evaluador rechazo 5 items
  por language_not_english durante la campana (defensa activa).

Estado: ejecutado (verificacion del propietario pendiente; nunca
auto-asignada por el agente). Datos de control: qa-r11@usfq.test.

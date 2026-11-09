---
id: BUG-027
tipo: Defect
type: Defect
title: El pipeline publica examenes sin material indexado ni banco (preguntas genericas fuera de tema)
description: Con 0 chunks y 0 preguntas en la materia, /exams/generate genera preguntas genericas del conocimiento del LLM (p.ej. "Sahara Desert") y publica el examen con ZIP/PDF; ademas la respuesta reporta indexed_chunks_count:0 pese a haber chunks en BD.
estado: corregido
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-009, IMPL-026, BUG-004, C6, E1]
status: draft
---

## Evidencia

Ronda 9 (2026-10-27):

- E5 (contrario): materia "QA R9 Recert" con `material_chunks = 0` y
  `generated_questions = 0` (verificado por API: material -> [], preguntas
  -> [] antes de generar). `POST /exams/generate` -> 200, `syllabus_summary:
  "No materials loaded."`, y el examen se publica con 2 items genericos:
  "The Sahara Desert is the largest desert on Earth." y una pregunta de
  "conceptual relationship", topic `general`, dificultad `hard`. Se crearon
  `QA_R9_Empty.zip`, `QA_R9_Empty_A.pdf`, `QA_R9_Empty_A_respondido.pdf` y
  la fila en `exams` (2 items, persistidos en BD) y 2 preguntas en el banco.
- E1 (nota): examen "QA_R9_Cert" sobre Eva (41 chunks en BD,
  445 preguntas): la respuesta reporta `"indexed_chunks_count": 0` y
  `"raw_materials_paths": []`; los 3 items publicados si tratan temas del
  curso (TIR/VAN, costos), lo que sugiere que el generador si usa RAG pero
  el contador/resumen del response no refleja el material usado.
- Contraste con BUG-004 (fix C6): ese fix falla-rapido cuando el pipeline
  no aprueba NINGUN item; aqui el pipeline aprueba items genericos y por
  eso publica, burlando la salvaguarda.

## Causa

`blueprint_node` construye el blueprint con `use_rag: true` pero el grafo
no exige material recuperado (ni banco existente) antes de generar: cuando
`indexed_chunks_count = 0`, el generator produce items desde el conocimiento
general del LLM (`topics_weight: {general: 1.0}`) y el evaluator los aprueba
si pasan sus umbrales de calidad. La salvaguarda de BUG-004 solo cubre
`len(approved_items) == 0`, no "items sin sustento en la materia". El
`indexed_chunks_count` del response se calcula en otro punto que no consulta
`material_chunks` por sujeto (siempre 0 en ambos casos probados).

## Fix y verificacion

1. Fail-fast en el pipeline (o en el endpoint): si `indexed_chunks_count ==
   0` y la materia no tiene preguntas aprobadas, devolver error accionable
   ("sube material o genera preguntas primero") sin publicar ZIP/PDF ni
   persistir examen (alineado con C6/BUG-004 y con E5 del plan).
2. Corregir el conteo: `indexed_chunks_count` debe leer
   `COUNT(material_chunks WHERE subject_id = ...)` real.
3. Verificacion: repetir E5 (0 chunks/0 preguntas -> rechazo); repetir E1
   (41 chunks -> `indexed_chunks_count: 41`); regredir C6 (sin items -> no
   publica).

## Ejecucion del fix (2026-10-28, ronda 12)

Implementado en ambos puntos prescritos:

- exam-app 2474b2c (fix #1): `POST /exams/generate` ahora 404 si el
  subject_id no existe (antes fingia nombre "Subject"), cuenta real de
  `material_chunks` y `generated_questions` por materia, y 422 con mensaje
  accionable en ingles si ambos son 0. Sin publicacion ni persistencia.
- agents-backend e5cee07 (fix #2): `ingestor_node` con `raw_materials_paths`
  vacio (camino API, RAG lee la BD) ahora devuelve el COUNT real de
  `material_chunks` de la materia como `indexed_chunks_count` en vez del
  0 constante.

Verificacion en vivo (4/4 PASS, imagen reconstruida):

- V1 (E5 repetido): materia 0 chunks/0 preguntas -> HTTP 422 con mensaje
  accionable; no se publica nada. Post-fix la BD quedo sin filas ni
  artefactos (repro purgado).
- V2 (E1 repetido): Database Systems (28 chunks) -> HTTP 200,
  `indexed_chunks_count: 28`, item RAG-grounded aprobado, PDFs/ZIP
  publicados (artefactos de prueba purgados tras la verificacion).
- V3: subject_id inexistente -> HTTP 404 "Subject not found".
- V4/C6 regresion: la materia vacia quedo 0 preguntas / 0 examenes en BD.

Regresion: suite e2e 16/16 PASS (15 versionadas + bug026). Nota: la fila
de examen del repro pre-fix sobrevivio con `persist:false` -> BUG-021
re-confirmado en vivo (2 ocurrencias en la ronda 12), DEC-003 sigue
pendiente del propietario.

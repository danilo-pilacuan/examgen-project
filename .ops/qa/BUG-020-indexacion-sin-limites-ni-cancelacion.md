---
id: BUG-020
tipo: Defect
type: Defect
title: Indexacion de material grande sin limites, progreso ni cancelacion bloquea el servicio de embeddings
description: Un PDF de 8000 paginas satura exam_embedding_service ~29 h, sin feedback al usuario ni forma de cancelar, y bloquea subidas posteriores.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-001, C2, BUG-005]
status: draft
---

## Evidencia

Ronda 6 (2026-10-27). C2 con PDF grande real:

- PDF sintetico de 8000 paginas / 6.86 MB (reportlab, texto extraible
  verificado con PyMuPDF en contenedor). Upload OK 200 (sin 413: nginx
  `client_max_body_size 100m`).
- Extraccion de texto: ~101 s (PyMuPDF, dentro del contenedor) -> ~41,500
  chunks (CHUNK_SIZE=1500).
- Embeddings bge-m3 en CPU: ~90 s por batch de 16 chunks -> estimacion
  ~29 HORAS para terminar. Durante la prueba, `exam_embedding_service`
  saturo CPU (~1200%) y el siguiente upload no avanzo mientras el job
  corria (servicio ocupado, sin cola ni aislamiento).
- El unico recurso fue reiniciar `exam_app` (mata el job a mitad, deja el
  material sin indexar y sin aviso).
- PDF realista de 5.4 MB (40 paginas + padding): ~20 min de indexacion,
  211 chunks, toast "211 chunks indexed" y RAG respondiendo con el material
  (C2 PASS en el caso nominal de tesis, ver test-plan ronda 6).

## Causa

`POST /api/files` -> `LocalFileService.upload` -> `extract_file_text` ->
`index_text_for_subject` corre sincronico dentro del request HTTP: sin
limite de paginas/chunks/tamano logico, sin job en background con estado,
sin eventos de progreso intermedios (el SSE solo publica al FINAL), sin
cancelacion y sin control de concurrencia (2 uploads compiten por el mismo
servicio de embeddings). El frontend muestra el spinner generico sin ETA.

## Fix y verificacion

Pendiente. Recomendacion (RFC-13 propuesta): validar tamano logico del
material (paginas/chunks estimados) en el endpoint y rechazar con 413/422
accionable lo que exceda la capacidad declarada; mover la indexacion a un
job con estado consultable y evento `material_index_progress` por batch;
permitir cancelar (flag en DB o pubsub). Verificacion: subir el PDF de
8000 paginas y confirmar rechazo accionable (o indexacion en background con
progreso y cancelacion efectiva).

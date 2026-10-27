---
id: IMPL-023-ronda-qa-6-certificacion
tipo: Implementation
type: Implementation
title: QA ronda 6 - certificacion RC3 en navegador y API
description: Verificacion browser/API de BUG-016, BUG-018, RFC-10/11, C2 con PDF grande real y regresiones; hallazgos BUG-019/020/021.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BL-008, BL-014]
status: draft
---

## Alcance

Incluye: certificacion E2E de RC3/develop con stack levantado - sondas HTTP
reales de BUG-018 via nginx, verificacion en navegador de RFC-10 (materia
activa tras reload), RFC-11 (abort + Retry + rehidratacion) y BUG-016
(3 restarts de exam_app sin 401), C2 con PDF grande real, regresiones
R1/R2/R4/R5/R6, documentacion de hallazgos (BUG-019/020/021), decisiones
abiertas (DEC-001/002/003) y actualizacion de .ops.

No incluye: fixes de codigo de los bugs nuevos (post-RC3, DEC-001/002/003
pendientes del propietario), BL-010 Playwright suite, limpieza de datos de
prueba mas alla de artefactos temporales.

## Diseno

Ejecucion contra el stack Docker del proyecto (`docker` compose, 6+1
contenedores healthy) con cuenta QA dedicada
(qa-r6@usfq.test / materia "QA R6 Certificacion", id
`54cd0d29-1470-40db-b603-4e4a65c406da`) y thread dedicado
(`0afd6caa-3b7f-49db-951d-64387cfe176a`), para no contaminar datos de
profesores reales. El abort de stream se propago parcheando `window.fetch`
con AbortController (patron `__r6RealFetch`/`__r6Abort` a ~1.5 s) para
provocar el fallo de red real que dispara el camino de Retry (C8/RFC-11).
PDF grande generado con reportlab (40 paginas de texto real + padding de
comentario % antes del trailer, 5.4 MB) y validado con PyMuPDF dentro del
contenedor.

Pasos y resultados (evidencia en `.ops/qa/test-plan.md` ronda 6 y BUGs):

1. Precondiciones: 6 contenedores healthy; login QA OK; materia activa.
2. BUG-018 sondas: raiz 422 (antes 200 silencioso), metadata anidada 200
   con num_versions=2 y 4 PDFs + ZIP. PASS.
3. RFC-10: hard reload conserva "QA R6 Certificacion" en el selector y los
   contadores (localStorage `mvp_active_subject`). PASS.
4. RFC-11: abort -> burbuja failed + Retry -> turno completo, contenido
   rehidratado desde el checkpointer sin duplicar la respuesta. PASS.
5. BUG-016: 3 restarts de exam_app con sesion activa -> 0 401 (retry
   RFC-12). PASS. Nota menor: pendingQuestion del store se pierde (el
   contenido del turno sobrevive en el checkpointer).
6. C2: PDF 5.4 MB sin 413 -> 211 chunks indexados (~20 min), RAG responde
   citando el material. PASS nominal. El caso extremo (6.86 MB / 8000
   paginas) destapo BUG-020 (~29 h embeddings, sin progreso/cancelacion).
7. Regresiones: R1 PASS (save HITL verified-by-human), R2 PASS (guardrail
   anti-borrado), R4 PASS (export XLSX por chat; auto-attach fallo, link
   OK), R5 PASS (llm_responses 3250 filas, thread trazado), R6 PASS
   (toggle ES/EN persistente).
8. Hallazgos documentados: BUG-019 (HUMAN duplicado en checkpointer tras
   Retry - mecanismo confirmado en `langgraph_engine._initial_state` +
   reducer `add_messages`), BUG-021 (persist=false persiste igualmente la
   fila del examen/PDFs/ZIP - `nodes.py` ~627 incondicional).

Rollback: no aplica (cambios documentales; sondas con datos QA desechables).

## Pruebas

Casos positivos: C21-C24, C2 nominal, R1/R2/R4/R5/R6 (ver test-plan ronda 6).
Casos de rechazo verificados: BUG-018 sonda raiz 422; guardrail R2 (sin
DELETE); C2 sin 413 hasta 100 MB (nginx client_max_body_size).
Pendiente del propietario: cerrar DEC-001/002/003 y marcar
BUG-019/020/021 con fix/verificacion.

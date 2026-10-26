---
id: IMPL-021
tipo: Implementation
type: Implementation
title: Ronda QA 5 - verificaciones API tras nuevo instruccionado
description: Pruebas de regresion y de borde via nginx; BUG-017b verificado, BUG-018 abierto.
estado: borrador
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [BUG-017b, BUG-018, IMPL-019]
status: draft
---

## Objetivo

Tras el nuevo instruccionado (commit 166c71e), ejecutar una ronda de
regresion API-centrada que cubra routing nginx, auth, multi-tenancy,
validaciones, generacion E2E, descarga de artifacts y el fix de BUG-017b,
documentando hallazgos nuevos.

## Cambios

Ronda 5 (2026-10-26) - stack exam_* (frontend 200, /health 200, latex 422
alive, embedding 200):

- Routing nginx: /subjects (Accept json) -> 401 proxied; SPA fallback 200 en
  /subjects, /questions, /exams; OPTIONS 200; HEAD 200; /output/missing 404;
  /subjects-api con token invalido -> 401.
- Auth: /auth/me sin token -> 401; registro de sonda OK.
- Multi-tenancy: sonda solo ve los 5 subjects de clones Eva/Maria/Sofia/
  Lucia/Pablo (aislamiento OK).
- Validacion: POST /exams/generate sin campos -> 422 con errores accionables
  (C12 OK).
- Generacion E2E con banco vacio: 16 llamadas LLM, 8 items, 0 rechazos,
  2 PDFs compilados (A respondido/no respondido), zip 200 (101 KB) via
  /output; persistencia 16 preguntas y 2 exams en BD.
- Regresion BUG-017b: PUT /questions-api/{id}/verification
  {"verified":true} -> 200; toggle {"verified":false} -> 200. Fix se sostiene.
- Hallazgos: BUG-018 (campos desconocidos del blueprint descartados en
  silencio: `num_versions`/`name` en la RAIZ se aceptan sin 422 y se
  ignoran; anidados en `blueprint.metadata` funcionan - sondas 1 y 2
  contrastadas, ver defecto); GET /subjects/{id} 404 (solo /questions y
  /exams sub-rutas, por diseno); DELETE /subjects/{id} 404 (sin endpoint
  de borrado, gap menor); /questions raiz 404 y PATCH 405 (solo PUT
  verification y DELETE, API minima). Nombre del examen: hereda el del
  subject solo cuando `metadata.name` viene vacio (comportamiento por
  diseno, verificado en `nodes.py` persist node).
- Regresion BUG-017 (UI scroll) no ejecutable en ronda API-centrada;
  verificado en ronda 4.
- C2 (PDF 29 MB) no reejecutado; pendiente re-test directo.

Limpieza: sonda DB purgada (2 exams, 15 preguntas, 1 subject); artifacts
QA_Round5_Subject* y QA_R5_Nested* en data/agent_outputs a eliminar
manualmente; usuario qa.invalid@example.com conservado para rondas futuras.

Confirmacion de num_versions (sonda 2): con `blueprint.metadata.
{title,name,num_versions:2}` el pipeline genera 2 versiones (4 PDFs A/B
respondido/sin respuestas), zip 130 KB via /output, `num_versions=2` y
nombre personalizado en BD. Contrato correcto documentado; BUG-018 queda
como endurecimiento (extra=forbid) y no como fallo funcional.

## Aceptacion

- BUG-017b verificado (estado verificado).
- BUG-018 abierto con evidencia.
- Sin regresiones nuevas en routing, auth, aislamiento, validacion ni
  descarga.

---
id: BL-006
tipo: BacklogItem
type: BacklogItem
title: Idioma del contenido de preguntas como parametro
description: content_language en/es en el blueprint, alineado con el template LaTeX.
estado: idea
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [REQ-001]
status: draft
---

## Descripcion

El contrato del generador dice "ALWAYS answer in ENGLISH" pero varios items llegaron con
enunciado/opciones en espanol (ISS-05, ronda 1; inconsistente con la regla declarada y el
template LaTeX en ingles). RFC-07: anadir `content_language: en|es` al blueprint y al
prompt de `generate_question`; el template ya es bilingue via babel; default `en`
configurable por materia. Post-V1.

## Criterio de salida

El idioma del enunciado y opciones sigue el parametro configurado por materia; prompt y
template alineados.

## IMPL

IMPL-013
---
id: BL-013
tipo: BacklogItem
type: BacklogItem
title: Preview en navegador del PDF de examenes multiversion
description: Se valido el ZIP en rondas previas; el preview del PDF en navegador no.
estado: idea
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [REQ-001]
status: draft
---

## Descripcion

El backlog post-ronda 4 (P3) pide confirmar visualmente el PDF de un examen multiversion:
las rondas previas validaron la descarga del ZIP con versiones con/sin respuestas, pero
el renderizado del PDF dentro del navegador no se verifico.

## Criterio de salida

Abrir el PDF de cada version desde la vista Exams en Chrome/Firefox muestra el examen
compilado correctamente (portada, preguntas, paginacion).

## IMPL

IMPL-019
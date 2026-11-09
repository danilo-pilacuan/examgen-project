---
id: BL-009
tipo: BacklogItem
type: BacklogItem
title: Calidad UX menor del frontend (cursor, chips, nombres de examen)
description: ISS-12/14/15/16 de la ronda 3: cursor de streaming, chips en Subjects, desambiguacion de examenes.
estado: idea
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [REQ-001]
status: draft
---

## Descripcion

Cuatro issues P2 de la ronda 3 agrupados por ser cambios de UI pequenos: ISS-12 el cursor
de streaming bloquea clicks en widgets (pointer-events/z-index); ISS-14 indicar "2/3
preguntas" cuando el examen tiene menos de las solicitadas; ISS-15 desambiguar examenes
con el mismo nombre en la vista Exams; ISS-16 chips de contexto tambien en la vista
Subjects.

## Criterio de salida

Los cuatro comportamientos verificados en navegador; sin regresiones en las vistas
tocadas.

## IMPL

IMPL-016
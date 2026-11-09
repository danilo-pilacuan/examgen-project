---
id: BUG-009
tipo: Defect
type: Defect
title: Contador de preguntas del header no se refresca al cambiar de materia
description: Los chips de contexto mostraban el valor de la materia anterior hasta recargar la vista.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): al activar "Base de Datos" (0 preguntas en ese momento) el header
siguio mostrando "31 questions" (valor de Economia Aplicada); recien se actualizo al
recargar la vista.

## Causa

El contador de la barra de contexto no reaccionaba al `activeSubjectId` (no re-consultaba
el banco al cambiar la materia).

## Fix y verificacion

Cubierto sin codigo nuevo (RFC-06): `AppHeader.onSubjectChange` ya re-fetch-ea
`bank`/`material`/`exams` al cambiar de materia y los chips leen de esos stores.
Verificado en ronda 3 (C10): cambiar de materia refresca los contadores (21 questions /
14 chunks al volver a Base de Datos).
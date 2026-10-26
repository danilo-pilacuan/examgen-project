---
id: BUG-017
tipo: Defect
type: Defect
title: Sin scroll en vistas con contenido mayor al viewport
description: El contenido que excedia la primera pantalla era inaccesible en Exams/Bank/Subjects/Material.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [QT-004, IMPL-019]
status: stable
---

## Evidencia

Ronda 4 (2026-10-26, reportado por el usuario): en Exams, Bank y otras vistas, las listas
que exceden el alto del viewport no scrollean; examenes/preguntas fuera de la primera
pantalla inaccesibles. Severidad alta (bloquea uso real con muchas entradas).

## Causa

`.main-view` (contenedor principal del layout global `AppHeader.vue`) tenia
`overflow: hidden`; las vistas hijas no definen scroll propio, asi que todo lo que
excedia el viewport se recortaba.

## Fix y verificacion

`overflow: hidden` -> `overflow-y: auto` en `.main-view` (marcado con comentario BUG-17);
el Chat no se ve afectado (`MessageList` tiene su propio overflow interno). Verificado
con Playwright: Exams (1395px vs 619px viewport, submit alcanzable), Bank (21 filas, fila
21 visible), Subjects (643px, lista completa); scrollTop avanza y overflow-y=auto en
todas.
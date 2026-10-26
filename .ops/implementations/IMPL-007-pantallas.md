---
id: IMPL-007
tipo: Implementation
type: Implementation
title: Pantallas
description: Subjects, Material, Bank, Exams y Chat completas con selector reactivo.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-17
relaciona: [BL-001, IMPL-005, IMPL-011]
status: stable
---

## Alcance

Incluye: las 5 pantallas del profesor (Subjects con registro/activacion de materias,
Material con subida e indexacion, Bank con filtros y toggle de verificacion, Exams con
formulario y descarga ZIP, Chat con stream del agente) y la sincronizacion del selector
de materia entre navbar y vistas. No incluye: auth multitenant (IMPL-011).

## Diseno

El layout global vive en AppHeader (header + nav + subject picker + context bar + main);
el overflow del main-view fue corregido en BUG-017 (overflow-y auto). Los contadores del
context bar reaccionan al cambio de materia (BUG-009). Verificado E2E; la matriz de
scroll de la ronda 4 certifica las 5 vistas.
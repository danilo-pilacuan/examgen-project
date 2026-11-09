---
id: IMPL-005
tipo: Implementation
type: Implementation
title: Frontend base
description: Vue 3 + Vite + Pinia con i18n en/es, api client y layout base.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-17
relaciona: [BL-001, IMPL-006, IMPL-007]
status: stable
---

## Alcance

Incluye: proyecto Vue 3 + Vite + Pinia, i18n en/es, cliente HTTP (`api/http.ts` con
apiFetch + auth), router con vistas base y proxy nginx de desarrollo. No incluye:
widgets de chat (IMPL-006) ni pantallas completas (IMPL-007).

## Diseno

`apiFetch` centraliza auth, Accept: application/json (anadido en BUG-015) y mensajes
accionables (friendlyHttpMessage, BUG-012). Las vistas consumen stores Pinia que
re-fetch-ean al cambiar `activeSubjectId`. Verificado E2E en todas las rondas QA.
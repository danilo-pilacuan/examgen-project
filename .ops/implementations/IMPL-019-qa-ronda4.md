---
id: IMPL-019
tipo: Implementation
type: Implementation
title: QA ronda 4 - scroll global + toggles Bank via nginx
description: Playwright E2E tras los fixes BUG-017 (scroll) y BUG-017b (rewrite nginx); matriz de 10 casos.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [QT-004, IMPL-016, IMPL-018]
status: stable
---

## Alcance

Incluye: QA E2E con navegador integrado (Playwright) de todas las vistas tras el fix del
scroll global (BUG-017, overflow-y en .main-view) y del routing nginx del toggle de
verificacion (BUG-017b, rewrite /questions-api conserva prefijo), con matriz de 10 casos
(login, materia activa, scroll en 4 vistas, toggle bidireccional, 12 examenes, formulario
alcanzable con scroll, material indexado, 7 materias, chat con tools). No incluye: suite
versionada (BL-010), ISS-17/18 (BL-008/BL-011).

## Diseno

Leccion central de la ronda: el routing condicional por Accept (BUG-015) exige tests de
TODOS los metodos HTTP de cada prefijo; un rewrite gemelo mal copiado rompio el PUT sin
afectar los GET. Regla QA: probar cada endpoint REST por su ruta real via nginx, no solo
via TestClient. Resultado: P1 vacio (RC2 mantiene su certificacion E2E); backlog P2/P3
actualizado (BL-010..BL-013). Evidencia en `../qa/BUG-017*.md`.
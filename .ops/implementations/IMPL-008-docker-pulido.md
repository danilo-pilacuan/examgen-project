---
id: IMPL-008
tipo: Implementation
type: Implementation
title: Docker pulido
description: Compose con 6 servicios healthy y orquestacion completa del stack.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-18
relaciona: [BL-001, IMPL-002, IMPL-005]
status: stable
---

## Alcance

Incluye: `docker/docker-compose.yml` con exam_frontend (:3000), exam_app (:8000),
exam_postgres_db (:5432), exam_latex_compiler, exam_embedding_service y exam_open_webui,
todos healthy con datos de prueba reales. No incluye: CI de images (IMPL-001).

## Diseno

nginx va horneado en la imagen de frontend: cualquier cambio de conf exige rebuild (en
BUG-017b el rebuild fue parte del fix). Los containers usan policy=always (en campanas
largas los reinicios del host los levantan solos, pero matan runs en curso; gotcha de la
etapa 15). Verificado: stack 6/6 healthy en las 4 rondas QA.
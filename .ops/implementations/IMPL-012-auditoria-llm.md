---
id: IMPL-012
tipo: Implementation
type: Implementation
title: Auditoria raw LLM + JSON en ingles
description: Tabla llm_responses con raw answer/thinking/latencia y artefactos JSON del pipeline en ingles.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [BL-002, IMPL-004]
status: stable
---

## Alcance

Incluye: auditoria completa de llamadas LLM en `llm_responses` (prompt, raw_answer,
thinking, latencia, contexto), JSON de artefacto del pipeline en ingles con
`rejection_log` + `total_llm_calls` (anadidos en BUG-004), y las telemetria usada por el
framework de evaluacion (IMPL-018). No incluye: dashboards de analisis (fuera de alcance).

## Diseno

La correlacion posicional de la etapa 15 extrae quality_score real correlacionando
respuestas crudas del evaluador/generador con los intentos. Verificado: R6 en rondas 1 y
3 (54-85 filas nuevas por sesion QA); 85 filas al cierre del RC1.
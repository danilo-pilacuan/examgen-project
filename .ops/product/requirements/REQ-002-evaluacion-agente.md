---
id: REQ-002
tipo: Requirement
type: Requirement
title: Evaluacion y benchmark del agente generador
description: Framework reproducible para medir capacidad, consumos y robustez del agente para la tesis.
estado: aprobado
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [BL-019, BL-020]
status: stable
sources: [{ id: copilot-instructions, resource: ../../.github/copilot-instructions.md, title: copilot-instructions }]
---

## Requisito

El framework de evaluacion (etapa 15, `test/evaluation/`) debe comparar capacidad
(aprobacion, calidad, alineacion Bloom), medir consumos (llamadas/tokens/latencia por
item), optimizar hiperparametros con diseno OFAT y aplicar metricas SOTA de agentes
(self-consistency, pass@k, robustez entre clones, faithfulness RAG), con un registro
central multi-proveedor (`models.yaml`) para reproducibilidad al cambiar de modelo.

## Criterio de aceptacion

Campana real de 102 runs (E01-E04) con las hipotesis H1-H5 resueltas y configuracion de
produccion validada empiricamente (T gen=0.7, top_k=3, T eval=0.2). Evidencia:
`test/evaluation/experiments/E0*/FINDINGS.md` y agregados versionados.

## No objetivos

Costos local vs nube (elemento #6, descartado) y tests automatizados del framework (opcional).
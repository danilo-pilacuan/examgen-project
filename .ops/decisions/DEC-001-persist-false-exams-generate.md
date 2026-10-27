---
id: DEC-001
tipo: Decision
type: Decision
title: ¿Que hace POST /exams/generate con persist=false (BUG-021)?
description: Decidir si persist=false respeta el flag (a) o se elimina el flag y toda generacion persiste (b).
estado: abierta
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BUG-021, IMPL-021, REQ-001]
status: draft
---

## Pregunta

El endpoint `POST /exams/generate` acepta `persist: bool = True`, pero el nodo
de finalizacion persiste SIEMPRE la fila del examen + PDFs + ZIP
(`nodes.py` ~627); el flag solo controla guardar las preguntas aprobadas.
El docstring del listado dice "every generation is persisted" (peticion del
profesor). ¿Respetamos el flag (a) o lo quitamos y documentamos que toda
generacion persiste (b)?

Fase en que se necesita: implementacion post-RC3 (bug abierto de la ronda 6).
Opciones (max 6 lineas):
- (a) Respetar flag: persist=false omite fila BD + PDFs + ZIP. Riesgo: rompe
  la expectativa del profesor de que todo examen queda en la vista Exams;
  requiere plumar el flag por todo el pipeline.
- (b) Quitar el flag del schema (breaking change REST) y documentar. Riesgo:
  clientes que hoy envian persist=false verian error 422; cambio de contrato.
Resolucion: (vacia, abierta al propietario)

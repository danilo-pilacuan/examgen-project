---
id: DEC-003
tipo: Decision
type: Decision
title: ¿Limites y estrategia de indexacion para material grande (BUG-020)?
description: Elegir entre rechazo preventivo por tamano logico, indexacion en background con progreso/cancelacion, o ambos.
estado: abierta
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BUG-020, BUG-005, REQ-001]
status: draft
---

## Pregunta

La indexacion de material corre sincronica en el request de
`POST /api/files`: un PDF de 8000 paginas demanda ~29 h de embeddings en
CPU, satura el servicio, sin progreso ni cancelacion. ¿Que politica se
adopta?

Fase en que se necesita: implementacion post-RC3 (bug abierto de la ronda 6).
Opciones (max 6 lineas):
- (a) Solo rechazo preventivo: estimar chunks y devolver 413/422 accionable
  si excede un presupuesto (p.ej. > 30 min CPU). Riesgo: materia legitima
  grande queda sin soporte.
- (b) Solo background: job con estado consultable + evento
  material_index_progress + cancelacion. Riesgo: sigue siendo ~29 h para el
  caso extremo, costo no acotado.
- (c) Ambos: presupuesto maximo + background con progreso. Riesgo: mas
  codigo; requiere decidir el presupuesto con el profesor.
Resolucion: (vacia, abierta al propietario)

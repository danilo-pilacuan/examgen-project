---
id: DEC-002
tipo: Decision
type: Decision
title: ¿Como deduplicar el mensaje HUMAN del Retry (BUG-019)?
description: Elegir entre dedupe por contenido en el endpoint (a), id determinista para add_messages (b) o reanudar el turno (c).
estado: abierta
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BUG-019, IMPL-022]
status: draft
---

## Pregunta

Tras un abort + Retry, el HUMAN queda duplicado en el checkpointer porque
`_initial_state` reinserta `{"role":"user","content":message}` en cada POST
y el reducer `add_messages` anade sin dedupe. ¿Que estrategia se adopta?

Fase en que se necesita: implementacion post-RC3 (bug abierto de la ronda 6).
Opciones (max 6 lineas):
- (a) Dedupe en el endpoint de stream: si el ultimo mensaje persistido del
  hilo es el mismo HUMAN, omitir reinserccion. Riesgo bajo, no cambia el
  contrato SSE; caso raro: usuario legitimo repite texto identico y no se
  reinserta (aceptable).
- (b) `id` determinista (hash thread+contenido) para upsert. Riesgo: cambia
  semantica de add_messages y requiere mapear ids estables entre turnos.
- (c) Reanudar el turno previo en vez de reenviar. Riesgo: acopla el
  frontend al estado del graph, mayor complejidad.
Resolucion: (vacia, abierta al propietario)

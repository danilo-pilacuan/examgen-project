---
id: DEC-004
tipo: Decision
type: Decision
title: ¿Como cerrar la brecha de propiedad y listado de hilos de chat (BUG-022/023)?
description: Elegir entre tabla threads con owner (a), extraer owner del primer checkpoint (b) o bloquear historial sin tabla (c).
estado: abierta
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BUG-022, BUG-023, BL-017, IMPL-024]
status: draft
---

## Pregunta

Los hilos no registran propietario: cualquiera autenticado lee/escribe el
hilo de otro (BUG-022) y el listado vive en localStorage (BUG-023, reporte
"no veo conversaciones pasadas"). ¿Que estrategia se adopta?

Fase en que se necesita: fix post-RC3 (P1, seguridad multitenant).
Opciones (max 6 lineas):
- (a) Tabla `threads` (thread_id, user_id, titulo, updated_at) + endpoint
  GET /api/chat/threads + validacion 403 en stream/invoke/history; cierra
  BL-017 y BUG-022/023 de una vez. Riesgo: migracion de hilos existentes.
- (b) Sin tabla nueva: resolver owner desde el primer checkpoint del hilo
  y listar hilos agregando checkpoints por usuario. Riesgo: consultas por
  checkpoint_blobs frágiles, sin titulos ni orden fiable.
- (c) Solo bloquear history/stream/invoke con ownership derivado de (b) y
  dejar el listado en localStorage. Riesgo: BUG-023 sigue abierto.
Resolucion: (vacia, abierta al propietario)

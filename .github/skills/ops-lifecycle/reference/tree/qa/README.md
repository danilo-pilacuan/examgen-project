---
id: qa-readme
tipo: Guide
type: Guide
title: QA - calidad y trazabilidad
description: Estrategia de pruebas, matriz de trazabilidad y defectos.
estado: vigente
dueno: rol:propietario
fecha: 2026-06-15
relaciona: [ops-readme]
status: stable
verified: 2026-06-15T00:00:00Z
sources: [{ id: agents-md, resource: ../../AGENTS.md, title: AGENTS.md v3 }]
---

- **Proposito:** definir que se prueba y como (seccion 9), mantener la trazabilidad REQ-IMPL-QT y registrar defectos.
- **Escribe:** rol:agente (ejecuta y registra) · **Aprueba:** rol:propietario (estados verificados).
- **Cuando:** al escribir pruebas de una fase (antes de implementar, regla 3) y al cerrar fase.

## Documentos

- [strategy.md](strategy.md) - alcance, reglas de ejecucion y cuadro de mando por fase.
- [traceability.md](traceability.md) - matriz de cobertura con evidencia de ejecucion.

## Defectos

Los BUG se abren como archivos `BUG-NNN.md` con la plantilla [../templates/defect.md](../templates/defect.md) y se listan aqui. Hoy no hay BUG abiertos: los fallos detectados durante las fases 0-4 (RLS con superusuario, defaults de conexion) se resolvieron en la misma fase y quedaron registrados en [../../PROGRESS.md](../../PROGRESS.md).

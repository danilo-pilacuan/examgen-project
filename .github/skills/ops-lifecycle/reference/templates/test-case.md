---
id: TEMPLATE-QT
tipo: Template
type: Template
title: Plantilla de caso de prueba (QT)
description: Modelo para qa/test-cases/QT-NNN.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: QT-000
tipo: TestCase
type: TestCase
title: <Nombre de la prueba>
description: <Una linea>
estado: pendiente          # pendiente | aprobada | fallida
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: [REQ-000]       # regla de trazabilidad: todo QT enlaza un REQ
status: draft
fase: <0-5>
---

## Objetivo

<Que verifica; deriva de la seccion 9 de AGENTS.md con su numero citado. Precondiciones si aplica.>

## Caso que debe pasar

<Pasos y resultado esperado.>

## Caso que debe ser rechazado

<Regla 3 de la seccion 0: toda prueba incluye un caso adversarial.>

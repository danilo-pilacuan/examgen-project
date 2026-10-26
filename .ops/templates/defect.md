---
id: TEMPLATE-BUG
tipo: Template
type: Template
title: Plantilla de defecto (BUG)
description: Modelo para qa/defects/BUG-NNN.md.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

---
id: BUG-000
tipo: Defect
type: Defect
title: <Fallo observado>
description: <Una linea>
estado: abierto            # abierto | corregido | verificado
dueno: rol:propietario
fecha: <YYYY-MM-DD>
relaciona: [QT-000]        # QT que lo detecto
status: draft
---

## Evidencia

<Salida real de la prueba o comando; regla 8 de la seccion 0: nunca afirmar sin ejecutar.>

## Causa

<Analisis; si revela una contradiccion de AGENTS.md, regla 4 de la seccion 0: reportar, no adaptarse en silencio.>

## Fix y verificacion

<Que cambio y que prueba lo confirma; rollback si aplica.>

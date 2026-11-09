---
id: IMPL-016
tipo: Implementation
type: Implementation
title: QA ronda 3 - navegador (certificacion del caso de uso central)
description: Certifica los fixes de rondas 1-2 E2E; 2 bugs nuevos (BUG-015/016) corregidos en la sesion.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-23
relaciona: [QT-003, IMPL-014]
status: stable
---

## Alcance

Incluye: E2E manual del MVP desde el frontend dockerizado actuando como profesor real,
certificando los fixes 11.1-11.6 y los P0 de la ronda 1 (C1, C5-C13, R1-R7 pendientes de
la etapa 11), con re-verificacion de BUG-013/014. Regla de la sesion: toda interaccion
exclusivamente por navegador + Playwright. No incluye: BUG-016 (abierto, RFC-12 en
BL-008).

## Diseno

Resultado: los fixes de las rondas 1-2 funcionan de punta a punta; el caso de uso central
esta certificado. 2 bugs nuevos detectados y corregidos en la misma sesion: BUG-015
(nginx sombreaba la SPA de /subjects; routing por Accept) y BUG-016 (401 transitorio tras
reiniciar exam_app, abierto como menor). Metricas: 21 preguntas y 12 examenes en BD al
cerrar; 54 filas nuevas en llm_responses; 4 rebuilds Docker. Detalle por bug en
`.ops/qa/`.
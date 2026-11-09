---
id: QT-007
tipo: TestCase
type: TestCase
title: Recertificacion ronda 7 - funcionales Playwright e integracion API/nginx/BD
description: C25-C40 y R2 sobre stack real; sin unitarias; detecta BUG-022/023/024/025.
estado: pendiente
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [REQ-001]
status: draft
fase: 6
---

## Objetivo

Recertificar el producto tras RC3 (mandato del propietario): funcionales con
Playwright en navegador real y de integracion contra API/nginx/Postgres, sin
unitarias. Deriva de la seccion 0 (validacion obligatoria) y la estrategia
QA (navegador real, nunca solo curl).

## Caso que debe pasar

- C26/C27/C33: hilos listados e hidratados en el mismo navegador, tras
  logout/login y tras reload duro.
- C28-C32: banco (filtros + toggle), examenes, material, materias, chat con
  materia activa.
- C34: ruta anonima -> /login?redirect=/; login valido entra.
- C36-C38: aislamiento 403, auth 422/409/401/200, guardrail de borrado.
- R2: guardrail anti-borrado de verificadas via API (403).

## Caso que debe ser rechazado

- C25: limpiar `mvp_chat_threads` + reload NO debe vaciar el historial
  (fallo real -> BUG-023, el bug reportado).
- C35: usuario B NO debe poder leer ni escribir el hilo de A (fallo real
  -> BUG-022 critico; evidencia API + visual).
- C39: nginx debe emitir cabeceras de seguridad (fallo real -> BUG-024).
- C34b: password invalida debe mostrar mensaje de credenciales (fallo
  real -> BUG-025).

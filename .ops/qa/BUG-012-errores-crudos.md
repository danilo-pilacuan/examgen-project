---
id: BUG-012
tipo: Defect
type: Defect
title: Errores de subida muestran el texto crudo del status HTTP
description: Sin codigo ni guia; el profesor no sabia que hacer ante un 413/401/403.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): la vista Material mostraba "Request Entity Too Large" (texto del
status line, sin codigo ni guia) al fallar una subida.

## Causa

`MaterialView.vue` (`uploadMessage`) usaba el mensaje crudo del error HTTP.

## Fix y verificacion

Fix 11.5: `friendlyHttpMessage()` en `http.ts` mapea 413/401/403 a mensajes accionables
(en/es) y banner `.form-error` en ExamsView con el detalle del backend (cubre ISS-07).
Verificado en ronda 3 (C12): subida de 101 MB -> "El archivo supera el tamano maximo
(100 MB). Divide el material en capitulos o archivos mas pequenos."; fallo del formulario
de Exams -> banner con detalle.
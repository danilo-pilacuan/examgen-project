---
id: BUG-005
tipo: Defect
type: Defect
title: Subida de material mayor a 1 MB falla con 413
description: El profesor no podia indexar material real; limite por defecto de nginx.
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): subir PDF de 3.1 MB (Foundations of Databases, libro completo)
desde la vista Material -> `413 (Request Entity Too Large)`; la UI muestra el texto crudo
"Request Entity Too Large" sin guia. Hubo que trocear el libro en capitulos.

## Causa

`client_max_body_size` de nginx por defecto = 1m; el backend no revisaba su propio limite
con mensaje accionable.

## Fix y verificacion

RFC-01: `client_max_body_size 100m;` en el server de nginx. Verificado en ronda 3 (C12,
lado del error): PDF de 101 MB -> 413 capturado y mostrado como "El archivo supera el
tamano maximo (100 MB). Divide el material en capitulos o archivos mas pequenos."
Re-test con PDF grande real (C2) queda pendiente de certificacion directa.
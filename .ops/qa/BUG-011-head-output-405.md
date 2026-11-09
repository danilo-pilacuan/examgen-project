---
id: BUG-011
tipo: Defect
type: Defect
title: HEAD /output/{file} devuelve 405
description: Solo GET registrado; rompia pre-chequeos de descarga (gestores/antivirus).
estado: verificado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [QT-001, IMPL-013]
status: stable
---

## Evidencia

Ronda 1 (2026-10-19): `HEAD /output/Parcial_1.zip` -> 405 (solo GET registrado); smoke
2026-10-22 lo confirmo en vivo (`allow: GET`). Impacto menor: rompe pre-chequeos de
descarga que hacen HEAD.

## Causa

`exam_app/main.py` registraba solo `@app.get("/output/{filename}")`.

## Fix y verificacion

Fix 11.4: `@app.api_route("/output/{filename}", methods=["GET","HEAD"])`. Verificado en
ronda 3 (C11): `HEAD /output/QA_Rebuild_-_Examen_1.zip` -> 200 (directo y via nginx); GET
incluye `Content-Disposition: attachment` (ISS-06 cubierto por `FileResponse`).
---
id: BUG-031
tipo: Defect
type: Defect
title: La fecha verified_at no se reflejaba al verificar en el Bank sin recargar
description: setHumanVerification en stores/bank.ts descartaba la respuesta del PUT y parcheaba solo verified_by_human; verified_at y created_at quedaban obsoletos hasta recargar la tabla.
estado: corregido
dueno: rol:propietario
fecha: 2026-11-06
relaciona: [QT-015, IMPL-031, BL-023]
status: draft
---

## Evidencia

Reporte del propietario (2026-11-06): al verificar una pregunta en Bank la
columna de fecha no cambiaba. Reproduccion pre-fix en
http://localhost:3000/bank (materia "Economia Aplicada - QA11"): toggle
Verify dejaba la celda en "-" y el badge "Pending" hasta recargar la tabla;
la respuesta del PUT ya traia el QuestionOut actualizado.

## Causa

stores/bank.ts, setHumanVerification: hacia `await apiFetch(...)`
descartando la respuesta y luego parcheaba localmente solo
`q.verified_by_human = verified`. El backend PUT
/questions/{id}/verification (exam-app subjects.py) ya devuelve el
QuestionOut completo con verified_at y created_at; el store lo ignoraba.
No se detecto antes porque la ronda 14 valido las columnas nuevas con la
tabla ya renderizada tras recarga, no el toggle en caliente.

## Fix y verificacion

Fix: capturar la respuesta como Question y reemplazar el elemento del
array por indice (`this.questions[i] = updated`), patron de adoptar la
respuesta authoritative completa en vez de parchear campos sueltos.
Verificacion: vue-tsc y build-only verdes; imagen frontend reconstruida;
QA Playwright en ambos sentidos sin recargar - Verify muestra la fecha
(11/6/2026, 5:08:19 AM) y badge "Human" al instante; Remove vuelve a "-"
y "Pending" al instante; estado original restaurado.

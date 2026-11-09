---
id: BUG-030
tipo: Defect
type: Defect
title: Interpolacion i18n sin parametros renderiza hint "(of )" vacio
description: perTopicSum/perTopicTotalError en ExamsView.vue se llamaban sin el objeto {sum,total}; vue-i18n interpola a cadena vacia y el hint mostraba "...(of )".
estado: corregido
dueno: rol:propietario
fecha: 2026-11-06
relaciona: [QT-015, IMPL-031]
status: draft
---

## Evidencia

Ronda 15 (2026-11-06), Playwright contra http://localhost:3000/exams con
materia "Economia Aplicada - QA11": al abrir el panel avanzado con conteos
por tema, el hint bajo los selectores numericos renderizaba literal
"2 of 3 questions planned (of )" - el sufijo "(of )" vacio. La cadena
perTopicSum en i18n declara {sum} y {total} pero las llamadas t() del
template y de generate() no pasaban el objeto de parametros.

## Causa

ExamsView.vue: en el template, `t('exams.perTopicSum')` y
`t('exams.perTopicTotalError')` sin segundo argumento; en generate() lo
mismo para perTopicTotalError. vue-i18n no advierte en runtime visible:
sustituye el placeholder faltante por cadena vacia. Detectado por el QA de
ronda y no antes porque la ronda 14 valido la estructura del panel sin
inspeccionar el texto interpolado del hint.

## Fix y verificacion

Fix: pasar `{ sum: topicSum(), total: totalQuestions }` (template) y
`{ sum: topicSum(), total: totalQuestions.value }` (generate()) en las 3
llamadas; rebuild de la imagen frontend. Verificacion: hint renderiza
"(of 10)" con total=10; el caso de rechazo muestra el mensaje completo
"sum (60) exceeds exam total (10)". Regla derivada: cada placeholder de
una clave i18n exige su objeto de parametros en la llamada.

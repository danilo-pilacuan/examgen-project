---
id: BL-024
tipo: BacklogItem
type: BacklogItem
title: Exams - Bloom/dificultad como checkboxes y blueprint por tema
description: Feedback de Felipe (ronda 2 de la tercera revision): Bloom no debe ser un select (usar checkboxes) y el panel avanzado debe pedir cuantas preguntas por tema con selectores numericos, no pesos abstractos.
estado: hecho
dueno: rol:propietario
fecha: 2026-11-06
relaciona: [REQ-001, BL-023]
status: draft
---

## Descripcion

Feedback transmitido por el propietario (2026-11-06) sobre ExamsView.vue tras la
ronda 14: (1) los selects de Bloom y dificultad con presets son confusos; como
la aplicacion ya usa checkboxes para tipos de pregunta, Bloom debe ser tambien
un grupo de checkboxes sobre los niveles reales; (2) el panel "Advanced
blueprint" es tecnicamente correcto pero no humanamente intuitivo: en lugar de
distribuciones de peso por nivel, debe pedir "cuantas preguntas por tema" con
selectores numericos por cada tema real de la materia.

Alcance: solo frontend (ExamsView.vue + i18n EN/ES). El contrato del backend
(ExamBlueprint con bloom_distribution/difficulty_distribution/topics_weight)
no cambia: el frontend traduce la seleccion a la misma estructura.

Fuera de alcance: cambios de schema o planner; items A3/A4, B1/B2, C1-C5
(pospuestos en BL-023).

## Criterio de salida

Checkbox groups de Bloom (6 niveles) y dificultad (3 niveles) con distribucion
uniforme de lo marcado; selectores numericos por tema con guard de suma contra
el total del examen; caso de rechazo en UI (suma > total, 0 llamadas API);
generacion real en navegador POST 200; validacion estatica verde (vue-tsc,
build).

## IMPL

IMPL-031

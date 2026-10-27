---
id: IMPL-024-ronda-qa-7-recertificacion
tipo: Implementation
type: Implementation
title: QA ronda 7 - recertificacion funcional e integracion
description: Recertificacion con Playwright (funcional) y API/nginx/BD (integracion), sin unitarias; bug reportado de historial diagnosticado (BUG-023) y 3 hallazgos nuevos.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BUG-022, BUG-023, BUG-024, BUG-025, QT-007, DEC-004, BL-017]
status: draft
---

## Alcance

Incluye: plan de pruebas ronda 7 (funcionales Playwright en navegador real,
integracion API/nginx/Postgres, sin unitarias), diagnostico del bug
reportado ("no veo conversaciones pasadas" -> BUG-023 con causa raiz en
`useThreadId.ts` + BL-017), ejecucion de C25-C34 y R1-R2/R4, hallazgos
BUG-022/024/025, decision abierta DEC-004, limpieza de datos QA.

No incluye: fixes de codigo (post-RC3, DEC-001..004 pendientes del
propietario), suite versionada Playwright (BL-010), generacion E2E de
examen (omitida: LLM largo ya cubierto en C19 ronda 5 y C2 ronda 6).

## Diseno

Stack Docker healthy (nginx :3000 -> exam-app :8000 -> Postgres). Cuenta
qa-r7@usfq.test + usuarios de contraste qa-r7-b@usfq.test (API) y
qa-r7-ui-temp@usfq.test (navegador, borrado al cierre). Materia propia
"QA R7 Recert" + hilos de control ad0e765d y c35b172e. Flujo del reporte
reproducido limpiando `mvp_chat_threads` y reloggeando. Sondas de
integracion via PowerShell + nginx y directo a :8000, con trampas
conocidas: Accept json en /subjects y /questions, login con body JSON,
`docker exec ... psql -t -A` para escalares.

Pasos y resultados (evidencia en test-plan ronda 7 y BUGs):

1. BUG-023 diagnosticado: mismo navegador PASS; storage limpio -> sidebar 0
   aunque BD conserva los hilos (repro del reporte). Causa: listado solo en
   localStorage, sin endpoint de listado (BL-017).
2. BUG-022 confirmado: usuario B lee y escribe el hilo de A (API + visual
   en navegador con tercer usuario).
3. Funcionales PASS: banco (200 filas, filtros, toggle verificacion),
   examenes (listado + enlaces ZIP/PDF), material (chunks + botones),
   materias (creacion; sin delete en UI/API), chat con materia activa
   ("contexto-ok"), hidratacion de 2 hilos, logout/login, reload duro,
   toggle ES/EN, guardia de ruta anonima -> /login?redirect=/.
4. Integracion PASS: auth (422/409/401/200), aislamiento de materias
   (403 en preguntas/examenes/material ajenos), toggle + guardrail de
   borrado de verificadas (403), BUG-019 matizado (duplicado solo en
   Retry, hilo nuevo limpio).
5. Hallazgos: BUG-024 (sin cabeceras de seguridad), BUG-025 (mensaje 401
   enganoso en login), nota de semillas sin owner escribibles por todos.

Rollback: no aplica (ronda documental; datos QA desechables purgados:
materia "QA R7 UI Temp", usuario qa-r7-ui-temp; hilos de control
conservados como evidencia).

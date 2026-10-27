---
id: QT-009
tipo: TestCase
type: TestCase
title: Recertificacion ronda 9 - funcionales Playwright e integracion API/nginx/BD
description: Re-ejecucion de la certificacion tras las rondas 7-8; el agente actua como verificador humano en el navegador; incluye certificacion completa del flujo de examenes (C-E1..E5).
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [REQ-001]
status: draft
fase: 6
---

## Objetivo

Recertificar el producto tras el fix de BUG-022/BUG-023 (IMPL-025) y el anexo
UX del Banco: pruebas funcionales con Playwright en navegador real (el agente
actua como humano verificador) y de integracion contra API/nginx/Postgres, sin
unitarias. Incluye la certificacion del caso de uso de examenes (generacion,
ZIP, PDFs, descarga, BD) que las rondas 7 omitieron. Deriva de la seccion 0
(validacion obligatoria) y la estrategia QA (navegador real, nunca solo curl).

Precondiciones: stack Docker healthy (nginx :3000, exam-app :8000,
postgres :5432); usuarios de control qa-r7 (A) y qa-r7-b (B) con contrasenas
restablecidas en esta sesion; navegador integrado con la app abierta.

## Caso que debe pasar (funcionales, Playwright, navegador real)

- F1: login A -> redirige a /; se muestra el nombre del profesor.
- F2: Bancos: las 5 materias semilla de B listan sus preguntas; banco con
  200+ filas scrolleable; filtros dificultad y verificacion funcionan.
- F3: detalle expandible inline de fila (chevron rota, cierra con X/segundo
  clic, una sola seleccion) - anexo UX ronda 8 (C54).
- F4: toggle de verificacion Pending -> Human -> Pending desde la UI.
- F5: Examenes: listado de examenes previos con enlaces Download ZIP/PDF
  funcionales (HTTP 200, Content-Disposition).
- F6: Material: chunks visibles de la materia activa, botones Delete y
  Delete-all presentes.
- F7: Materias: crear una materia nueva via UI y quede seleccionada.
- F8: Chat con materia activa: indicador Context visible; respuesta del
  agente referenciando el asunto.
- F9: Sidebar de hilos: listado server-side con badges (materia + contador);
  click hidrata la conversacion; reload duro conserva la sesion y los hilos.
- F10: Logout/login conserva los hilos (mismo navegador).

## Caso que debe ser rechazado (adversariales)

- F11: ruta anonima -> /login?redirect=/; sin token no se ve contenido.
- F12: guardrail de borrado: eliminar una pregunta verificada por humano
  debe ser rechazado (403) via API y por el agente en el chat.
- F13: aislamiento: A no lista materias de B y viceversa (salvo legacy);
  hilo de A invisible para B.
- F14: login con password invalida muestra mensaje de credenciales
  (BUG-025 conocido, solo registro del texto).
- I-serie (integracion): 401 sin token en /api/chat/threads; 403 de B sobre
  el hilo de A (history/write/rename/delete); toggle PUT via nginx; headers
  de seguridad de nginx (BUG-024 conocido); auth 422/409/401.
- E-serie (certificacion de examenes): E1 generacion via formulario Exams;
  E2 ZIP con 2 versiones; E3 PDFs con/sin respuestas en /output; E4 examen
  visible solo en su materia; E5 pipeline sin items aprobados no publica.

## Resultado (2026-10-27, evidencia real)

- F1-F8, F10-F13: PASS (detalles en `test-plan.md`, Ronda 9).
- F9: PASS con BUG-026 (chips 0/0 tras login/Activate hasta re-seleccion
  manual del combobox; la hidratacion de hilos e historial si funciona).
- F14: BUG-025 sigue abierto (mensaje "Tu sesion expiro" con contrasena
  incorrecta; 401 real en consola).
- I1, I2, I3, I5, I6: PASS (401 sin token; 403 ownership; PUT verified
  200 + DELETE verificada 403; auth 422/422/401/200; aislamiento por
  propietario con legacy legible por diseno). I3 nota: el campo del body
  es `{"verified": bool}`, no `verified_by_human` (422 en ese caso).
- I4: FAIL conocido (BUG-024, las 5 cabeceras de seguridad ausentes).
- E1: PASS con nota (QA_R9_Cert: POST 200, 8 llamadas LLM, 1 rechazo por
  difficulty_mismatch, 3/4 items publicados, "indexed_chunks_count: 0"
  pese a 41 chunks en BD -> parte de BUG-027).
- E2, E3, E4: PASS (ZIP 175KB con A/B y A/B_respondido; PDF GET/HEAD 200
  con Content-Disposition attachment; examen visible en su materia,
  403 cruzado).
- E5: FAIL -> BUG-027 (materia 0 chunks/0 preguntas publica 2 preguntas
  genericas "Sahara Desert" con ZIP/PDF y persiste el examen).
- I8 (C11 re-check): HEAD 200 archivo existente; 404 inexistente.
- I9 (threads CRUD): POST/GET/PATCH/DELETE /api/chat/threads 200/200/200/
  204; history tras DELETE -> 404.

Estado: ejecutado (verificacion del propietario pendiente; nunca
auto-asignada por el agente). Datos de control r9 purgados salvo el examen
QA_R9_Cert (evidencia de certificacion) y el hilo 57a386a2 de A.

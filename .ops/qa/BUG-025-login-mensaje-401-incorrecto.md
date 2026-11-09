---
id: BUG-025
tipo: Defect
type: Defect
title: Login muestra "Tu sesion expiro" cuando la contrasena es incorrecta
description: El 401 de credenciales invalidas se mapea al mensaje de sesion expirada, confundiendo al usuario.
estado: abierto
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [QT-007, IMPL-024, BUG-012]
status: draft
---

## Evidencia

Ronda 7 (2026-10-27, Playwright en el formulario de login): enviar
qa-r7@usfq.test con contrasena invalida -> el formulario muestra
"Tu sesion expiro. Vuelve a iniciar sesion." en lugar de un mensaje de
credenciales invalidas (la consola registra el 401 real).

## Causa

`frontend/src/api/http.ts:74`: `friendlyHttpMessage()` mapea TODO 401 a
"Tu sesion expiro..."; el mapeo esta pensado para respuestas autenticadas
de la app, no para el POST /auth/login, donde 401 significa contrasena
incorrecta. Regresion menor del criterio C12 (errores accionables).

## Fix y verificacion

En la pantalla de login usar el `detail` del backend (o mapear 401 del
endpoint de login a "Email o contrasena incorrectos"). Verificacion:
contrasena invalida muestra el texto correcto; un 401 de token vencido
dentro de la app sigue mostrando el aviso de sesion expirada.

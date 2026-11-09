---
id: IMPL-026-ronda-qa-9-recertificacion
tipo: Implementation
type: Implementation
title: QA ronda 9 - recertificacion funcional e integracion con certificacion de examenes
description: Re-ejecucion de la certificacion con Playwright (el agente como verificador humano) e integracion API/nginx/BD; incluye el flujo de examenes E1-E5 que la ronda 7 omitio.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [BL-017, QT-009]
status: draft
---

## Alcance

Incluye: plan de pruebas ronda 9 (funcionales Playwright en navegador real,
integracion API/nginx/Postgres, sin unitarias), certificacion del caso de uso
de examenes (generacion, ZIP de 2 versiones, PDFs /output, propietario,
pipeline sin items), regresion de los fixes de BUG-022/BUG-023 (IMPL-025) y
del anexo UX del Banco (C54). El agente actua como humano verificador en el
navegador integrado, segun mandato del propietario.

No incluye: fixes de codigo (BUG-019/020/021/024/025 siguen con sus
decisiones o estado actual), suite versionada Playwright (BL-010), cambios a
AGENTS.md o scope.

## Diseno

Stack Docker healthy. Cuentas de control qa-r7 (A) y qa-r7-b (B) con
contrasenas restablecidas en sesion (misma via que ronda 7, sin endpoint de
reset). Datos semilla Economia Aplicada Eva/Lucia heredados de rondas
anteriores (owner NULL, visibles por el fallback legacy) para tener bancos
grandes (497 preguntas, 82 chunks) sin tocar datos del profesor real.
Navegador integrado con la app en http://localhost:3000; sondas de
integracion por PowerShell via nginx (:3000) y directo a :8000 cuando se
compara routing.

Pasos atomicos en orden:

1. Preparar datos: semillas ya presentes; contrasenas A/B; hilos de control
   de A creados via API con badge de materia.
2. Funcionales F1-F11 en navegador (login, bancos, filtros, detalle inline,
   toggle, examenes, material, materias, chat con contexto, sidebar hilos,
   reload duro, logout/login, guardia de ruta).
3. Adversariales F12-F14: guardrail de borrado, aislamiento, mensaje de
   login invalido.
4. Integracion I1-I6 por API via nginx: 401 sin token, 403 de B sobre hilo
   de A (history/write/rename/delete), toggle PUT, cabeceras nginx, auth
   422/409/401, aislamiento de materias.
5. Certificacion de examenes E1-E5: generacion via formulario Exams sobre
   materia semilla de B (banco grande), verificacion de ZIP (2 versiones),
   PDFs en /output (Content-Disposition, HEAD), propietario en la vista
   Exams y en BD, y rechazo sin items aprobados.
6. Limpieza: datos de control desechables (materia/hilos de la ronda)
   purgados; semillas intactas.

Rollback: ronda documental, sin cambios de codigo; solo datos QA
desechables. Si un check FALLA se abre BUG-NNN con evidencia y causa raiz.

## Ejecucion real (2026-10-27)

- F1-F8, F10-F13 PASS; F9 PASS con BUG-026 nuevo (chips 0/0 tras
  login/Activate hasta re-seleccion manual); F14 registra BUG-025 vivo.
- I1, I2, I3, I5, I6 PASS (401/403/guardrail/auth/aislamiento);
  I4 FAIL conocido (BUG-024, sin fix planificado); I8/I9 (C11 re-check,
  CRUD de hilos) PASS.
- E1-E4 PASS (QA_R9_Cert: 3/4 items tras 1 rechazo difficulty_mismatch;
  ZIP 175KB; PDFs con Content-Disposition y HEAD 200; propietario ok),
  E1 con nota "indexed_chunks_count: 0" pese a 41 chunks.
- E5 FAIL -> BUG-027 nuevo (examen publicado con preguntas genericas
  "Sahara Desert" en materia sin material ni banco).
- Limpieza: hilos de control r9 purgados; materia QA R9 Recert y examen
  QA_R9_Empty eliminados de BD y /output; semillas y QA_R9_Cert intactos.
- Resultado global: 22 PASS / 2 FAIL (1 conocido, 1 nuevo BUG-027) +
  BUG-026 menor. Documentado en test-plan.md (Ronda 9) y QT-009;
  verificacion final pendiente del propietario.

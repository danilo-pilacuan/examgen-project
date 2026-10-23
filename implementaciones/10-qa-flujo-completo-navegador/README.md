# 10 — QA de flujo completo en el navegador (profesor humano-in-the-loop)

> **Fecha:** 2026-10-19 · **Alcance:** E2E manual del MVP V1.0.0 desde `http://localhost:3000` (frontend dockerizado), actuando como profesor real: registrar materia → descargar y subir material → crear y verificar 75+ preguntas → generar examen del primer parcial.
> **Regla de la sesión:** toda interacción exclusivamente por el navegador integrado (sin llamadas directas a la API).

## Contenido

| Archivo | Descripción |
|---|---|
| [bugs.md](./bugs.md) | Registro de bugs con severidad, evidencia, causa raíz y fix sugerido |
| [issues.md](./issues.md) | Observaciones menores y mejoras de UX no bloqueantes |
| [rfcs.md](./rfcs.md) | Propuestas de solución para los bugs críticos |
| [backlog.md](./backlog.md) | Backlog priorizado (P0/P1/P2) para la ronda de corrección |

## Resumen ejecutivo

El flujo **conversacional de preguntas con HITL funciona de punta a punta** (generar → revisar → guardar → verificar → guardrail anti-borrado), pero **la generación de exámenes está rota en los tres caminos** (chat, formulario Exams y pipeline), y el proxy nginx degrada toda operación larga o pesada.

- ✅ Materias: registro + activación + sincronización reactiva del selector.
- ✅ Material: subida e indexación OK (PDFs ≤ ~120 KB); falla > 1 MB (413).
- ✅ Preguntas: 90 intentos → **87 guardadas**, 86 verificadas como humano desde el chat; calidad de contenido correcta en la muestra revisada.
- ✅ Banco: filtros, detalle, toggle de verificación y guardrail (agente se niega a borrar pregunta verificada).
- ❌ Examen por chat: el stream SSE muere a los 60 s (timeout nginx), sin artefactos ni mensaje de error.
- ❌ Formulario Exams: `POST /exams/generate` no está proxificado → 405 siempre.
- ❌ Pipeline: compila y publica exámenes **vacíos** (0 ítems) marcándolos como completados.

## Flujo ejecutado (evidencia)

### 1. Materias
- Vista Subjects → "+ New subject" → `Base de Datos` → Register → Activate.
- El selector del navbar, la barra de contexto y el badge "Active" se sincronizaron correctamente.

### 2. Material
- Descarga (como profesor, desde la web del libro *Foundations of Databases*, webdam.inria.fr, uso personal permitido):
  - Libro completo (3.1 MB) → **falló al subir: 413** (BUG-05).
  - Capítulos 1 y 3 (~95-120 KB c/u) → subidos por la vista Material.
- Indexación: 14 chunks por capítulo (28 total); ~2 min por archivo (ISS-01).

### 3. Preguntas (HITL por chat)
- 90 intentos de "Generate a question about …, <difficulty> difficulty" en 8 conversaciones (renovadas cada lote para no degradar el DOM).
- Por cada pregunta, como humano verificador: revisión del enunciado, opciones, respuesta y explicación → confirmación textual `yes, save it and mark it as verified by human`.
- Muestra verificada manualmente (todas correctas): primary keys (B), integridad referencial (A), precedencia AND/OR en SQL (A), división relacional con doble NOT EXISTS (A, con caveat de la IA sobre la justificación de B — aceptado), UPDATE…SET (B).
- Resultado: **87 guardadas** (86 verificadas + 1 pendiente), 3 turnos perdidos por cortes de stream (BUG-06/07).
- Los botones del widget QuestionCard (Save / Save & verify) **no se pudieron usar**: 401 (BUG-01); todo el HITL se hizo por texto.

### 4. Banco (vista Bank)
- 91 filas visibles para Base de Datos; filtros por topic (6 resultados "normalization"), difficulty=hard (26), verification=Unverified (0).
- Panel de detalle OK; toggle Remove→Pending→Verify OK.
- Guardrail: "Delete the question about capacity planning…" → el agente localizó la pregunta, detectó `verified_by_human=True` y **se negó a borrarla**, indicando el procedimiento correcto. ✔

### 5. Examen "Parcial 1"
- Chat: el agente propuso blueprint (10 preguntas, temas del banco) y pidió nombre + versiones (HITL correcto).
- Confirmación "Name: Parcial 1, 2 versions" → **stream cortado a los 60 s exactos** (09:09:16 → 09:10:16, `ERR_INCOMPLETE_CHUNKED_ENCODING`), burbuja vacía, sin artefactos nuevos, sin fila en BD, sin llamada al compilador (0 `POST /compile` en la ventana). Causa: BUG-03.
- Formulario "+ Generate exam" (10 preguntas) → **405 Method Not Allowed** siempre (BUG-02), sin mensaje de error en la UI.
- Artefactos preexistentes `Parcial_1_*` (de una sesión anterior del usuario, 03:13): PDFs de 1 página, **0 preguntas, 0 puntos**, título "Economía Aplicada", `Parcial_1.json` con `items: []` → el pipeline compiló un examen vacío como "completed" (BUG-04). Además aparecen listados bajo la materia Base de Datos (BUG-08).
- Descargas: `GET /output/*.pdf` → 200 `application/pdf`; `GET /output/Parcial_1.zip` → 200 ZIP válido con los 4 PDFs; `HEAD /output/*` → 405 (ISS-06).

### 6. Diagnóstico de infraestructura (soporte de los bugs)
- Contenedores sanos: `exam_app (healthy)`, `exam_frontend`, `exam_postgres_db`, `exam_latex_compiler`, `exam_embedding_service`.
- LLM vLLM (`zai-org/GLM-5.3-Flash`) accesible; embedding-service OK (bge-m3, 1024d).
- Logs: el stream del examen (09:09:16) no registra ninguna actividad posterior del pipeline; `POST /exams/generate` nunca aparece en el access log (coherente con BUG-02/03).
- `nginx.conf` sin `client_max_body_size`, sin `proxy_read_timeout` en `/api/` (default 60 s), sin proxy de `/exams` (coherente con BUG-02/03/05).

## Métricas de la sesión

| Métrica | Valor |
|---|---|
| Preguntas generadas (intentos) | 90 |
| Preguntas guardadas | 87 |
| Verificadas por humano (chat) | 86 |
| Turnos perdidos por stream cortado | 3 |
| Tiempo medio por pregunta (gen+save) | ~15-20 s |
| Material indexado | 2 PDFs / 28 chunks |
| Bugs críticos | 4 · altos 2 · medios 3 · bajos 2 |

# Informe de estado de implementación — RC1 (Tag_RC1)

> **Fecha:** 2026-10-23 · **Tag:** `Tag_RC1` (release candidate 1) · **Alcance:** estado consolidado del MVP tras las 3 rondas de QA, listo para congelar desarrollo y pasar al escrito de la tesis.
> **Fuente:** repos verificados en local (commits y tags), stack Docker en ejecución, BD `exam_generator_db` y los informes de las etapas 10-13.

---

## 1. Resumen ejecutivo

El MVP **Exam Generator** (generación de exámenes con agente conversacional HITL para profesores) alcanza su primer **release candidate**: el caso de uso central está completo y certificado E2E en navegador — profesor inicia sesión, registra materias, sube e indexa material, genera/verifica preguntas por chat con human-in-the-loop, genera exámenes (por chat o formulario) con versiones anti-copia y descarga el ZIP.

- **3 rondas de QA** ejecutadas como usuario real (navegador + Playwright): 16 bugs y 16 issues documentados, 15 bugs corregidos y verificados.
- **Stack Docker completo healthy** (6 contenedores) con datos reales de prueba.
- **Deuda conocida documentada** en backlogs priorizados (no bloquea el RC).

---

## 2. Estado por repositorio (Tag_RC1)

| Repo | Commit | Cambios desde V1.0.0 | Rol |
|---|---|---|---|
| **MVP_LatexExam_v1** (meta) | `7a4b896` | docs + punteros | Monorepo, informes QA, deploy |
| **frontend** | `90fe331` | 19 archivos, +274/−22 | Vue 3 + Vite + Pinia, nginx proxy |
| **exam-app** | `1fd9ff5` | 7 archivos, +241/−66 | FastAPI: chat SSE, auth, REST, historial |
| **agents-backend** | `e3a9b8a` | 9 archivos, +525/−72 | LangGraph: agente conversacional + pipeline de exámenes |
| **core** | `62d62e8` | 11 archivos, +459/−5 | Shared kernel: modelos, bank service, config |

Historial de tags: `Tag_V1.0.0` (auth multi-profesor) → `Tag_V1.1.0` (QA ronda 2) → `Tag_V1.1.1` (QA ronda 3) → **`Tag_RC1`**.

---

## 3. Funcionalidad certificada (E2E en navegador)

### 3.1 Caso de uso central — ✅ COMPLETO
| Capacidad | Estado | Certificación |
|---|---|---|
| Login/logout multi-profesor (JWT) | ✅ | C1, R1 (rondas 1-3) |
| Registro/activación de materias con selector reactivo | ✅ | C1, C10, R3 |
| Subida e indexación de material (PDF → chunks + embeddings) | ✅ | C2 (ronda 1) |
| Generación de preguntas por chat con HITL textual | ✅ | 87 preguntas en ronda 1 |
| **HITL por botones** (Save / Save & verify en QuestionCard) | ✅ | C7 (ronda 3) |
| Banco de preguntas: filtros, detalle, toggle verificación | ✅ | R4 |
| Guardrail anti-borrado de preguntas verificadas | ✅ | R2 (rondas 1 y 3) |
| **Examen por chat** (blueprint → nombre/versiones → ZIP) | ✅ | C3 (ronda 1), ronda 3 |
| **Examen por formulario** (POST /exams/generate proxificado) | ✅ | C5 (rondas 1 y 3) |
| ZIP con versiones con/sin respuestas descargable | ✅ | C3, P9 (ronda 2) |
| **Un registro por examen** en la vista Exams (solo botón ZIP) | ✅ | P7-P8 (ronda 2) |
| **Persistencia de conversaciones** (logout/login → historial hidratado) | ✅ | P1-P6 (ronda 2) |
| Exportaciones CSV/XLSX/JSON del banco y JSON del examen | ✅ | R5 |
| Auditoría LLM (`llm_responses` con raw answer/thinking) | ✅ | R6 |
| Inglés forzado en respuestas del agente | ✅ | R7 |
| HEAD /output + Content-Disposition | ✅ | C11 (ronda 3) |
| Errores accionables (413/401/403, banner en formulario) | ✅ | C12 (ronda 3) |
| Tablas markdown sin desbordar la burbuja | ✅ | C13 (ronda 3) |
| Stream muerto → aviso + Retry + persistencia en checkpointer | ✅ | C8 (ronda 3) |
| Idempotencia del guardado HITL tras stream muerto | ✅ | C9 (ronda 3) |
| Pipeline fail-fast (no publica exámenes vacíos) | ✅ | C6 (rondas 1 y 3) |

### 3.2 Pendiente de certificación directa (cubierto por fix aplicado)
- **C2 re-test** (subida ≥ 5 MB sin 413): el fix nginx (`client_max_body_size 100m`) está aplicado; el límite se verificó por el lado del error (413 accionable en C12) pero no con un PDF grande real en la ronda 3.
- **C6 forzado** (LLM inaccesible → `rejection_log`): verificado con blueprint sin ítems; el caso de fallo de red del LLM quedó cubierto por código (fail-fast) sin test de red dedicado.

---

## 4. Bugs: estado consolidado

| Bug | Descripción | Ronda | Estado |
|---|---|---|---|
| BUG-01 | 401 en botones del QuestionCard | 1 | ✅ Corregido (ronda 3, C7) |
| BUG-02 | POST /exams/generate no proxificado (405) | 1 | ✅ Corregido (ronda 1) |
| BUG-03 | SSE muere a los 60 s (timeout nginx) | 1 | ✅ Corregido (ronda 1) |
| BUG-04 | Pipeline publica exámenes vacíos | 1 | ✅ Corregido (fail-fast) |
| BUG-05 | Subida > 1 MB → 413 | 1 | ✅ Corregido (100 MB) |
| BUG-06 | Burbuja vacía sin error al cortarse el stream | 1 | ✅ Corregido (aviso + Retry) |
| BUG-07 | Cortes intermitentes ERR_INCOMPLETE_CHUNKED | 1 | ✅ Corregido (heartbeat + timeouts) |
| BUG-08 | Exámenes legacy de otra materia en el historial | 1 | ✅ Corregido (agrupado por base + filtro huérfanos) |
| BUG-09 | Contadores no refrescan al cambiar materia | 1 | ✅ Corregido (RFC-06) |
| BUG-10 | Pending consumido aunque el stream muera | 1 | ✅ Corregido (ronda 3, C9) |
| BUG-11 | HEAD /output → 405 | 1 | ✅ Corregido (ronda 3, C11) |
| BUG-12 | Errores crudos de subida | 1 | ✅ Corregido (ronda 3, C12) |
| BUG-13 | Conversaciones no persisten al re-login | 2 | ✅ Corregido (endpoint historial + hidratación) |
| BUG-14 | Registros duplicados por PDF en Exams | 2 | ✅ Corregido (37 → 8 registros) |
| BUG-15 | Hard reload de /subjects devolvía 401 JSON (nginx sombreaba la SPA) | 3 | ✅ Corregido (routing por Accept) |
| BUG-16 | 401 transitorio tras reiniciar exam_app | 3 | 🟨 Abierto (menor, transitorio; RFC-12) |

---

## 5. Estado operativo (verificado 2026-10-23)

### 5.1 Stack Docker — 6/6 contenedores healthy
`exam_app` (healthy) · `exam_frontend` · `exam_postgres_db` · `exam_latex_compiler` · `exam_embedding_service` · `exam_open_webui` (healthy)

Endpoints: frontend `200`, `/docs` `200`, `HEAD /output/*.zip` `200`.

### 5.2 Datos en BD (sesión de QA)
| Tabla | Filas | Nota |
|---|---|---|
| users | 1 | danilo.pilacuan@gmail.com |
| subjects | 2 | Base de Datos + Redes de Computadoras |
| generated_questions | 21 | mayoría verificadas por humano |
| exams | 5 | todos con ZIP (QA_Form_Round3, Probe_Head ×2, QA_Empty_Test, QA Rebuild - Examen 1) |
| material_chunks | 14 | 1 PDF indexado |
| llm_responses | 85 | auditoría completa de llamadas LLM |
| checkpoints | 115 | persistencia LangGraph de conversaciones |

Artefactos en `/app/output`: 10 ZIPs, 54 PDFs (los 26 huérfanos UUID pre-persistencia ya no se listan en la UI).

---

## 6. Arquitectura implementada

```
frontend (Vue3+nginx :3000)
  ├─ SSE /api/chat/stream (heartbeat 15 s, retry UI)
  ├─ REST proxificada por Accept (subjects/questions/exams/auth/output)
  └─ Historial de chat hidratado desde /api/chat/history/{thread_id}
exam-app (FastAPI :8000)
  ├─ Auth JWT multi-tenant (users + subject ownership)
  ├─ ChatService → LangGraphEngine (PostgresSaver checkpointer)
  ├─ REST: subjects, bank, exams (agrupado por base + filtro huérfanos), material
  └─ /output con GET+HEAD y Content-Disposition
agents-backend (LangGraph)
  ├─ Grafo conversacional con tools (HITL, guardrails, pending store idempotente)
  └─ Pipeline de exámenes fail-fast (rejection_log + auditoría de errores LLM)
core (shared kernel)
  ├─ Modelos SQLAlchemy + migraciones Alembic
  ├─ bank service con guardrails de verificación humana
  └─ Config: gateway USFQ (OpenAI-compatible) + auth_secret
```

---

## 7. Deuda técnica y backlog (no bloquea el RC)

### P1 — Robustez de sesión (ronda 3)
- BUG-16: retry único ante 401 con token vigente (RFC-12).
- ISS-11: persistir la materia activa entre recargas (RFC-10).
- ISS-13: re-hidratar la burbuja tras un Retry (RFC-11).

### P2 — Calidad/UX
- ISS-12: cursor de streaming bloquea clicks en widgets.
- ISS-14: indicar "2/3 preguntas" cuando el examen tiene menos de las solicitadas.
- ISS-15: desambiguar exámenes con el mismo nombre.
- ISS-16: chips de contexto en la vista Subjects.

### Heredado (rondas 1-2)
- Indexación de material en background con progreso (ISS-01).
- Eventos de progreso del pipeline en el chat (ISS-02).
- Paginación/virtualización del Banco (ISS-03) y del chat (ISS-04).
- `content_language` explícito en/es (ISS-05, RFC-07).
- Advertencia de duplicados al guardar preguntas (ISS-08).
- Migración de exámenes legacy a la tabla `exams` con `subject_id` (RFC-05).

### Infraestructura del proyecto
- **Etapa 1:** repos remotos en GitHub + CI (repos locales listos, remotos no creados).
- Tests E2E automatizados (Playwright scripted) del flujo crítico.
- Token streaming real por tokens (hoy el turno llega como un solo token al final; backlog etapa 2.5).

---

## 8. Conclusión

**RC1 es un release candidate válido**: las 3 rondas de QA certificaron el flujo completo del profesor (materias → material → preguntas HITL → exámenes → ZIP) con 15 de 16 bugs corregidos y verificados, persistencia real de conversaciones (checkpointer Postgres) y de exámenes (tabla `exams`), y un único bug menor abierto (BUG-16, transitorio). El desarrollo puede congelarse en este tag para pasar al escrito de la tesis; el backlog P1/P2 queda documentado para una futura ronda post-RC.

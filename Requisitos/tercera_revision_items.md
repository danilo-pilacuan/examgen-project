# Tercera revision (Felipe) - Items solicitados sobre el estado actual

> **Fuente:** `Requisitos/tercera_revision_Felipe.md` (revision del 2026-11-04)
> **Fecha de analisis:** 2026-11-05 · **Rama:** `RC3/develop`
> **Uso:** marca con `[x]` los items a implementar. Cada item indica el estado real del
> codigo verificado (archivo/linea), el tipo de trabajo y el esfuerzo estimado.

---

## A. Cambios de codigo (producto)

### A1. Fechas de creacion y verificacion en el Question Bank

- **Pedido:** agregar por pregunta la fecha/hora de creacion y la fecha/hora de verificacion.
- **Estado actual (verificado):**
  - `created_at` ya existe en BD (`projects/core/src/core/domain/models.py:58`,
    `server_default=func.now()`), se serializa en `QuestionOut`
    (`projects/exam-app/src/exam_app/schemas/bank.py`) y en el tipo `Question`
    (`projects/frontend/src/types/domain.ts`), pero **no se muestra** como columna en la
    tabla de `BankView.vue` (columnas actuales: expandir, topic, tipo, Bloom, dificultad,
    verificacion, acciones).
  - `verified_at` **no existe en ninguna capa**: requiere migracion Alembic (head actual
    `b8c9d0e1f2a3`) + columna en el modelo + DTOs (`QuestionOut`, `BankExportQuestion`) +
    tipo TS + columna en la tabla. Se setea al marcar verificacion humana
    (`set_human_verification` en el service layer) y al verificar por IA.
- **Trabajo:** migracion + backend + frontend (columna con fecha, formateada).
- **Esfuerzo:** medio. **Decision:** [x] implementar (2026-11-05, IMPL-030/QT-014) / [ ] posponer

### A2. Seleccion por checkboxes de tipos de pregunta en "Generate" de examenes

- **Pedido:** en el flujo de generacion de examenes, elegir con checkboxes que tipos de
  pregunta incluir (ej. solo multiple choice).
- **Estado actual (verificado):**
  - `planner_node` (`projects/agents-backend/src/agents_backend/exam_pipeline/nodes.py:227-270`)
    asigna el tipo **programaticamente** segun nivel Bloom (remember/understand -> MC/TF
    aleatorio; create -> essay; resto -> MC/short/essay aleatorio). No hay forma de restringirlo.
  - `ExamBlueprint` (`projects/core/src/core/domain/schemas/exam.py:128-155`) usa
    `extra="forbid"` (fix BUG-018): hay que agregar un campo nuevo (ej.
    `allowed_question_types: list[QuestionType]` con default = todos) para no romper el contrato.
  - `ExamsView.vue` (form lineas ~104-148, `generate()` lineas ~48-90) no tiene checkboxes;
    habra que agregarlos + claves i18n en `en.ts`/`es.ts` (secciones `exams`).
- **Trabajo:** schema + planner (filtrar la eleccion aleatoria) + frontend + i18n + test de
  rechazo (blueprint con tipo invalido debe fallar 422).
- **Esfuerzo:** medio. **Decision:** [x] implementar - version EXTENDIDA con distribucion
  custom de Bloom/dificultad y retrieval (2026-11-05, IMPL-030/QT-014) / [ ] posponer
- **Refinamiento ronda 2 (2026-11-06, BL-024/IMPL-031):** feedback de Felipe - Bloom como
  checkboxes (no select de presets) y panel avanzado con "cuantas preguntas por tema"
  (selectores numericos); rediseno frontend-only sin cambios de backend (QT-015, BUG-030).

### A3. Comentario en el .env: donde cambiar endpoint y API key

- **Pedido:** dejar un comentario indicando donde se cambia el endpoint y la key del LLM.
- **Estado actual (verificado):** `projects/core/src/core/config.py:14-16` ya documenta
  `LLM_BASE_URL` / `LLM_MODEL` / `OPENAI_API_KEY` en codigo, y `deploy/docker-compose.yml:88-91`
  los declara para el servidor remoto. Falta el comentario visible en el `.env` de trabajo y
  en `docker/docker-compose.yml` (local), que es donde Felipe miraria.
- **Trabajo:** comentarios en `.env.example` (si existe) / `docker/docker-compose.yml` +
  nota en el readme. Sin cambios de comportamiento.
- **Esfuerzo:** bajo. **Decision:** [ ] implementar / [ ] posponer

### A4. Levante automatico con un solo comando (Docker como unico requisito)

- **Pedido:** que Felipe pueda "decirle a Claude que levante todo" sin copiar archivos a mano,
  con Docker instalado como unico requisito; opcionalmente una receta para el agente + un
  script fijo de respaldo.
- **Estado actual (verificado):**
  - Local: `docker/docker-compose.yml` levanta los 6 servicios con
    `cd docker && docker compose up -d --build` (el entrypoint de exam-app aplica migraciones).
  - Remoto: `deploy/deploy.sh|up.sh|down.sh` automatizan el servidor 172.28.230.10 (requiere SSH).
  - Falta: un punto de entrada unico local (ej. `start.bat`/`start.sh` en la raiz o un
    `make up`), prerrequisitos escritos (Docker + `.env` con `OPENAI_API_KEY`), e
    instruccion para el agente (ej. `AGENTS.md`/`CLAUDE.md` en la raiz con la receta de
    levante y el script de respaldo).
- **Trabajo:** script de un comando + seccion "Quick start para revisores" en readme +
  archivo de instruccion del agente.
- **Esfuerzo:** bajo-medio. **Decision:** [ ] implementar / [ ] posponer

---

## B. Entregables de documento / tesis

### B1. Figura del flujo / arquitectura del agente (para enviar por WhatsApp)

- **Pedido:** enviar la figura del flujo/arquitectura del agente (lunes; si feriado, miercoles
  o hasta una semana despues).
- **Estado actual:** `docs/informe_avance.md` (§2.2, §2.3, §3.1, §3.2) y `docs/graphs.md`
  ya contienen los diagramas mermaid del pipeline, RAG y loops. Falta **exportar a imagen**
  (PNG) una figura consolidada lista para enviar por chat.
- **Trabajo:** render de mermaid a PNG + eleccion de la figura final.
- **Esfuerzo:** bajo. **Decision:** [ ] hacer / [ ] posponer

### B2. Documento centrado en la arquitectura del agente (figuras + RAG + metricas)

- **Pedido:** escribir el documento de la tesis centrado en la arquitectura del agente, con
  figuras, detalles tecnicos de RAG y las metricas de los cuatro experimentos.
- **Estado actual:** material base listo: `ARCHITECTURE.md`, `docs/informe_avance.md`,
  `docs/graphs.md`, y los resultados de evaluacion en `test/evaluation/` (4 experimentos
  OFAT, 102 runs, hipotesis H1-H5 resueltas, FINDINGS.md con tablas/plots).
- **Trabajo:** redaccion (capitulo de implementacion + experimentacion). Es el escrito de tesis.
- **Esfuerzo:** alto (escritura, no codigo). **Decision:** [ ] hacer / [ ] posponer

---

## C. Tareas externas / de proceso (no codigo)

| # | Tarea | Responsable | Nota |
|---|---|---|---|
| C1 | Compartir el repo con Felipe y darle acceso | Danilo | Los 7 repos ya estan en GitHub (`examgen-project` + `examgen-*`); falta invitar a Felipe |
| C2 | Mini QA / capacitacion de uso con la asistente de Felipe | Danilo | Requiere A4 (levante facil) para que ella pueda probar |
| C3 | Transferencia del repo a la organizacion USFQ | Felipe/Joshua | Joshua es admin del grupo institucional; espera contacto |
| C4 | Contacto de Emilia | Emilia | Pendiente de ella, sin accion |
| C5 | Definir la defensa en noviembre; escrito hasta el 18 de diciembre | Danilo/Felipe | Calendario, no codigo |

**Decision:** [ ] dejar registradas / [ ] omitir del seguimiento

---

## Resumen de decision

| Item | Que es | Esfuerzo | ¿Implementar? |
|---|---|---|---|
| A1 | Fechas creacion/verificacion en Bank (migracion + UI) | Medio | [x] implementado 2026-11-05 (IMPL-030) |
| A2 | Checkboxes de tipos de pregunta en Generate | Medio | [x] implementado extendido 2026-11-05 (IMPL-030) |
| A3 | Comentario endpoint/key en .env y compose | Bajo | [ ] |
| A4 | Levante de un comando + instruccion para agente | Bajo-medio | [ ] |
| B1 | Figura de arquitectura en PNG | Bajo | [ ] |
| B2 | Documento de tesis (arquitectura + RAG + metricas) | Alto | [ ] |
| C1-C5 | Proceso/externas | - | [ ] |

> **Nota de implementacion (2026-11-05):** A1 y A2 quedaron implementados y
> validados estaticamente (tsc, vue-tsc, vite build, py_compile, AST, caso de
> rechazo, head unico de Alembic `c9d0e1f2a3b4`); trazabilidad en
> `.ops/implementations/IMPL-030-tercera-revision-fechas-tipos.md` y
> `.ops/qa/QT-014-tercera-revision-fechas-tipos.md`. La verificacion en
> navegador (rebuild Docker + `alembic upgrade head`) queda pendiente del
> propietario.

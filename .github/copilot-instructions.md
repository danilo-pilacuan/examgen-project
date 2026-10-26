# Copilot Instructions — Exam Generator (tesis USFQ)

Instrucciones permanentes para el agente en este repositorio. **Léelas al inicio de cada sesión
y aplícalas sin necesidad de que se te vuelvan a pedir.**

## 0. Política permanente: documentación de estado de implementación y handoff

El objetivo de este repo es **reproducibilidad del desarrollo**: cualquier persona (o agente)
debe poder retomar el proyecto leyendo 2-3 archivos. Por eso, como **política del repositorio**:

> **Toda sesión del agente en este repo DEBE generar y actualizar la documentación de estado de
> implementación y handoff como parte del propio trabajo de la sesión, no como un extra
> opcional.** Aplica siempre, sin que el usuario tenga que volver a pedirla.

Flujo obligatorio de cada sesión:

1. **Al iniciar:** leer [implementaciones/HANDOFF.md](../implementaciones/HANDOFF.md) →
   [implementaciones/README.md](../implementaciones/README.md) → el `.md` de la etapa activa.
   No rehacer trabajo ya hecho; continuar desde el estado registrado.
2. **Durante:** si aparece una etapa nueva (o un bloque de trabajo grande), crear el directorio
   `implementaciones/NN-nombre-descriptivo/` con su README y avanzar sus checkboxes. Registrar
   los bugs/issues que aparezcan con la numeración global vigente.
3. **Al cerrar (checklist de cierre):** actualizar, en este orden:
   - el `.md`/directorio de la etapa (estado real, verificado, no "creo que quedó");
   - la fila de la etapa en el mapa de [implementaciones/README.md](../implementaciones/README.md)
     + sección 📊 Progreso global (con fecha real del día);
   - [implementaciones/HANDOFF.md](../implementaciones/HANDOFF.md) (fecha, rama, estado del
     árbol, tabla "Estado por dónde se quedó", gotchas nuevos descubiertos en la sesión);
   - si el hito es visible para el seguimiento de la tesis (release, ronda QA, etapa cerrada):
     añadir una nota de actualización al inicio de [docs/informe_avance.md](../docs/informe_avance.md);
   - commits atómicos y push a `origin` al final de la sesión si hay red.

## 1. Estructura de documentación por etapa

Cada bloque de trabajo vive en `implementaciones/` con este patrón de nombres:

```
implementaciones/
├── HANDOFF.md                    # ← PUNTO DE ENTRADA. Siempre actualizado.
├── README.md                     # mapa de etapas (tabla) + progreso global (📊)
├── NN-nombre-etapa.md            # etapa simple: un solo archivo
└── NN-nombre-etapa/              # etapa compleja o ronda QA: un directorio
    ├── README.md                 # objetivo, alcance, matriz de verificación, artefactos
    ├── bugs.md                   # BUG-XX: síntoma, causa raíz, fix, estado
    ├── issues.md                 # ISS-XX: problemas menores/no bloqueantes, propuestas
    ├── rfcs.md                   # RFC-XX: decisiones de diseño (si aplica)
    └── backlog.md                # prioridades resultantes (P1/P2/P3)
```

Referencias de formato: [13-qa-round3-navegador/](../implementaciones/13-qa-round3-navegador/README.md)
y [16-qa-round4-scroll-playwright/](../implementaciones/16-qa-round4-scroll-playwright/README.md).

### Plantilla de bugs.md (usar exactamente estos campos)

```markdown
## BUG-XX — <título corto>

- **Severidad:** 🔴 Crítica / 🟠 Alta / 🟡 Media / ⚪ Baja
- **Vista(s)/Componente(s):** <dónde>
- **Síntoma:** <qué se observa, con mensaje de error exacto si hay>
- **Causa raíz:** <archivo y línea aproximada; el "por qué", no solo el "dónde">
- **Por qué no se detectó antes:** <una línea; vacío si no aplica>
- **Fix:** <cambio exacto + comando de rebuild si hace falta>
- **Estado:** ✅ Corregido y verificado / 🟨 Corregido sin verificar / ❌ Abierto
```

### Cómo numerar

- BUG/ISS/RFC: continuar la secuencia global (no por archivo). El último número usado está en
  los `bugs.md`/`issues.md` de las rondas previas.
- Etapas: siguiente número libre en `implementaciones/` (16 → 17...).

## 2. Reglas técnicas del repositorio

### Arquitectura

- Meta-repo con submódulos: `projects/frontend`, `projects/exam-app`,
  `projects/agents-backend`, `projects/core`, `projects/embedding-service`,
  `projects/latex-compiler`. Un cambio de código exige commit **dentro del submódulo** y luego
  bump del puntero en el meta-repo.
- Grafo de dependencias acíclico: `frontend → exam-app → agents-backend → libs/core`. Nada de
  imports en sentido contrario.
- Arquitectura limpia por app: `domain → application → interface adapters → infrastructure`.

### Docker (entorno de ejecución)

- Compose principal: `docker/docker-compose.yml` (correr comandos compose desde `docker/`).
- Servicios: `exam_frontend` (:3000, nginx + SPA), `exam_app` (:8000, FastAPI),
  `exam_postgres_db` (:5432), `exam_latex_compiler` (:8080), `exam_embedding_service` (:8081),
  `exam_open_webui`.
- **Cambios en `projects/frontend/nginx.conf` o en el código fuente requieren
  `docker compose build <svc> && docker compose up -d <svc>`** — el conf y el bundle van horneados
  en la imagen, no hay bind-mount.
- Verificación mínima tras rebuild: `curl http://localhost:3000/` → 200.

### Frontend

- Vue 3 + Vite + TS + Pinia. Auth: token en localStorage bajo `mvp_auth`; todas las llamadas
  REST pasan por `src/api/http.ts` (`apiFetch`, que manda `Accept: application/json` y Bearer).
- **Routing API/SPA en nginx es condicional por header `Accept`:** los prefijos `/subjects` y
  `/questions` se proxían al backend solo si el request espera JSON; si no, sirven `index.html`
  (rutas SPA del mismo nombre). Al añadir un prefijo nuevo:
  1. replicar el par de bloques `/<prefijo>` + `/<prefijo>-api`;
  2. en el rewrite del bloque `-api` **conservar el prefijo** (`/<prefijo>$1`), no eliminarlo;
  3. probar **todos los métodos HTTP** del endpoint vía nginx (curl con token), no solo el GET
     de listado — un GET que funciona no garantiza el PUT/POST/DELETE (lección BUG-17b).

### QA en navegador

- QA E2E = navegador real vía Playwright sobre `http://localhost:3000`, no solo TestClient.
- Credenciales de prueba de profesor: preguntar al usuario (no hay credenciales versionadas).
- Checklist mínimo por ronda QA: login → activar materia → Bank (lista + toggle verificación) →
  Exams (lista + formulario con scroll) → Material → Subjects → Chat (pregunta simple al agente).
- En vistas con listas: verificar `scrollHeight > clientHeight` y que el último elemento es
  visible (scrollIntoView) — el scroll global vive en `.main-view` de `AppHeader.vue`
  (`overflow-y: auto`); no volver a poner `overflow: hidden` ahí.
- Restaurar el estado de la BD tras pruebas que lo mutan (toggles, creación de registros).

### Windows / contenedores (gotchas del entorno)

- PowerShell no soporta `&&` → usar `;` o `if ($?) { ... }`.
- Scripts creados en Windows llevan CRLF: `sh` de alpine los rechaza ("not found") →
  `dos2unix` dentro del contenedor o generar el script sin backslash-continuaciones.
- Para debug HTTP dentro de la red de Docker, copiar un script con `docker cp` y ejecutarlo con
  `docker exec <container> sh /tmp/script.sh`.
- curl.exe en PowerShell: escapar JSON con `\"` dentro del cuerpo (`--data '{\"k\":1}'`).

## 3. Definición de "terminado" (por tarea y por sesión)

Una tarea está terminada cuando: el cambio está hecho + verificado (navegador o test) +
documentado en su etapa + commiteado. Una sesión está terminada cuando: HANDOFF.md refleja el
estado exacto en que se quedó + README de etapas actualizado + commits pusheados (o indicados
como pendientes de push en el HANDOFF).

## 4. Documento de handoff: estructura obligatoria

[implementaciones/HANDOFF.md](../implementaciones/HANDOFF.md) es **el documento de soporte para
pasar contexto a la siguiente sesión** (humana o de agente). Debe poder leerse en <2 minutos y
mantener SIEMPRE estas secciones, en este orden:

1. **Encabezado** (blockquote): fecha de última actualización, rama activa y estado del árbol
   (limpio/pendiente, con los hashes de los últimos commits relevantes).
2. **Contexto en 30 segundos:** qué es el sistema, en qué release/etapa está, logros recientes
   en bullets.
3. **Qué leer y en qué orden:** rutas relativas a los documentos de soporte relevantes para los
   escenarios actuales (continuar desarrollo, QA, tesis, etc.).
4. **Estado por dónde se quedó:** tabla `| Tema | Estado |` — es el resumen ejecutivo; cada fila
   debe poder verificarse (comando, test o vista).
5. **Trabajo pendiente:** lista priorizada; indicar si cada ítem requiere código o no.
6. **Gotchas que NO hay que redescubrir:** lecciones del entorno/infra que ya costaron tiempo
   una vez (rebuilds, encoding, semántica de datos, etc.). Añadir los descubiertos en la sesión;
   no borrar los vigentes sin confirmar que ya aplican.

Reglas de mantenimiento: actualizar la fecha SIEMPRE que se toca el archivo; usar la fecha real
del día (no estimar); si algo queda sin terminar, describir el siguiente paso concreto, no solo
el síntoma.

## 5. Al iniciar un proyecto nuevo a partir de este (uso como template)

Copiar esta estructura y adaptarla en orden:

1. `.github/copilot-instructions.md` (este archivo) → renombrar el dominio de negocio y las
   reglas técnicas de la sección 2; mantener tal cual las secciones 0 (política de
   documentación), 1 (estructura por etapa), 3 (definición de terminado) y 4 (estructura del
   handoff) — son de proceso, no de dominio.
2. `implementaciones/HANDOFF.md` + `implementaciones/README.md` iniciales (pueden partir de las
   plantillas de las secciones 1 y 4 de este archivo).
3. Carpetas por etapa según se vayan planificando.
4. Conservar la regla de numeración global de BUG/ISS/RFC y el formato de `bugs.md`: es lo que
   hace auditable el historial entre sesiones y modelos de IA.

# Kit de personalizacion de agentes

Personalizacion generica y multiuso para desarrollo de software: reglas universales de trabajo en
`copilot-instructions.md` + skill `ops-lifecycle` que gobierna el ciclo de vida de documentacion de
operaciones en `.ops` (formato OKF 0.2). No trae estado ni convenciones de ningun proyecto: lo
especifico de cada repo vive en su rulebook (preferiblemente `AGENTS.md`, si existe; si no, README o
documentacion equivalente) y en su propia documentacion.

## Contenido

| Ruta | Que es |
|---|---|
| `copilot-instructions.md` | Nucleo siempre cargado (<= 80 lineas): quirks de entorno, politica de idioma, reglas de trabajo, commits, adopcion. |
| `skills/ops-lifecycle/` | Skill del ciclo de vida: plantillas de documentos, reglas duras de `.ops`, trazabilidad, handoff y bootstrap. Sus `reference/` se cargan solo cuando la tarea toca `.ops`. |
| `tools/validate-kit.mjs` | Validador del kit (Node >= 18, sin dependencias): frontmatter de la skill, ids unicos, enlaces internos, tokens de proyecto y tamano del nucleo. |
| `workflows/validate-kit.yml` | Workflow opcional que ejecuta el validador; se auto-desactiva si el kit no esta instalado. |

## Instalacion en un repo

1. Copia `copilot-instructions.md` a `.github/copilot-instructions.md`.
2. Copia la carpeta `skills/ops-lifecycle/` a `.github/skills/ops-lifecycle/`.
3. Opcional (CI): copia `tools/validate-kit.mjs` a `.github/tools/` y `workflows/validate-kit.yml` a
   `.github/workflows/`.
4. Opcional: crea o revisa el `AGENTS.md` del repo (u otro rulebook) para el stack, comandos,
   puertos y convenciones de codigo especificas. El nucleo lo referencia si existe, pero ningun
   paso de instalacion lo exige: el kit funciona sin el.
5. Ejecuta `node .github/tools/validate-kit.mjs` para verificar la instalacion.

## Actualizacion

Sobrescribe los archivos copiados con la nueva version del kit y vuelve a ejecutar el validador. Si
el repo ya tiene documentacion `.ops` propia, la actualizacion del kit no la toca: los `reference/`
son esqueletos de arranque, no estado.

## Adaptacion por proyecto (puntos configurables)

- `AGENTS.md` del repo (u otro rulebook, si existe): todo lo especifico (stack, comandos, puertos,
  estilo de codigo). Ninguno de los pasos de instalacion lo exige.
- Politica de idioma en `copilot-instructions.md`: el nucleo responde en el idioma del usuario y
  exige ASCII sin diacriticos en artefactos tecnicos y `.ops`; si tu plataforma maneja bien los
  diacriticos, relajalo en tu copia.
- Reglas duras de `.ops` viven solo en `SKILL.md` (fuente unica); para variarlas, edita ahi.

## Validacion

`node tools/validate-kit.mjs` comprueba: frontmatter de `SKILL.md` conforme a la especificacion de
Agent Skills (name en minusculas-con-guiones y <= 64 caracteres, coincidente con el directorio;
description de 1 a 1024 caracteres), ids unicos en todos los `.md`, enlaces relativos internos sin
romper, ausencia de tokens de proyectos ajenos, nucleo de instrucciones dentro del limite de
lineas, ausencia de dependencia dura de `AGENTS.md` (el kit funciona sin el), citas fragiles a
reglas por numero (las plantillas citan reglas por su texto corto) y campos `fecha` con timestamp
estandarizado. Sale con codigo 1 si algo falla.

## Licencia

MIT; ver [LICENSE](LICENSE).

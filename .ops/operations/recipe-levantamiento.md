---
id: qa-recipe-levantamiento
tipo: Guide
type: Guide
title: Recipe de levantamiento del stack
description: Script automatizada y recipe manual para clonar, levantar, verificar y exponer; sin credenciales embebidas.
estado: vigente
dueno: rol:propietario
fecha: 2026-11-12
relaciona: [RUN-016]
status: stable
---

Credenciales: ninguna de las credenciales (admin, QA, LLM, tunnel token)
vive en este documento ni en el repo. El stack lee `OPENAI_API_KEY` del
`.env` (gitignored, se pide al usuario) y `AUTH_SECRET` se genera aleatorio.
Las cuentas de usuario se crean por UI o API en cada levantamiento.

## Via automatizada (entrada para un agente)

`RECIPE.md` en la raiz: objetivo, reglas duras para el agente (seccion 0A),
requisitos, pasos manuales y notas para el agente. Punto de entrada unico
en la raiz: `python levantar.py` (launcher fino que delega en
`scripts/bring-up.py` via runpy conservando los flags `--no-tunnel` y
`--reuse-running`; verifica que la script exista y aborta con mensaje si
no). Una sola script multiplataforma, Python 3.7+ solo stdlib:
`scripts/bring-up.py`
(submodulos -> `.env` (crea desde `.env.example`, pide la key oculta o toma
`OPENAI_API_KEY` del entorno, genera `AUTH_SECRET`) -> deteccion de stack
en marcha -> `docker compose up -d --build` -> espera healthy -> smoke
(SPA 200, /subjects 401 sin token) -> verificacion de submodulos en SHAs
fijados (paso 6) -> quick tunnel e imprime la URL publica). Idempotente.

Reglas duras del recipe (endurecidas tras un experimento con un agente
externo que derivo a exploracion manual, 2026-11-09): (1) primera accion =
ejecutar la script, sin diagnostico manual previo; (2) correr desde el SO
donde `docker version` responde, sin depurar interop WSL; (3) deteccion
obligatoria de stack en marcha por labels de compose: si los exam_* salen
de otro checkout, la script aborta salvo `--reuse-running`; (4) secretos
jamás se copian entre checkouts; (5) exit 0 + lineas OK son el unico
veredicto de exito.

Si el host no tiene Python: bootstrap portable temporal documentado en
`RECIPE.md` (zip embeddable de python.org a `%TEMP%`, sin instalar ni
tocar el PATH); probada 2026-11-09 con el Python del host y con el
interprete portable. Eleccion de tecnologia iterada con el propietario:
PS descartado (no universal), bash descartado (Git Bash extra en Windows),
Python elegido con bootstrap portable temporal autorizado por el
propietario.

## Via manual (equivale paso a paso)

```bash
git submodule update --init --recursive
cp .env.example .env   # editar: OPENAI_API_KEY=<tu-key>; AUTH_SECRET generado
docker compose -f docker/docker-compose.yml up -d --build
docker inspect --format '{{.State.Health.Status}}' exam_app   # -> healthy
docker compose -f docker/docker-compose.yml --profile tunnel up -d tunnel
docker logs exam_tunnel 2>&1 | grep trycloudflare             # URL publica
```

El tunel es un servicio compose (`tunnel`, perfil opt-in) y va por la red
compose al alias `exam-frontend`: el puerto host deja de importar (DGX u
otro `FRONTEND_PORT` no requieren cambios). Para URL estable con credencial
propia: edita el `command` del servicio `tunnel` a
`tunnel --no-autoupdate run --token $TUNNEL_TOKEN` (token solo por
entorno). Bajar todo: `docker compose -f docker/docker-compose.yml
--profile tunnel down; docker compose -f docker/docker-compose.yml down`
(volumenes intactos).

## Gotchas (probados en vivo)

- En PS 5.1 a mano: `docker logs 2>&1` dispara NativeCommandError (usar
  `cmd /c "docker logs ... 2>&1"`) y el 401 llega como excepcion (catch
  generico + StatusCode). Resueltos dentro de `bring-up.py`.
- `docker compose up -d --build` puede devolver exit 1 cosmetico por
  stderr; la script valida por health + HTTP, no por exit code.
- Winget y curl.exe a GitHub releases devolvieron 504 en esta red:
  `docker pull` es la via fiable para las imagenes.
- Stack en marcha desde otro checkout: `docker compose up` de este clon
  falla por conflicto de puertos porque el nombre de proyecto compose
  depende del directorio. La script lo detecta por labels
  (`com.docker.compose.project.config_files`) y aborta salvo
  `--reuse-running` (verificado 2026-11-09 con simulacion de checkout
  ajeno y con el stack real de este checkout).

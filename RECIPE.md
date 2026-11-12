# RECIPE — Levantar y exponer el sistema desde un clone fresco

Objetivo: que cualquier persona o agente (Claude Code, OpenCode, Hermes,
Copilot) clone **solo este repo**, pida al usuario los secretos y deje el
sistema corriendo y expuesto al internet en ~15 minutos. Version corta: una
unica script de Python (`scripts/bring-up.py`, solo biblioteca estandar)
hace todo. Si el sistema ya tiene Python 3.7+:

```bash
python3 scripts/bring-up.py          # Windows: python scripts\bring-up.py
```

Si NO hay Python: usa una copia **portable y temporal** (zip a un directorio
temporal; no se instala nada, no se toca el PATH, nada dentro del repo).
Windows (PowerShell):

```powershell
$py = "$env:TEMP\python-portable\python.exe"
if (-not (Test-Path $py)) {
  Invoke-WebRequest -UseBasicParsing -OutFile "$env:TEMP\py.zip" `
    "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip"
  Expand-Archive "$env:TEMP\py.zip" "$env:TEMP\python-portable" -Force
}
& $py scripts\bring-up.py
```

Linux / macOS: `python3` viene de fabrica en practicamente todas las
distribuciones (`python3 scripts/bring-up.py`); si faltara, instala el
paquete de siempre (`sudo apt install python3`, `xcode-select --install`).

La script hace todo (submódulos, `.env`, build, smoke checks, túnel) y es
idempotente: se puede re-ejecutar. Si prefieres hacerlo paso a paso a mano,
sigue las secciones siguientes. **Este documento no contiene credenciales**; los placeholders
(`<URL-GENERADA>`, `$TUNNEL_TOKEN`, `<tu-key>`) se resuelven en tu entorno.

---

> [!IMPORTANT]
> **Reglas duras para el agente (leer antes de ejecutar cualquier
> comando).** No negociables; si alguna falla, para y comunicala.

1. **Sin exploracion.** No "averigues" el estado del sistema con decenas
   de comandos: `scripts/bring-up.py` ya hace deteccion, build, espera,
   smoke y tunel. Ejecutala primero y lee su salida; investiga SOLO lo
   que la script reporte como error, y con el comando exacto que la
   script sugiera en el mensaje.
2. **Ejecuta desde donde Docker es nativo.** La script requiere `git` y
   `docker` en el PATH. En Windows + WSL: si `docker` no funciona en la
   distro WSL, NO depures el interop ni uses binarios ajenos a traves de
   `/mnt/c`: para y ejecutala desde el shell donde `docker version`
   responda sin errores (PowerShell/CMD en Windows). Valida con
   `docker version` ANTES de empezar; no agregues sondeos propios.
3. **Deteccion de stack en marcha (obligatoria antes de `compose up`).**
   Un stack exam_* corriendo puede pertenecer a OTRO checkout del mismo
   repo. Averigualo con un comando, no con una cadena de comandos:

   ```bash
   docker inspect exam_app --format "{{index .Config.Labels \"com.docker.compose.project.config_files\"}}"
   ```

   - **Mismo checkout** (la ruta impresa es un ancestro de tu repo):
     reutiliza. `bring-up.py` lo detecta solo y salta al smoke.
   - **Otro checkout**: para. NO hagas `compose down` ni rebuild por tu
     cuenta: pregunta al usuario entre (a) reutilizar el stack en marcha
     tal cual (verifica con el smoke de la seccion 4 y termina), o
     (b) reemplazarlo (`docker compose -f docker/docker-compose.yml
     --profile tunnel down` y
     `docker compose -f docker/docker-compose.yml down` **desde el
     checkout dueno del stack**, luego corre la script aqui).
   - **Stack parcial** (algunos contenedores exam_* Up y otros no,
     o todos sin etiqueta `com.docker.compose.*`): no es reutilizable;
     pregunta al usuario antes de `docker rm -f` cualquier contenedor
     exam_* o de reemplazarlo.
4. **Secretos: nunca se copian ni se leen entre checkouts.** `.env`
   vive en cada clone. Si este checkout no tiene `.env`, la script pide
   la `OPENAI_API_KEY` al usuario. NO copies `.env` desde otro
   directorio, NO lo leas y NO lo muevas: lo unico permitido es que el
   usuario pegue su key (o la exporte en `OPENAI_API_KEY`).
5. **Exito = evidencia, no sensacion.** El exit 0 de la script + sus
   lineas `OK` son el veredicto. Si no aparecen, el sistema NO esta
   verificado: reporta el error exacto y para; no lo sustituyas por
   checks HTTP ad-hoc ni por `docker ps` interpretado a mano.

## 0B. Requisitos (verificar antes de empezar)

| Requisito | Cómo verificar |
|---|---|
| Docker Desktop corriendo | `docker version` (sin errores) |
| Git + submodules | `git --version` |
| Python 3.7+ (solo para la script; si falta, bootstrap portable del encabezado) | `python3 --version` (Windows: `python --version`) |
| Conectividad a github.com (y a python.org solo para el bootstrap portable) | `git ls-remote https://github.com/danilo-pilacuan/examgen-project.git HEAD` |
| Stack exam_\* en marcha (si existe, aplicar la regla 3) | `docker ps --filter name=exam_` |

## 1. Clonar el repo principal + submódulos

```bash
git clone https://github.com/danilo-pilacuan/examgen-project.git
cd examgen-project
python3 scripts/bring-up.py   # Windows: python scripts\bring-up.py
```

La script hace los pasos 1-5. A mano, cada paso:

```bash
git submodule update --init --recursive   # clona los 6 submódulos en el SHA fijado
```

> El SHA de cada submódulo queda fijado por el repo principal; nadie toca
> per-submodule auth. `git submodule status` debe listar 6 sin prefijo
> `+` ni `U`; si sale algo distinto, la script lo reporta y se corrige con
> `git submodule update --init --recursive` (o `git checkout` del SHA
> fijado si un submódulo quedó en otra rama).

## 2. Secretos: crear `.env` (gitignored)

Solo se pide al usuario **un valor**; el resto se genera o viene de
`.env.example`:

1. `OPENAI_API_KEY` — API key del gateway LLM institucional (USFQ u otro
   proveedor compatible con OpenAI). **El único secreto obligatorio.**
2. `AUTH_SECRET` — las scripts lo generan solas (no lo pidas).

La script edita `.env` por ti: pide la key con input oculto (o la toma de la
variable de entorno `OPENAI_API_KEY` si existe) y genera `AUTH_SECRET`.
Solo si lo haces a mano:

```bash
cp .env.example .env
# Edita .env y pon tu key:
#   OPENAI_API_KEY=<tu-key>
# AUTH_SECRET (JWT multi-profesor), generar una y pegarla:
python3 -c "import secrets; print(secrets.token_hex(48))"
```

> `.env` está en `.gitignore` — jamás se commitea. Si el usuario no tiene
> aún `OPENAI_API_KEY`, explícale que es la credencial del gateway LLM
> (get it from the gateway admin) y detente ahí: sin esa key el sistema
> levanta pero no genera preguntas ni examenes.

## 3. Levantar el stack (build + health)

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

Antes de esto, la script aplica la regla 3 (deteccion de stack): si los
contenedores `exam_*` que ya corren salen de OTRO checkout, para y
pregunta; no reemplaza nada por su cuenta.

La primera vez tarda 5-10 min (latex-compiler descarga TeX Live). Espera a
que `exam_app` esté `healthy`:

```bash
docker inspect --format '{{.State.Health.Status}}' exam_app   # → healthy
docker ps --filter name=exam_                                 # → 5 contenedores Up
```

El entrypoint de exam-app aplica las migraciones Alembic al arrancar; no
corras Alembic manualmente. En algunos shells `docker compose up -d
--build` puede devolver un exit 1 cosmético — valida por health + smoke,
no por exit code (la script ya lo hace asi).

## 4. Verificar (smoke checks)

```bash
# SPA
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:3000/          # → 200
# auth intacta (este caso DEBE fallar con 401)
curl -s -o /dev/null -w '%{http_code}\n' -H 'Accept: application/json' \
  http://localhost:3000/subjects                                          # → 401
```

Los puertos del smoke salen del mapeo real del compose (`FRONTEND_PORT:80`
y `APP_PORT:8000`), no de valores fijos; la script los lee de
`docker port` del contenedor levantado.

La script ejecuta estas verificaciones automaticamente tras el build
(Windows 10+ ya incluye `curl`; si falta, usa `python -c "import
urllib.request; print(urllib.request.urlopen('http://localhost:3000/').status)"`).

Opcional, cuenta de prueba (pregúntale al propietario; nunca en la doc):

```bash
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email": "<nuevo>", "password": "<nueva>"}'
curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "...", "password": "..."}'                                # -> 200
curl http://localhost:3000/subjects -H 'Accept: application/json' \
  -H "Authorization: Bearer $TOKEN"                                       # -> 200
```

## 5. Exponer al internet (cloudflared quick tunnel)

El tunel es hoy un **servicio compose** (`tunnel`, perfil opt-in
`tunnel`), dentro de la misma red del stack; alcanza el frontend por su
alias de red `exam-frontend` (no usa `host.docker.internal` ni rutas
prohibidas). Un solo comando, **sin credenciales**; la URL publica es
aleatoria y cambia en cada levantamiento (RUN-016 Modo A):

```bash
docker compose -f docker/docker-compose.yml --profile tunnel up -d tunnel
docker logs exam_tunnel 2>&1 | grep trycloudflare
#    → https://<4-palabras>.trycloudflare.com   ← comparte esta URL
```

- La script hace este paso completa: levanta el servicio, espera y extrae
  la URL de los logs del tunel. El puerto host deja de importar: el tunel
  va a `http://exam-frontend:80` por la red compose.
- **URL estable (opcional):** tunnel token propio de Cloudflare Zero
  Trust. En `docker/docker-compose.yml` cambia el `command` del servicio
  `tunnel` por `tunnel --no-autoupdate run --token $TUNNEL_TOKEN`
  (placeholder; nunca en git).
- Apagar: `docker compose -f docker/docker-compose.yml --profile tunnel
  down` (mata el tunel y la URL al instante).
- *Modo heredado* (`docker run --name exam_tunnel ...`): sigue siendo
  validamente accesible pero ya no es el camino soportado.

## 6. Teardown

```bash
docker compose -f docker/docker-compose.yml --profile tunnel down  # tunel + URL
docker compose -f docker/docker-compose.yml down                   # contenedores + red
# los volumenes (BD, open_webui_data) sobreviven al down
```

---

## Notas para el agente que ejecuta la recipe

- **Ejecuta la script antes que nada** (regla 1 de la seccion 0A): sin
  salida de `bring-up.py` no hay diagnostico; con su salida, cada
  siguiente comando debe salir del mensaje de error impreso.
- **Reutilizacion del stack en marcha:** `bring-up.py` acepta
  `--reuse-running` para adoptar un stack exam_* que salga de otro
  checkout SIN tocarlo (solo smoke + tunel) y aborta sin el flag. La
  decision siempre es del usuario, nunca del agente.
- **Submodulos:** la script verifica (paso 6) que los 6 existan y esten
  en los SHAs fijados; cualquier desviacion aborta con el comando exacto
  de arreglo. No corras `git submodule update --remote`: cambiaria los
  SHAs y romperia la reproducibilidad.
- **No inventes secretos.** Si falta `OPENAI_API_KEY`, pídeselo al usuario
  y detente hasta tenerlo; jamás lo escribas en un archivo versionado ni
  en un log. No copies `.env` entre clones (regla 4 de la seccion 0A).
- **No pidas credenciales de Cloudflare** para el Modo A (quick tunnel):
  no existen. Para URL estable, pide el token al usuario (`$TUNNEL_TOKEN`)
  y úsalo solo por entorno, nunca en el repo.
- **Valida antes de declarar éxito:** exit 0 de `bring-up.py` + sus
  lineas `OK` (los 5 contenedores `exam_*` Up, `exam_app` healthy, SPA
  200, `/subjects` 401 sin token, URL en logs del túnel). Si la script
  no termina en exit 0, el sistema NO esta verificado; no lo sustituyas
  con checks hechos a mano.
- **Una sola script para cualquier SO:** `python scripts/bring-up.py`
  (desde la raiz del repo). Si no hay Python, sigue el bootstrap portable
  del encabezado: zip embeddable de python.org a un directorio temporal,
  ejecutalo desde ahi; no instales Python, no toques el PATH y no
  descargues nada dentro del repo. Si en Windows `python` abre la
  Microsoft Store (stub), usa directamente el bootstrap portable.
- **No toques contenedores ajenos** (projecthub-*, graphify-*): solo los
  `exam_*` de este repo.
- Gotchas de Windows (ya resueltos dentro de `bring-up.py`; aplican a
  mano): PowerShell 5.1 sin `&&` (usa `;`); el 401 de `Invoke-WebRequest`
  llega como excepción; `docker logs` sin stderr se queda mudo — usa
  `cmd /c "docker logs exam_tunnel 2>&1"`; consola cp1252; `docker compose
  up` con exit 1 cosmético — valida con health + HTTP.
- Gotchas Linux: el tunel ya no depende de `host.docker.internal` (va por
  la red compose al alias `exam-frontend`); el interprete puede llamarse
  `python3` y no `python` — usa el que exista; el interprete del zip
  embeddable en Windows se llama `python.exe` (la ruta del bootstrap del
  encabezado ya lo usa).

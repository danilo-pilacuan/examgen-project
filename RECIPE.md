# RECIPE — Levantar y exponer el sistema desde un clone fresco

Objetivo: que cualquier persona o agente (Claude Code, OpenCode, Hermes,
Copilot) clone **solo este repo**, pida al usuario los secretos y deje el
sistema corriendo y expuesto al internet en ~15 minutos. Version corta: una
unica script de Python (`scripts/bring-up.py`, solo biblioteca estandar)
hace todo. Si el sistema ya tiene Python 3.7+:

```bash
python scripts/bring-up.py          # Windows: python scripts\bring-up.py
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

## 0. Requisitos (verificar antes de empezar)

| Requisito | Cómo verificar |
|---|---|
| Docker Desktop corriendo | `docker version` (sin errores) |
| Git + submodules | `git --version` |
| Python 3.7+ (solo para la script; si falta, usa el bootstrap portable del encabezado) | `python --version` |
| Puertos 3000/8000/5432/8080/18081/3001 libres | `docker ps` (nada en esos puertos) |
| Conectividad a github.com (y a python.org solo para el bootstrap portable) | `git ls-remote https://github.com/danilo-pilacuan/examgen-project.git HEAD` |

## 1. Clonar el repo principal + submódulos

```bash
git clone https://github.com/danilo-pilacuan/examgen-project.git
cd examgen-project
git submodule update --init --recursive   # clona los 6 submódulos en el SHA fijado
```

> El SHA de cada submódulo queda fijado por el repo principal; nadie toca
> per-submodule auth. `git submodule status` debe listar 6 sin prefijo `+`.

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
python -c "import secrets; print(secrets.token_hex(48))"
```

> `.env` está en `.gitignore` — jamás se commitea. Si el usuario no tiene
> aún `OPENAI_API_KEY`, explícale que es la credencial del gateway LLM
> (get it from the gateway admin) y detente ahí: sin esa key el sistema
> levanta pero no genera preguntas ni examenes.

## 3. Levantar el stack (build + health)

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

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

Un solo comando, **sin credenciales**; la URL pública es aleatoria y cambia
en cada levantamiento (RUN-016 Modo A):

```bash
docker pull cloudflare/cloudflared:latest
docker run --rm -d --name exam_tunnel cloudflare/cloudflared:latest \
  tunnel --url http://host.docker.internal:3000 --no-autoupdate
docker logs exam_tunnel 2>&1 | grep trycloudflare
#    → https://<4-palabras>.trycloudflare.com   ← comparte esta URL
```

- Linux: añade `--add-host=host.docker.internal:host-gateway`.
- La script hace este paso completa: levanta el contenedor, espera y
  extrae la URL de los logs del tunel.
- **URL estable (opcional):** tunnel token propio de Cloudflare Zero Trust
  (placeholder `$TUNNEL_TOKEN`): `tunnel --no-autoupdate run --token $TUNNEL_TOKEN`.
- Apagar: `docker rm -f exam_tunnel` (la URL muere al instante).

## 6. Teardown

```bash
docker rm -f exam_tunnel                                 # mata la URL pública
docker compose -f docker/docker-compose.yml down         # contenedores + red
# los volumenes (BD, open_webui_data) sobreviven al down
```

---

## Notas para el agente que ejecuta la recipe

- **No inventes secretos.** Si falta `OPENAI_API_KEY`, pídeselo al usuario
  y detente hasta tenerlo; jamás lo escribas en un archivo versionado ni
  en un log.
- **No pidas credenciales de Cloudflare** para el Modo A (quick tunnel):
  no existen. Para URL estable, pide el token al usuario (`$TUNNEL_TOKEN`)
  y úsalo solo por entorno, nunca en el repo.
- **Valida antes de declarar éxito:** los 5 contenedores `exam_*` Up,
  `exam_app` healthy, SPA 200, `/subjects` 401 sin token, URL en logs del
  túnel.
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
- Gotchas Linux: el tunel necesita
  `--add-host=host.docker.internal:host-gateway` (la script lo añade sola
  en Linux); el interprete puede llamarse `python3` y no `python` — usa el
  que exista.

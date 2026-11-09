# Exponer el sistema al internet (cloudflared)

Guía para dar acceso externo al stack (demo de tesis, revisión de Felipe)
sin abrir puertos del router ni tocar el firewall. Elegimos **cloudflared
quick tunnel** sobre Tailscale Funnel por ser la opción más sencilla y
**agnóstica a credenciales**: en el modo demo no hace falta cuenta ni token
de ningún proveedor; la decision formal vive en
[DEC-005](../.ops/decisions/DEC-005-exposicion-publica-tunel.md) y el
runbook verificado en [RUN-016](../.ops/operations/RUN-016-exposicion-publica-cloudflared.md).

## Cómo funciona

`cloudflared` abre una **conexión saliente** hacia el edge de Cloudflare y
recibe tráfico de vuelta: no se publica ningún puerto, no se modifica el
firewall ni el router. El modo *quick tunnel* imprime una URL pública
aleatoria (`https://<4-palabras>.trycloudflare.com`) que **cambia en cada
levantamiento** y desaparece al detener el contenedor. El túnel apunta al
**frontend (nginx, puerto host 3000)**, que ya hace mismo-origen y proxifica
`/api`, `/ws`, `/auth`, `/subjects`, `/output`, etc. — nunca al backend directo.

## Modo A — Demo (sin credenciales, el más simple)

Requisitos: Docker corriendo y el stack arriba (`cd docker && docker compose up -d --build`).

```powershell
# 1. Imagen (solo la primera vez; winget/curl directo falló con 504 en esta red)
docker pull cloudflare/cloudflared:latest

# 2. Levantar el túnel (Windows/macOS; en Linux añade --add-host=host.docker.internal:host-gateway)
docker run --rm -d --name exam_tunnel cloudflare/cloudflared:latest `
  tunnel --url http://host.docker.internal:3000 --no-autoupdate

# 3. Leer la URL pública generada de los logs
docker logs exam_tunnel 2>&1 | Select-String "trycloudflare"
#    → https://grab-testimonials-pty-numbers.trycloudflare.com (ejemplo; la tuya será otra)
```

Comparte esa URL: el visitante ve el login del frontend y necesita una
cuenta (la auth JWT se mantiene a través del túnel). Si el puerto del
frontend es otro (DGX: 39005), sustitúyelo en `--url`.

## Modo B — URL estable (requiere TU credencial propia)

Cuando necesites una URL fija (Dominio propio + subdominio), crea un
*tunnel token* en el dashboard Zero Trust de Cloudflare (Networks → Tunnels
→ Create tunnel → copia el token) y ejecuta:

```powershell
docker run --rm -d --name exam_tunnel cloudflare/cloudflared:latest `
  tunnel --no-autoupdate run --token $env:TUNNEL_TOKEN
```

El token vive solo en tu entorno (`$env:TUNNEL_TOKEN` o un `.env` fuera de
git); **jamás se commitea ni se documenta**. Alternativa: Tailscale Funnel
(`tailscale funnel 3000`) da URL `*.ts.net` estable, pero exige cuenta
Tailscale, HTTPS habilitado y ACL de funnel en la consola.

## Verificación (todas pasaron el 2026-11-09 a través de la URL pública)

| Prueba | Esperado |
|---|---|
| `GET <URL>/` | 200 — HTML de la SPA |
| `GET <URL>/subjects` con `Accept: application/json` **sin token** | **401** — la auth no se relaja al exponer |
| `POST <URL>/auth/login` con una cuenta de prueba | 200 — token JWT |
| WebSocket `wss://<host>/ws` | OPEN (101) — chat del agente funciona |

## Seguridad — lee antes de exponer

- **No expongas** puertos crudos: Postgres (5432), exam-app (8000),
  latex-compiler (8080) o embedding-service (18081) quedan solo en la red
  interna de Docker.
- **Nunca expongas open-webui** (puerto 3001, perfil legacy): corre con
  `WEBUI_AUTH=false`, sin login.
- [BUG-024](../.ops/qa/BUG-024-sin-cabeceras-seguridad-nginx.md) (cabeceras
  de seguridad nginx) sigue abierto: evita compartir la URL más tiempo del
  necesario.
- Apaga el túnel al terminar la demo:

```powershell
docker rm -f exam_tunnel   # la URL queda muerta inmediatamente
```

## Levantamiento completo (recipe)

Para levantar desde cero (clone fresco) con script automatizada o pasos
manuales, ver [RECIPE.md](../RECIPE.md) y la única script multiplataforma
[scripts/bring-up.py](../scripts/bring-up.py) (Python 3.7+, solo stdlib; si
el host no tiene Python, el bootstrap de un intérprete portable temporal
está documentado en el RECIPE); la versión .ops está en
[.ops/operations/recipe-levantamiento.md](../.ops/operations/recipe-levantamiento.md).

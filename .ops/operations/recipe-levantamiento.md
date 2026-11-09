---
id: qa-recipe-levantamiento
tipo: Guide
type: Guide
title: Recipe de levantamiento del stack
description: Secuencia de comandos (Windows + Docker) para levar el stack y exponerlo; sin credenciales embebidas.
estado: vigente
dueno: rol:propietario
fecha: 2026-11-09
relaciona: [RUN-016]
status: stable
---

Credenciales: ninguna de las credenciales (admin, QA, LLM, tunnel token)
vive en este documento. El stack lee `OPENAI_API_KEY` de `../.env` (fuera de
git). Las cuentas de usuario se crean por UI o API en cada levantamiento.

## 1. Stack

```powershell
cd docker
docker compose up -d --build   # postgres, latex-compiler, embedding, exam-app, frontend
docker ps --filter name=exam_  # 5 contenedores Up (open-webui es perfil legacy)
```

Verificacion: `curl http://localhost:3000/` -> 200 y
`http://localhost:8000/health` -> healthy. El entrypoint de exam-app aplica
Alembic al arrancar.

## 2. Exposicion al internet (RUN-016)

```powershell
docker pull cloudflare/cloudflared:latest
docker run --rm -d --name exam_tunnel cloudflare/cloudflared:latest `
  tunnel --url http://host.docker.internal:3000 --no-autoupdate
docker logs exam_tunnel 2>&1 | Select-String "trycloudflare"
```

Con `FRONTEND_PORT` distinto (DGX: 39005) sustituir en `--url`. Para URL
estable con credencial propia: `tunnel run --token $TUNNEL_TOKEN`.

## 3. Alta de usuario de prueba

```powershell
$u = "https://<URL-del-tunnel>"
Invoke-WebRequest -Uri "$u/auth/register" -Method POST -ContentType `
  "application/json" -Body '{"email":"<nuevo>","password":"<nueva>"}'
```

## 4. Bajar todo

```powershell
docker rm -f exam_tunnel              # mata el quick tunnel (URL invalida)
docker compose down                   # contenedores + red; volumenes intactos
```

Comprobado en Windows: si `docker compose up -d --build frontend` devuelve
exit 1 cosmetico por stderr, verificar con `docker ps` y curl, no con el exit
code (gotcha de handoff).

---
id: IMPL-011
tipo: Implementation
type: Implementation
title: Auth multitenant + navbar reactivo (Tag_V1.0.0)
description: Login multi-profesor JWT, ownership de materias y selector reactivo sincronizado.
estado: ejecutado
dueno: rol:propietario
fecha: 2026-10-19
relaciona: [BL-001, IMPL-007]
status: stable
---

## Alcance

Incluye: auth JWT multi-profesor (users + subject ownership), navbar con login/logout,
selector de materia reactivo con sincronizacion bidireccional (navbar <-> vista Subjects
<-> chat) y context bar con chips de conteo. Tag `Tag_V1.0.0` en los submodulos. No
incluye: persistencia de la materia activa entre recargas (BL-008/ISS-17).

## Diseno

El token se guarda en localStorage (`mvp_auth`) y se inyecta en apiFetch; los endpoints
de chat lo exigen en el body para SSE (BUG-001). Verificado E2E: C1/R1/R3 certificados
en rondas 1-3; BUG-013 anade persistencia de conversaciones por usuario.
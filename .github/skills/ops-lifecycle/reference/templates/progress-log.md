---
id: TEMPLATE-LOG
tipo: Template
type: Template
title: Plantilla de bitacora (progress)
description: Modelo de entrada para project/progress.md (sustituye a PROGRESS.md).
estado: vigente
dueno: rol:propietario
fecha: 2026-10-25
relaciona: [templates-base]
---

`project/progress.md` es un log OKF (seccion 9): sin frontmatter, entradas agrupadas por fecha ISO `YYYY-MM-DD`, mas reciente primero, una entrada por tarea (regla 7 de la seccion 0).

Modelo de entrada:

## <YYYY-MM-DD>

* **Hecho**: <que se hizo; id de BL/IMPL>.
* **Falta**: <que queda pendiente de esa tarea>.
* **Decision**: <id DEC tomada o "ninguna">.
* **Medicion**: <resultado medido con salida real, si la fase lo exige (p. ej. tiempo de busqueda, Fase 2)>.

Nota: mientras no se apruebe el cambio (DEC abierta sobre PROGRESS.md), si PROGRESS.md existe en la raiz, copiar aqui y anotar la coexistencia.

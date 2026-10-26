# 🔄 Handoff — Próxima sesión (leer primero)

> **Última actualización:** 2026-10-26 · **Rama activa:** `RC2/develop` (meta-repo + 6 submódulos)
> **Estado del árbol:** limpio (todo commiteado y pusheado, último commit `78a874f` + docs etapa 15)

## Contexto en 30 segundos

Sistema: **Exam Generator** — multi-agente LangGraph que genera exámenes con HITL para profesores
(tesis USFQ, defensa 14–21 dic 2026).

- **RC1 (Tag_RC1, etapa 14):** MVP funcional certificado E2E (3 rondas QA, 15/16 bugs corregidos).
- **RC2 (etapa 15):** framework de evaluación en `test/evaluation/` + **102 runs reales** con
  GLM-5.3-Flash (gateway USFQ). **Hipótesis H1-H5 todas resueltas**; hiperparámetros de
  producción validados empíricamente (gen T=0.7, top_k=3, eval T=0.2).

## Qué leer y en qué orden

1. **Este archivo** (contexto + estado).
2. [`implementaciones/README.md`](README.md) → mapa de etapas + progreso global (sección 📊).
3. [`implementaciones/15-framework-evaluacion-agente.md`](./15-framework-evaluacion-agente.md) →
   **el documento de handoff principal de RC2**: diseño, resultados, decisiones técnicas,
   gotchas del entorno y cómo ejecutar todo.
4. Si toca escribir la tesis → `test/evaluation/experiments/E0*/FINDINGS.md` (4 archivos con
   tablas, plots incrustados y discusión lista para capítulo de experimentación).
5. Si toca el framework → `test/evaluation/README.md` (doc viva: §6 ejecución, §8 metodología,
   §9 limitaciones, §10 checklist).

## Estado por dónde se quedó

| Tema | Estado |
|---|---|
| Framework de evaluación (código) | ✅ congelado y reproducible (dry-run + real) |
| Campañas reales E01-E04 | ✅ 102 runs, agregados, FINDINGS, plots |
| Judge LLM faithfulness | ✅ implementado + ejecutado sobre E03 (0.352 ± 0.052) |
| Hipótesis H1-H5 | ✅ todas resueltas |
| Publicación | ✅ `origin/RC2/develop` (commits 007a9d7 → 78a874f) |
| Informes de implementación | ✅ etapa 15 creada; README de etapas e informe_avance actualizados |

## Trabajo pendiente (ninguno depende de código)

1. **Escrito de la tesis** (prioridad alta): capítulo de experimentación tiene toda la base
   (FINDINGS + metodología + limitaciones documentadas).
2. **Cross-provider comparativa** (opcional): solo requiere un modelo nuevo en el gateway →
   1 entrada en `test/evaluation/models.yaml` + 1 brazo en `experiments.yaml`. Sin código.

## Gotchas que NO hay que redescubrir

- Dry-run escribe stub embeddings en la BD real → si se mezclan modos, correr
  `test/evaluation/_reindex_real.py` (detalle en etapa 15 §5.1).
- Gateway GLM consume reasoning tokens en chat aunque `reasoning_effort=none` →
  `max_tokens` ≥ 2000 para respuestas JSON (el judge ya lo configura).
- Portátil en movimiento corta WSL2 → contenedores mueren a mitad de run; usar keep-awake
  (`SetThreadExecutionState`) y verificar `docker ps` antes de reintentar.
- CLIs del framework requieren `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- runs.jsonl / logs son gitignored; aggregate.json + report.md + FINDINGS.md + PNGs están versionados.

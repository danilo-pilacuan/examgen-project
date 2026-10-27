---
id: qa-readme
tipo: Guide
type: Guide
title: QA index
description: Estrategia, plan de pruebas, matriz de trazabilidad y registro BUG.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-27
relaciona: [templates-defect]
status: stable
---

## Index

- `strategy.md` - what "verified" means (browser-only rule) + validation rules.
- `test-plan.md` - C1-C40 + R1-R7 certification matrix per round.
- `traceability.md` - REQ -> BL -> IMPL -> QT coverage with evidence.
- `BUG-001..BUG-025.md` - defect register, flat in this folder (26 files).

Round 7 (2026-10-27, IMPL-024, recertificacion funcional + integracion):
bug reportado "no veo conversaciones pasadas" = BUG-023 (listado solo en
localStorage; fix en BL-017); BUG-022 critico (hilos de chat sin
propiedad: lectura/escritura entre usuarios, DEC-004 abierta); BUG-024
(sin cabeceras de seguridad nginx) y BUG-025 (mensaje 401 enganoso en
login) nuevos. C25-C40: 11 PASS / 3 FAIL / 2 PASS con nota.

Bugs follow `templates/defect.md`; the agent writes evidence (real output, never
claimed), the owner sets `verified`. QT follow `templates/test-case.md`; only the
owner closes them.
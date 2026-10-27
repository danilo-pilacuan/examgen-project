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
- `test-plan.md` - C1-C24 + R1-R7 certification matrix per round.
- `traceability.md` - REQ -> BL -> IMPL -> QT coverage with evidence.
- `BUG-001..BUG-021.md` - defect register, flat in this folder (22 files).

Round 6 (2026-10-27, IMPL-023, RC3 certification): BUG-016 verified fixed
(3 restarts, 0 401), BUG-018 verified fixed (real HTTP sondas via nginx),
RFC-10/11 PASS in browser, C2 PASS with 5.4 MB PDF (211 chunks, RAG OK).
New findings: BUG-019 (duplicate HUMAN in checkpointer on Retry),
BUG-020 (unbounded indexing blocks embedding service ~29 h, no progress
nor cancel), BUG-021 (persist=false still persists the exam row/PDFs/ZIP).
Open decisions for the owner: DEC-001, DEC-002, DEC-003.

Bugs follow `templates/defect.md`; the agent writes evidence (real output, never
claimed), the owner sets `verified`. QT follow `templates/test-case.md`; only the
owner closes them.
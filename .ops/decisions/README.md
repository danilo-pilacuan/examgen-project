---
id: decisions-readme
tipo: Guide
type: Guide
title: Decisions index
description: Registro DEC de decisiones abiertas y cerradas.
estado: vigente
dueno: rol:propietario
fecha: 2026-10-26
relaciona: [templates-decision]
status: stable
---

## Index

- `DEC-001-persist-false-exams-generate.md` (abierta, 2026-10-27): que hace
  `POST /exams/generate` con `persist=false`; detectada en QA ronda 6 (BUG-021).
- `DEC-002-dedupe-human-retry.md` (abierta, 2026-10-27): estrategia de
  deduplicacion del HUMAN tras Retry; detectada en QA ronda 6 (BUG-019).
- `DEC-003-limites-indexacion-material.md` (abierta, 2026-10-27): limites y
  estrategia de indexacion de material grande; detectada en QA ronda 6
  (BUG-020, C2).

Open questions are drafted here as `DEC-NNN-slug.md` (template `templates/decision.md`,
6-line options table max) and the owner answers them. The agent never closes a DEC
itself, never edits AGENTS.md or scope on its own. Current open questions live in the
backlog as BL items (e.g. BL-019 cross-provider comparison) until promoted to DEC.
---
name: ops-lifecycle
description: Work with the .ops/ lifecycle structure — create or update REQ, BL, IMPL, QT, BUG, DEC, RSK, VULN, RUN, MIG or REL documents, apply the OKF 0.2 frontmatter contract, maintain traceability, or bootstrap the .ops tree in a new project. Use when the task involves .ops documents, their templates, numbering, or governance rules.
---

# .ops lifecycle

`.ops/` is the repository's lifecycle reference (governance, planning, traceability). It is
NOT shipped code. `.ops` organizes and links; root `PROGRESS.md` is the single source of
truth for progress. Platform knowledge lives in `core/` and `orgs/`, never in `.ops/`.

This skill carries **reference copies** of the live `.ops` files under `reference/`:

- `reference/templates/` — copies of `.ops/templates/*.md` (OKF 0.2 contract + one
  template per doc type).
- `reference/tree/` — copies of `.ops/README.md` and each tree's `README.md` (indexes).

## Sync rule (mandatory)

The live files in `.ops/` are authoritative; the copies here are snapshots. When you
create or change any `.ops/templates/*.md` or any tree README, apply the identical change
to the corresponding copy under `reference/` **in the same change set**. On any
discrepancy, read the live file and prefer it; fix the copy while you are there. Never
edit the copies as if they were the live documents.

## Routing: what am I documenting?

| Need | Tree | Doc type + id | Template |
|---|---|---|---|
| Product need or feature | `product/` | REQ-NNN | `requirement.md` |
| Planned, traceable work | `project/` | BL-NNN | `backlog-item.md` |
| Phase spec and verification | `implementations/` | `fase-N` | `implementation.md` |
| Decision with alternatives | `decisions/` | DEC-NNN | `decision.md` |
| Test case or evidence | `qa/` | QT-NNN | `test-case.md` |
| Defect from QA | `qa/` | BUG-NNN | `defect.md` |
| Risk with trigger | `governance/` | RSK-NNN | `risk.md` |
| Audit, control or compliance | `governance/` | AUD/CTRL in `audits.md` table | — |
| Security finding | `security/` | VULN-NNN | `vuln.md` |
| Recurring operation | `operations/` | RUN-NNN | `run.md` |
| Deployment of a change set | `operations/` | REL-NNN | `release.md` |
| Schema or data change | `data/` | MIG-NNN | `migration.md` |
| Coding/review/onboarding practice | `development/` | `dev-<topic>` (no numbering) | `guide.md` |
| UI, CLI or usability | `ux-and-interfaces/` | Guide (no numbering) | per-tree model |
| How progress went | root `PROGRESS.md` | entry (date + Hecho/Falta/Decision) | `progress-log.md` |

Numbering prefixes are global and never reset: REQ, BL, QT, BUG, DEC, RSK, VULN, RUN,
MIG, REL. IMPL uses the `fase-N` convention; guides use descriptive ids. Always continue
from the last number in the target tree's index; `base.md` owns the `estado` vocabulary
per prefix.

## Operating on an existing .ops tree

1. Read the live README of the target tree (or its copy in `reference/tree/`) to get the
   index, the write/approve pair and the "when to update" rule.
2. Start every new document from its template in `reference/templates/` (or the live
   `.ops/templates/`), preserving the frontmatter contract exactly.
3. Apply the hard rules of the repo instructions: one file per document, ~40 content
   lines max, READMEs under 15 lines, the agent never writes `verified`, no secrets,
   global numbering, cite the AGENTS.md section for reproduced requirements.
4. Update the tree README index and the cross-references (`relaciona`) in the same change.

## Mini-examples

Single-doc types (DEC, RSK, VULN, RUN, MIG, REL) keep ordinary entries as rows in the
tree's index table; only items with their own plan get a file. Registry-row example
(security/vulns.md):

```markdown
| VULN-001 | jwt expira en 24h | alta | abierto | BL-305 reduce a 15min |
```

File example (MIG with own plan, full frontmatter per `migration.md`):

```markdown
---
id: MIG-001
tipo: Migration
type: Migration
title: Agregar org_id a tabla tags
description: Tenancy key en tabla compartida
estado: borrador
dueno: rol:dba
fecha: 2026-10-26
relaciona: [REQ-010]
status: draft
---

## Aplicar y verificar

ALTER TABLE tags ADD COLUMN org_id uuid; backfill por lotes; luego SET NOT NULL;
verificar con conteo de nulos = 0.
```

## Bootstrapping a new project

Create the full skeleton from `reference/templates/` and the structure of
`reference/tree/`:

- `README.md` per tree: use `templates/readme-model.md` (max 15 lines) and this project's
  purpose — do not copy this project's indexes, phases or REQ/DEC contents.
- `templates/base.md` copied **untouched** (it is the frontmatter contract).
- `project/plan.md`, `project/handoff.md`, and root `PROGRESS.md` as empty skeletons per
  the repo instructions, without carrying over this project's state.
- The doc-type vocabulary (REQ, BL, IMPL, QT, BUG, DEC, RSK, REL) and the `estado`
  vocabularies come from `base.md` and are project-independent: keep them.

Bootstrap mode must not propagate this project's contents: no phase names, no decision
histories, no requirement titles. Only the forms.

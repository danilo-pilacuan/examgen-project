# Copilot Instructions - DigitalMe

Permanent instructions for the agent in this repository. Read them at the start of every
session and apply them without being asked again.

> `AGENTS.md` remains the product rulebook (rules, architecture, roadmap, knowledge model).
> This file governs *how the agent works* in the repository; the lifecycle structure it uses
> lives in `.ops/` and is described in section 1.

## 0. Permanent policy: implementation status and handoff

Goal: reproducibility of development - anyone (or any agent) must be able to resume the
project by reading 2-3 files. Therefore, as repository policy:

> **Every agent session in this repo MUST generate and update the implementation status and
> handoff documentation as part of the session's own work, not as an optional extra.**
> Always apply it, without the user having to ask again.

Mandatory session flow:

1. **Start:** read `.ops/project/handoff.md` -> `PROGRESS.md` -> the active phase spec in
   `.ops/implementations/`. Do not redo finished work; continue from the recorded state.
2. **During:** update the documents that describe the work in the same change set as the
   code it describes (phase spec, traceability, test cases). Open BUG files for defects and
   DEC files for open decisions as they appear, continuing global numbering (section 3).
3. **Close (session checklist):** update, in this order:
   - the active phase spec in `.ops/implementations/` (real, verified state - never
     "I think it works");
   - `.ops/qa/traceability.md` and every QT/BUG touched;
   - `.ops/project/handoff.md` (date, branch, tree state, work in progress, gotchas
     discovered in the session);
   - `PROGRESS.md` (one entry: what was done, what is missing, which decision was taken -
     rule 7 of AGENTS.md section 0);
   - atomic commits, and push to `origin` at the end of the session if network is available.

Definition of done: a task is done when the change is implemented + verified (test or
browser, with real output shown) + documented in its phase spec + committed. A session is
done when handoff.md reflects the exact stopping state + the phase/plan maps are updated +
commits are pushed (or marked as pending push in handoff.md).

Before finishing a turn that changes code, verify that the phase spec, the traceability and
PROGRESS.md reflect the change; if they do not, update them or state explicitly why not.

## 1. The `.ops/` development structure (mandatory)

`.ops/` is the lifecycle reference of the project. It is NOT part of the shipped code: it
holds governance, planning and traceability. Every change that affects product state must
be reflected there in the same change set. Boundaries: `.ops` holds management and
governance of the lifecycle; platform knowledge lives in `core/` and `orgs/`; the daily
progress log lives in root `PROGRESS.md`. `.ops` organizes and links; `PROGRESS.md` is the
single source of truth for progress - never duplicate or replace it.

### Tree map

| Directory | Content |
|---|---|
| `.ops/product/` | REQ requirements and product vision |
| `.ops/project/` | phase plan, BL backlog, handoff |
| `.ops/architecture/` | overview, NFR, threat model |
| `.ops/decisions/` | DEC decision register (open/closed) |
| `.ops/governance/` | charter, RACI, DoR/DoD, change control, risks |
| `.ops/qa/` | test strategy, traceability matrix, BUG defects |
| `.ops/implementations/` | per-phase specs + conventions |
| `.ops/ux-and-interfaces/` | CLI, outputs and usability |
| `.ops/security/` | VULN findings, MR security review, periodic checks |
| `.ops/operations/` | RUN runbooks, REL releases, service objectives, incidents |
| `.ops/data/` | MIG migrations, logical data model, tenancy/RLS map |
| `.ops/development/` | coding, review, branching and onboarding guides |
| `.ops/templates/` | OKF 0.2 contract + one template per doc type |

Each directory has its own README (purpose, who writes/approves, when to update, index) -
read it before adding documents there.

**Invoke the `ops-lifecycle` skill before creating or updating any `.ops` document** - it
carries the templates, the OKF 0.2 frontmatter contract, the tree indexes, the numbering
indexes and the bootstrap procedure. The agent never invents a document format, state
vocabulary or numbering from memory; the live `.ops` indexes are always the source.

### Hard rules of `.ops`

- One file per document; large registers (DEC, RSK, BUG, QT, REL) are their own files,
  referenced from their index.
- Content files stay under ~40 content lines; folder READMEs under 15 lines (the root
  `.ops/README.md` may exceed that).
- **The agent never assigns `verified` to itself.** Only a human (rol:propietario or
  rol:funcional) writes `verified: <ISO date>` after reviewing evidence. Without `verified`
  a document is `unverified`.
- Roles: `rol:agente` drafts and executes; `rol:propietario` approves (scope, plan,
  states, phase closure); `rol:funcional` validates knowledge. The RACI matrix is in
  `governance/roles-raci.md`; these governance roles are not the tenant ingestion roles of
  `org.yaml`.
- No secrets and no real client data; synthetic examples only.
- Content that reproduces requirements cites the AGENTS.md section it derives from; do not
  paraphrase it as new rules.
- Do not move or rename `.ops` documents without reading
  `governance/change-control.md`; changes to AGENTS.md or to scope require human approval
  (a DEC must be opened first and answered by the owner before the MR).

### Traceability chain and numbering

- Chain: every BL links a REQ; every IMPL links a BL; every QT links a REQ.
  `.ops/qa/traceability.md` is the coverage matrix (REQ -> BL -> IMPL -> QT with evidence).
- Numbering is global, never per-file: continue REQ-NNN, BL-NNN, IMPL-NNN, QT-NNN, BUG-NNN,
  DEC-NNN, RSK-NNN, VULN-NNN, RUN-NNN, MIG-NNN, REL-NNN from the last number used in the
  corresponding index of the target tree. Guides in `.ops/development/` use descriptive ids
  (`dev-<topic>`), no numbering.

## 2. Handoff document (`.ops/project/handoff.md`)

The support document to pass context to the next session (human or agent). It must be
readable in under 2 minutes and always keep these sections, in this order:

1. **Header (blockquote):** last update date (real date of the day, never estimated),
   active branch and tree state (clean/pending, with hashes of relevant recent commits).
2. **Product state:** what the system is, current phase/release, recent achievements.
3. **How to use it:** read order for a new session: handoff -> `PROGRESS.md` -> active
   phase spec in `.ops/implementations/`.
4. **Local environment:** services, host ports, env file, demo credentials, known
   environment limitations (explicitly not product defects).
5. **How to run and verify:** compose commands, test suites, E2E checks, what requires
   image rebuild vs. hot reload.
6. **Document map:** table of supporting documents and when each one is updated.
7. **Work in progress and pending:** prioritized list; each item states whether it needs
   code.
8. **Session history:** one row per session (scope and result).

Maintenance rules: update the date every time the file is touched; if something is left
unfinished, describe the next concrete step, not just the symptom; never delete gotchas
without confirming they no longer apply.

## 3. Defects (BUG) and open decisions (DEC)

- **Defects** are files `BUG-NNN.md` in `.ops/qa/` (template `templates/defect.md`),
  listed in `qa/README.md`. Required fields: severity (critical/high/medium/low),
  evidence (real command or test output - never claim without running), component and
  location, root cause (file and approximate line; the "why", not just the "where"),
  why it was not caught earlier, fix + verification command, and state
  (abierto / corregido / verificado).
- **Open decisions** are files `DEC-NNN.md` in `.ops/decisions/`: question, phase, and
  options with pros/cons/risks in 6 lines max - then wait for the owner's answer. The
  agent never closes a DEC by itself, never edits AGENTS.md or scope on its own, and
  stops to report contradictions with evidence instead of adapting silently.

## 4. Technical rules of this repository

One rule = one problem that already cost time once; do not document preferences.
Environment specifics (ports, env values, demo users, rebuild triggers) live in
`.ops/project/handoff.md` and are kept current there - do not duplicate them here.

- Platform: GitHub (`danilo-pilacuan/DigitalMe`), CI in GitHub Actions. Git is the source
  of truth; work enters by branch per task and PR.
- Mandatory validation before commit (from `.ops/implementations/conventions.md`):
  - `npx tsc --noEmit` with no errors;
  - CLI validator in `repo` mode green:
    `node --experimental-strip-types tools/index/src/cli.ts --modo=repo`;
  - secret scanner green (gitleaks in CI);
  - phase test suites green, including rejection cases; never weaken tests to make them
    pass.
- Working cadence (from AGENTS.md section 0): one phase and one task at a time; adversarial
  tests written before the feature (every suite includes a case that must be rejected);
  execute before claiming (show real output); SQL in docs is a draft until verified
  against a real Postgres; no system clock in business logic - inject a clock.

### Universal environment gotchas

- PowerShell does not support `&&` -> use `;` or `if ($?) { ... }`.
- Scripts created on Windows get CRLF: `sh` rejects them ("not found") -> `dos2unix` inside
  the container, or generate the script without backslash continuations.
- For HTTP debug inside a Docker network: `docker cp` the script into the container and run
  it with `docker exec <container> sh /tmp/script.sh`.
- `curl.exe` in PowerShell: escape JSON with `\"` inside the body (`--data '{\"k\":1}'`).
- When adding routes/prefixes behind a reverse proxy: test **every HTTP method** of the
  endpoint through the proxy (a working GET does not guarantee PUT/POST/DELETE) and verify
  the rewrite **keeps the prefix** instead of stripping it.

## 5. Language policy

- Never use accented or non-ASCII characters (the set a e i o u n and their uppercase
  variants) in comments, identifiers, or log messages. Comments are plain ASCII English.
- Accented characters are allowed only inside user-facing string literals when the product
  language requires them (for example, Spanish UI text). If a Spanish term must appear in
  a comment or identifier, write it without diacritics (e.g. `numero`, `ejecucion`).
- Keep source files ASCII-safe outside of those user-facing string literals.
- The `.ops` documents of this repo are also written without diacritics; follow the same
  convention when creating new ones, in English or Spanish as the document requires.

## 6. Communication

- Keep answers short, impersonal, and factual. Use Markdown.
- Start every fenced code block with its programming language. Never wrap the whole
  response in triple backticks.
- Use KaTeX for math: `$...$` inline, `$$...$$` for blocks. Use mermaid blocks for
  diagrams when they clarify.
- There is one reply per conversation turn: make it complete and actionable.
- Reply in English even when the user's request is written in Spanish.

## 7. Working rules

- Make minimal, complete changes; do not refactor beyond scope or fix unrelated issues.
- Verify changes with the smallest relevant build, lint, or test command before
  considering the task done.
- Do not invent APIs: confirm symbols and files exist in the repository before using them.
- If a requirement is ambiguous, ask instead of guessing.

## 8. Commit messages

- Conventional Commits format in English, imperative mood, no accents:
  `type(scope): summary`.

## 9. Adopting this file in a project

1. Copy this file to `<repo>/.github/copilot-instructions.md`.
2. Sections 0-3 are process policy: keep them intact across projects. If the project uses
   another name for the state directory, rename `.ops` in this file and in every
   reference; what matters is that a single entry point exists.
3. Adapt section 4 to the project's real technical rules (a rule = a problem already
   suffered, not a preference).
4. Bootstrap the state tree via the `ops-lifecycle` skill (bootstrap mode): create the
   tree of section 1 with its READMEs, `project/plan.md`, `project/handoff.md`,
   `PROGRESS.md`, and seed `templates/base.md` untouched (it is the frontmatter contract).
   The skill guarantees that only the forms are copied, never this project's contents.
5. Keep the global numbering of REQ/BL/IMPL/QT/BUG/DEC and the frontmatter contract:
   that is what makes the history auditable across sessions and AI models.

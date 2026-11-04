# Infrastructure graphs

This document is the visual source of truth for the MVP infrastructure. It uses
Mermaid because the repository already renders Mermaid diagrams in its technical
documentation and the diagrams can be reviewed without a separate modeling server.
The model is C4-like: context, containers, components, and operational flows.

## Reading order

1. **Context**: actors, external systems, and trust boundaries.
2. **Containers**: deployable services and data stores.
3. **Agent components**: conversational and batch LangGraph contexts.
4. **Harnessing**: the primary view for reproducible agent experiments.
5. **Runtime flows**: the two production paths and their evidence outputs.

## Level 1 - system context

```mermaid
flowchart LR
    professor["Professor<br/>human"]
    evaluator["Researcher / evaluator<br/>human"]
    system["Exam Generator<br/>AI-assisted exam authoring system"]
    gateway["USFQ LLM gateway<br/>GLM-5.3-Flash"]
    browser["Browser"]
    gpu["Remote GPU host<br/>Docker deployment"]

    professor -->|"chat, material, review"| browser
    browser --> system
    evaluator -->|"experiment config and acceptance criteria"| system
    system -->|"OpenAI-compatible requests"| gateway
    system -->|"runs on"| gpu
```

The system has two human-facing roles. The professor operates the product and
confirms question verification. The evaluator operates the experiment harness
and interprets evidence; it does not bypass the production guardrails.

## Level 2 - deployment and containers

```mermaid
flowchart TB
    subgraph host["Remote GPU host - isolated Docker network"]
        fe["frontend<br/>Vue 3 + nginx<br/>39005:80"]
        app["exam-app<br/>FastAPI + auth + SSE/WS/REST<br/>39002:8000"]
        agent["agents-backend<br/>LangGraph contexts"]
        db[("postgres-db<br/>PostgreSQL 16 + pgvector<br/>39000:5432")]
        emb["embedding-service<br/>bge-m3<br/>39004:8081"]
        latex["latex-compiler<br/>FastAPI + TeXLive<br/>39003:8080"]
        webui["open-webui<br/>legacy profile<br/>39001:8080"]
        files[("Mounted data<br/>inputs + agent_outputs")]
    end

    professor["Professor browser"]
    llm["USFQ LLM gateway<br/>HTTPS 443"]

    professor -->|"same-origin HTTP / WS / SSE"| fe
    fe -->|"nginx proxy"| app
    webui -->|"OpenAI-compatible /v1"| app
    app --> agent
    agent -->|"checkpoints, subjects,<br/>questions, audit logs"| db
    agent -->|"embeddings"| emb
    emb --> db
    agent -->|"compile LaTeX"| latex
    latex --> files
    agent -->|"chat and generation calls"| llm
    app --> files
```

The local Compose profile uses ports 3000/8000/5432/8080/8081. The remote
deployment uses the high ports shown above and mounts data only below the
deployment user's home directory.

## Level 3 - agent contexts

### 3.1 Conversational context

```mermaid
flowchart TD
    start([User turn]) --> assistant["assistant node<br/>LLM + system prompt"]
    assistant --> decision{"Tool calls?"}
    decision -->|"no"| response["Assistant response"]
    decision -->|"yes"| tools["tools node"]
    tools --> validate["Pydantic args schemas<br/>topic guardrail"]
    validate --> readwrite{"Read or write tool?"}
    readwrite -->|"read"| read["Scoped bank/material tools"]
    readwrite -->|"write"| write["Save/update/delete/generate tools"]
    read --> assistant
    write --> confirmation["Prompt-level human confirmation<br/>for write and verification actions"]
    confirmation --> assistant
    assistant -.-> checkpoint[("Postgres checkpointer<br/>thread history + pending state")]
    tools -.-> events["Typed agent events<br/>EventBus"]
    events --> stream["exam-app SSE / WS"]
    stream --> ui["Chat UI + tool activity"]
```

The conversational graph is a ReAct loop. The checkpointer preserves thread
state, while the event bus exposes tool activity without coupling the agent to
the Vue client. Write tools are explicitly identifiable and their confirmation
policy is part of the prompt contract.

### 3.2 Batch generation context

```mermaid
flowchart LR
    input["Subject + material + blueprint"] --> ingestor["ingestor"]
    ingestor --> planner["planner"]
    planner --> generator["generator"]
    generator --> evaluator["evaluator"]
    evaluator --> route{"Approved?"}
    route -->|"yes"| accept["accept"]
    route -->|"no"| reject["reject + rejection log"]
    reject --> retry{"Retries left?"}
    retry -->|"yes"| generator
    retry -->|"no"| planner
    accept --> remaining{"Specs remain?"}
    remaining -->|"yes"| generator
    remaining -->|"no"| assembler["assembler"]
    assembler --> compiler["compiler"]
    compiler --> compile_retry{"Compilation completed?"}
    compile_retry -->|"no, attempts left"| compiler
    compile_retry -->|"yes or failed"| output["PDF / ZIP / audit state"]
    ingestor -.-> db[("Postgres + pgvector")]
    generator -.-> llm["USFQ LLM gateway"]
    evaluator -.-> llm
    compiler -.-> latex["latex-compiler"]
```

The batch context is stateful within a run. Rejections, retries, accepted
items, LLM call counts, and compilation attempts are explicit state fields and
must remain observable in the run record.

## Level 3 - infrastructure interfaces

```mermaid
flowchart TB
    subgraph api["exam-app interfaces"]
        rest["REST<br/>auth, subjects, material, questions, exams"]
        sse["SSE<br/>chat turn events"]
        ws["WebSocket<br/>chat transport"]
        compat["OpenAI-compatible /v1<br/>legacy OpenWebUI"]
    end
    frontend["Vue frontend"] --> rest
    frontend --> sse
    frontend --> ws
    webui["OpenWebUI legacy"] --> compat
    api --> engine["LangGraphEngine"]
    engine --> conversational["Conversational graph"]
    api --> batch["Exam pipeline services"]
    conversational --> db[("Postgres")]
    batch --> db
    batch --> embedding["Embedding service"]
    batch --> compiler["LaTeX compiler"]
```

## Level 4 - primary graph: agent harnessing

This is the most important graph for the thesis. The harness is an executable
control plane around the agent, not another agent. It selects a profile,
controls the experimental arm, runs the same pipeline in dry or real mode,
captures telemetry, and emits evidence that can be audited after the run.

```mermaid
flowchart TB
    config["experiments.yaml<br/>arms, repeats, blueprints"]
    subjects["subjects.yaml<br/>material and cloned subjects"]
    cli["harness CLI<br/>--experiment + --dry-run / --real"]
    registry["models_registry.py<br/>model profile + parameters"]
    patch["_patch.py<br/>controlled runtime seams"]
    stubs["Deterministic stubs<br/>LLM + embeddings<br/>dry-run, no gateway cost"]
    real["Real adapters<br/>gateway + embeddings<br/>real evidence"]
    index["_indexing.py<br/>register and index clones"]
    pipeline["LangGraph exam pipeline<br/>ingestor -> planner -> generator<br/>-> evaluator -> assembler -> compiler"]
    telemetry["LLMTelemetry<br/>node, latency, chars, usage"]
    metrics["Metric families<br/>quality, diversity, RAG, Bloom,<br/>cost, faithfulness"]
    judge["Optional LLM judge<br/>correlated retrieval evidence"]
    record["runs.jsonl<br/>config, blueprint, items,<br/>rejections, timings, metrics"]
    reports["aggregate + reporting<br/>FINDINGS.md and reports"]
    qa["QA / thesis evidence<br/>reproducible claims"]
    guard["Guardrails<br/>scope rejection, retries,<br/>typed schemas, fail-fast"]

    config --> cli
    subjects --> cli
    cli --> registry
    cli --> index
    cli --> patch
    registry --> pipeline
    patch --> stubs
    patch --> real
    stubs --> pipeline
    real --> pipeline
    index --> pipeline
    guard -.-> pipeline
    pipeline --> telemetry
    pipeline --> record
    telemetry --> metrics
    record --> metrics
    metrics --> judge
    judge --> record
    record --> reports
    reports --> qa
```

### Harness invariants

| Invariant | Implementation evidence |
|---|---|
| Same pipeline in dry and real modes | `test/evaluation/src/harness.py` invokes the production graph; `_patch.py` swaps controlled seams. |
| Every run is attributable | `runs.jsonl` stores experiment, arm, repeat, subject clone, blueprint, and timings. |
| Clone-based robustness | `subjects.yaml` and `ensure_subject()` index the same material under separate subject identities. |
| Guardrails are measured, not implied | Rejections, retry counts, evaluator results, and RAG evidence are persisted. |
| Production code stays testable | Stubs and monkey patches live under `test/evaluation`, not in agent runtime paths. |
| Judge evidence is correlated | Retrieval chunks must be paired with the originating statement before judging faithfulness. |

### Harness execution flow

```mermaid
sequenceDiagram
    participant E as Evaluator
    participant H as Harness
    participant R as Registry
    participant P as Patch layer
    participant G as LangGraph pipeline
    participant M as Metrics
    participant O as runs.jsonl

    E->>H: Select experiment, arm, mode
    H->>R: Load model profile and overrides
    H->>P: Install dry-run or real adapters
    H->>G: Register/index clone and invoke pipeline
    G-->>H: Items, rejections, calls, compilation result
    H->>M: Compute quality, RAG, Bloom, cost, diversity
    M->>O: Append one complete run record
    O-->>E: Reproducible evidence and report inputs
```

## Runtime flow - conversational generation

```mermaid
sequenceDiagram
    participant U as Professor
    participant F as Vue + nginx
    participant A as exam-app
    participant C as Conversational graph
    participant T as Tool layer
    participant L as LLM gateway
    participant D as Postgres

    U->>F: Chat request
    F->>A: SSE/WS/REST with thread_id
    A->>C: Invoke graph with persisted config
    C->>L: Prompt + tool schema
    L-->>C: Answer or tool call
    C->>T: Execute scoped tool
    T->>D: Read/write through service layer
    T-->>A: Typed event and tool result
    A-->>F: Activity, token, done/error
    F-->>U: Render response and artifacts
```

## Runtime flow - batch and evaluation

```mermaid
sequenceDiagram
    participant H as Harness or API
    participant P as Batch graph
    participant E as Embedder
    participant D as Postgres + pgvector
    participant L as LLM gateway
    participant X as LaTeX compiler
    participant O as Output volume

    H->>P: Subject, material paths, blueprint
    P->>E: Index material and create vectors
    E->>D: Store chunks and embeddings
    P->>D: Retrieve relevant chunks
    P->>L: Generate and evaluate each item
    L-->>P: Structured item or evaluator result
    P->>X: Compile approved items
    X->>O: PDF and ZIP artifacts
    P->>D: Persist questions, audit, and counters
    P-->>H: State, metrics inputs, and outputs
```

## Diagram maintenance

Update this file when a container, agent context, harness seam, external
dependency, port, or evidence contract changes. Keep the harnessing graph
aligned with `test/evaluation/src/harness.py`, `projects/agents-backend`, and
the deployment Compose files. Validate Mermaid blocks in the editor preview
before considering the architecture change documented.

Primary sources:

- `deploy/docker-compose.yml` for remote containers and ports.
- `docker/docker-compose.yml` for local runtime wiring.
- `projects/agents-backend/src/agents_backend/conversational/graph.py`.
- `projects/agents-backend/src/agents_backend/exam_pipeline/graph.py`.
- `test/evaluation/src/harness.py`.

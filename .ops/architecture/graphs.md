---
id: architecture-graphs
tipo: Guide
type: Guide
title: C4-like infrastructure graphs
description: Mermaid views of infrastructure, agent contexts, tool harnessing, and evaluation evidence.
estado: borrador
dueno: rol:agente
fecha: 2026-11-04
relaciona: [REQ-001, REQ-002]
status: draft
---

## Purpose

The rendered source is [`docs/graphs.md`](../../docs/graphs.md). It documents
context, containers, agent components, every harness layer and its components,
the 15-tool capability surface, tool sublayers, the tool invocation lifecycle,
runtime flows, and the evaluation harness. The harness view is the primary
thesis view because it explains how agent behavior becomes reproducible evidence.

The agent-specific views use an Agent Harness Reference Model rather than
forcing all concerns into C4 levels: runtime loop, context/state providers,
tool providers, policy/approval, UX/event streaming, and evaluation evidence.
The model is informed by the [Microsoft Agent Harness reference](https://learn.microsoft.com/en-us/agent-framework/concepts/harness)
but is mapped to this repository's LangGraph, EventBus, Postgres, and
`test/evaluation` implementation.

## Update rule

Update this guide and the linked source together when deployment wiring, agent
graphs, harness seams, or evidence contracts change. The agent drafts the
diagram; the owner reviews architecture claims and sets verification status.

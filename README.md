# agentic-decision-ledger

**Decision ≠ Log.**  
A decision is an admissible state transition under explicit constraints at commit-time.

Most agentic repositories can tell you *what happened*.  
Very few can tell you *why it was allowed to happen* at the moment it happened — in a way that survives audits, turnover, and changing constraints.

`agentic-decision-ledger` implements an **Agentic Change Control Plane**:  
a portable, framework-agnostic governance layer that enforces **commit-time decision admissibility** for agent-driven changes.

This is not an agent runtime.  
It is admission control.

---

## The Axioms (non-negotiable)

1) **Logs are forensic. Decisions are contractual.**  
2) **If a decision can’t be justified at commit-time, it doesn’t advance.**  
3) **Replay without intent is archaeology.**  
4) **Velocity comes from legibility, not autonomy.**  
5) **Every agent action is a state transition with an admissibility boundary.**

If these axioms don’t feel operationally necessary, you probably haven’t had to defend an incident weeks later with incomplete context and drifting constraints.

---

## What this repo is (and is not)

This repo is a **minimal, rigorous v0.1 Decision Admissibility Engine**:

- Captures **intent and constraints** as first-class **Decision Contracts**
- Enforces **commit-time admissibility** via deterministic CI gates
- Emits **Decision Records** (human-readable) and **Snapshots** (machine-readable)
- Tracks **decision debt** and **drift** over time
- Produces **safe suggestions as artifacts** (never autonomous edits)

This repo is not:

- An agent framework or runtime
- A promise of correctness, alignment, or “trustworthy autonomy”
- Vendor-specific tooling

You can run it locally.  
You can run it in CI.  
You can remove it without rewriting your system.

---

## Why logs aren’t enough (production reality)

Logs answer: *what happened?*  
Incidents, audits, and handovers demand: *why was this permitted, under which constraints, by whom, and what alternatives were rejected?*

When the “why” lives in implicit prompts, transient chat history, or tribal knowledge:

- Every incident becomes archaeology
- Constraints drift silently across teams
- Accountability becomes post-hoc rationalization
- Velocity collapses under review friction

The marginal cost of **commit-time admissibility** is far lower than the cost of **weeks-later reconstruction**.

---

## Core idea: decision admissibility (commit-time)

A **decision** is treated as a state transition that is allowed only if it is **admissible at commit-time**.

This requires a strict separation:

- **Authorization semantics** (human-owned):  
  intent, scope, constraints, owners, success criteria
- **Execution traces** (automation-owned):  
  timestamps, diffs, metrics, tool outputs, run IDs

Most systems log execution.  
This layer governs admissibility.

---

## The Agentic Change Control Plane

This project implements a **control plane**, not an execution plane.

- Agents (or humans) may propose changes
- The control plane evaluates whether the change is admissible
- Only admissible state transitions reach `main`

This mirrors proven systems architecture:
- Data plane vs control plane
- Runtime vs admission control
- Execution vs governance

---

## Layered architecture (conceptual stack)

**Layer 0 — Intent & constraint capture**  
Human-owned semantics. Explicit. Versioned.

**Layer 1 — Translation / intake interface**  
Structured contracts that reduce variance.

**Layer 2 — Candidate generation**  
LLM or human proposals. No commit rights.

**Layer 3 — Evaluation / scoring**  
Deterministic, logged, certifiable checks.

**Layer 4 — Decision record**  
Alternatives, assumptions, criteria, owner.

**Layer 5 — Execution**  
Constrained, bounded, reversible where possible.

**Layer 6 — Audit & learning**  
Drift detection, decision debt, postmortems.

This repo ships the minimal rails required to implement these layers without imposing an agent framework.

---

## Bootstrap vs install contracts (production reality)

A single gate cannot govern its own evolution using the same contract it enforces for downstream systems.

This repo therefore distinguishes between two contract classes:

- **Repository maintenance contracts**  
  Used for self-governance. Allow bounded changes to the control plane itself.

- **Install / demo contracts**  
  Used to demonstrate how this layer governs agent-driven changes in a target repository.

This separation is the practical application of  
**authorization semantics vs execution traces** to real lifecycle ownership.

---

## External evidence (scaling without coupling)

The control plane does not own global KPIs.  
It **requires that decisions reference them explicitly**.

Decision contracts may point to external evidence sources:

- Metrics systems
- Incident IDs
- FinOps guardrails
- Risk registries

The gate validates **existence, structure, and falsifiability**, not business logic.

This keeps the system:
- Auditable
- Portable
- Enterprise-compatible

---

## Quick demo outcomes (v0.1)

This repo includes two runnable paths:

- **Happy path**  
  An admissible change generates a Decision Record and Snapshot.

- **Failure mode**  
  A non-admissible change is blocked at commit-time with explicit failures.

Artifacts are always generated, even on failure.

---

## Decision Contract (example)

A Decision Contract defines the admissibility boundary.

```yaml
decision_id: DC-2026-001
title: "Enable live price collector with bounded authority"

owner:
  team: "platform"
  approver: "human:@maintainer"

intent:
  goal: "Collect live prices to support latency KPIs."
  scope:
    includes:
      - "collector websocket client"
      - "raw tick storage"
    excludes:
      - "trade execution"
      - "portfolio actions"

assumptions:
  - "Websocket endpoint is stable within SLO variance."
  - "Tick data is non-PII."

constraints:
  bounded_authority:
    can_write_paths:
      - "data/ticks/"
    cannot_touch:
      - ".github/workflows/"
      - "secrets/"
      - "trading/"

alternatives_rejected:
  - option: "Log-only approach"
    rejected_because: "Does not encode admissibility."

success_criteria:
  - "Snapshot and decision record generated"
  - "CI blocks if scope expands"

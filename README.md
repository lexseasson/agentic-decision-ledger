# agentic-decision-ledger

**Decision ≠ Log.**  
A decision is an admissible state transition under explicit constraints at commit-time.

Most agentic repositories can tell you *what happened*.  
Very few can tell you *why it was allowed to happen* at the moment it happened — in a form that survives audits, turnover, and drifting constraints.

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

If these axioms don’t feel operationally necessary, you probably haven’t had to defend an incident weeks later with incomplete context, shifting owners, and evolving constraints.

---

## What this repo is (and is not)

This repo is a **minimal, rigorous Decision Admissibility Engine (v0.1)**:

- Captures **intent + constraints** as first-class **Decision Contracts**
- Enforces **commit-time admissibility** via deterministic CI gates
- Emits **Decision Records** (human-readable) and **Snapshots** (machine-readable)
- Tracks **decision debt** and **drift** as derived signals
- Produces **safe suggestions as artifacts** (never autonomous edits)

This repo is not:

- An agent framework or runtime
- A promise of correctness, alignment, or “trustworthy autonomy”
- Vendor tooling

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

- **Authorization semantics (human-owned)**  
  intent, scope, constraints, owners, success criteria, explicit tradeoffs

- **Execution traces (automation-owned)**  
  timestamps, diffs, metrics, tool outputs, run IDs

Most systems log execution.  
This layer governs admissibility.

---

## The Agentic Change Control Plane

This project implements a **control plane**, not an execution plane.

- Agents (or humans) propose changes
- The control plane evaluates whether the change is admissible
- Only admissible state transitions reach `main`

This mirrors proven system design:
- data plane vs control plane
- runtime vs admission control
- execution vs governance

---

## Decision Stewardship (the operational role)

Agentic systems fail in production when decision intent and boundaries drift faster than the team’s memory.

This repo is designed around an operational role: **Decision Steward**.

A **Decision Steward** preserves **intent**, **boundaries**, and **auditability** of agent-driven change *before execution*:
- prevents silent scope expansion
- prevents “post-hoc” justification
- keeps admissibility legible across turnover

See: `docs/decision_steward_role.md`

---

## Bootstrap vs install contracts (production reality)

A single gate cannot govern its own evolution using the same contract it enforces downstream.

This repo distinguishes two contract classes:

- **Repository maintenance contracts (self-governance)**  
  Allow bounded evolution of the control plane itself: workflow, action, engine, schema.

- **Install/demo contracts (drop-in governance)**  
  Demonstrate governance in a target repository without expanding workflow/secrets surface.

This is the practical application of **authorization semantics vs execution traces** to real lifecycle ownership.

---

## External evidence (scaling without coupling)

The control plane does not own global KPIs.  
It requires decisions to **reference external evidence explicitly** (without runtime coupling):

- incident IDs
- metrics dashboards
- risk registers
- cost guardrails

The gate validates **structure and falsifiability**, not business logic.  
This keeps governance portable and audit-grade.

---

## Quick demo (Windows CMD)

```bat
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .[dev]

examples\happy_path\run_demo.cmd
examples\failure_mode\run_demo.cmd

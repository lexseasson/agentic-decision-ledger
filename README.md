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

## Why this exists (production failure categories)

This control plane targets failure modes that appear repeatedly in real deployments:

- Scope creep via “tiny exceptions” (boundaries erode one PR at a time)
- Post-hoc rationalization (systems explain after the fact, not before the fact)
- Unowned decisions (no accountable owner when incidents happen)
- Non-falsifiable success criteria (nothing measurable, nothing enforceable)
- Evidence drift (metrics/assumptions change, but decisions don’t get revisited)
- Self-governance deadlocks (a gate blocks its own evolution without a maintenance posture)

Outcome: audits become archaeology and velocity collapses.


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
see `docs/v0.2_steward_visibility.md`

---
## Contract classes (so governance doesn't deadlock)

This repo ships three contract patterns:

- **Repository maintenance (self-governance)** — e.g. `DC-REPO-001`  
  Allows bounded changes to the control plane itself (workflows, engine, docs, demo scripts) under explicit authority.

- **Install/demo posture (drop-in)** — e.g. `DC-INSTALL-DEMO-001`  
  Demonstrates a strict target-repo contract (docs-only) that blocks workflow/engine expansion.

- **Example contracts** — e.g. `DC-2026-001`  
  Illustrative contracts for downstream systems. They are not required for maintaining this repo.

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
- Role: [Decision Steward](docs/decision_steward_role.md)
- Visibility: [v0.2 Steward Visibility](docs/v0.2_steward_visibility.md)
- Postures: [Contract postures](docs/contracts_postures.md)

---

## Quick demo (Windows CMD)

```bat
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .[dev]

examples\happy_path\run_demo.cmd
examples\failure_mode\run_demo.cmd

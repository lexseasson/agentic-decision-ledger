# agentic-decision-ledger
**Decision ≠ Log.** A decision is an admissible state transition under explicit constraints at commit-time.

Most agentic repos can tell you *what happened*. Very few can tell you *why it was allowed to happen* at the moment it happened — in a way that survives audits, turnover, and changing constraints.

`agentic-decision-ledger` is a **portable governance layer** you can drop into any repository to make agent actions **legible, admissible, and reviewable** without turning your project into a framework or an “agent OS”.

## The Axioms (non-negotiable)
1) **Logs are forensic. Decisions are contractual.**  
2) **If a decision can’t be justified at commit-time, it doesn’t advance.**  
3) **Replay without intent is archaeology.**  
4) **Velocity comes from legibility, not autonomy.**  
5) **Every agent action is a state transition with an admissibility boundary.**

If these axioms don’t feel operationally necessary, you probably haven’t had to defend an incident weeks later with incomplete context and drifting constraints.

---

## What this repo is (and is not)
This repo is a **minimal, rigorous v0.1 “Decision Admissibility Engine”**:
- It captures **intent + constraints** as a first-class **Decision Contract**.
- It enforces **commit-time decision admissibility** via CI gates.
- It emits **Decision Records** (human-readable) and **Snapshots** (machine-readable).
- It tracks **decision debt** and **drift** over time.
- It produces **safe suggestions** as artifacts (no autonomous edits).

This repo is not:
- A giant framework or agent runtime.
- A promise of correctness, alignment, or “trustworthy autonomy”.
- Vendor tooling. You can run it locally and in CI.

---

## Why logs aren’t enough (production reality)
Logs answer: “what happened?”.  
Incidents, audits, and handovers demand: “why was this permitted, under which constraints, by whom, and what alternatives were rejected?”

When the “why” lives in implicit prompts, transient chat history, or tribal knowledge:
- Every incident becomes **archaeology**.
- Constraints drift silently across teams.
- Accountability becomes post-hoc rationalization.
- Velocity collapses under review friction.

The marginal cost of **commit-time admissibility** is far lower than the cost of **weeks-later reconstruction**.

---

## Core idea: Decision admissibility (commit-time)
A **decision** is treated as a state transition that is allowed only if it is **admissible** at commit-time:

- **Authorization semantics** (human-owned): intent, constraints, priorities, owners, success criteria.
- **Execution traces** (automation-owned): timestamps, tool outputs, metrics, diffs, run ids.

Most systems log execution. This layer governs admissibility.

---

## The stack we advocate (layered architecture)
**Layer 0 — Intent & constraint capture** (governed; human-owned semantics)  
**Layer 1 — Translation / intake interface** (structured request; reduce variance)  
**Layer 2 — Candidate generation** (LLM proposals; probabilistic; no commit rights)  
**Layer 3 — Evaluation / scoring** (deterministic; logged; certifiable)  
**Layer 4 — Decision record** (versioned artifact; alternatives; assumptions; criteria; owner)  
**Layer 5 — Execution** (constrained; reversible where possible; tool boundaries)  
**Layer 6 — Audit & learning** (postmortems; drift detection; decision debt metrics)

This repo ships the minimal rails to implement these layers without imposing an agent framework.

---
## Bootstrap vs install contracts (production reality)

A single gate cannot govern its own evolution using the same contract it enforces for downstream repos.

This repo ships two contract classes:

- **Repo maintenance contract** (self-governance): allows changes to `adl/` and `.github/workflows/` under explicit bounded authority.
- **Install/demo contract** (drop-in): demonstrates how to govern agent changes in a target repo without allowing workflow or secret surface expansion.

This separation is the practical version of **authorization semantics vs execution traces** applied to real lifecycle ownership.

## Quick demo outcomes (v0.1)
v0.1 includes two runnable paths:
- **Happy path**: a candidate proposal passes admissibility gates and generates a Decision Record + Snapshot.
- **Failure-mode path**: a proposal fails commit-time admissibility (missing constraints / weak success criteria / unauthorized scope) and CI blocks the merge.

---

## Decision Contract (example)
A Decision Contract is the **commit-time contract** that makes the state transition admissible.

`decisions/contracts/DC-2026-001.yaml`:
```yaml
decision_id: DC-2026-001
title: "Enable live price collector for BTC/USDT with bounded authority"
owner:
  team: "platform"
  approver: "human:@maintainer_handle"
intent:
  goal: "Collect live prices for BTC/USDT to support latency KPIs and downstream signals."
  scope:
    includes:
      - "collector websocket client"
      - "storage of raw ticks"
    excludes:
      - "trade execution"
      - "portfolio actions"
assumptions:
  - "Exchange websocket endpoint is stable within normal SLO variance."
  - "Tick data is non-PII."
constraints:
  bounded_authority:
    can_write_paths:
      - "data/ticks/"
      - "artifacts/snapshots/"
    cannot_touch:
      - ".github/workflows/"
      - "secrets/"
      - "trading/"
  safety:
    max_requests_per_second: 5
    timeout_seconds: 10
    retries: 3
signals_considered:
  - name: "need_latency_kpi"
    evidence: "incident-2025-11: missing tick latency caused false positives"
  - name: "operability_gap"
    evidence: "no deterministic audit trail for why collector changes were approved"
alternatives_rejected:
  - option: "log-only approach"
    rejected_because: "does not encode admissibility; post-hoc justification risk"
success_criteria:
  - "collector produces snapshot + decision_record on every change"
  - "CI blocks if scope expands to trading paths"
  - "p95 tick ingestion latency metric emitted"
revocation:
  conditions:
    - "drift_score > 0.7 for 3 consecutive runs"
    - "unexpected write outside bounded paths"
  rollback_plan: "disable collector job; revert commit; retain artifacts for audit"

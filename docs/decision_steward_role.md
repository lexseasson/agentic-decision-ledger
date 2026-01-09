
---

# 3) Repo content (ENGLISH): docs/decision_steward_role.md

Crea `docs/decision_steward_role.md` con este contenido:

```md
# Decision Steward (Agentic Decision Stewardship)

## Purpose

The Decision Steward is accountable for preserving **intent**, **boundaries**, and **auditability** of agent-driven changes *before execution*.

This is a governance function in the **control plane**: it prevents silent scope expansion, post-hoc justification drift, and unowned decisions.

## Definition

> A Decision Steward ensures that any agent-driven state transition is **admissible at commit-time** under explicit, falsifiable constraints.

The steward governs admissibility semantics while remaining independent from:
- agent runtimes
- model providers
- orchestration frameworks
- deployment stacks

## What the steward owns

**Contractual semantics**
- intent (goal, scope, exclusions)
- ownership (team + approver)
- constraints (bounded authority, safety limits)
- success criteria (falsifiable)
- alternatives rejected (explicit tradeoffs)
- revocation conditions (when to rollback)

**Audit posture**
- decision records are immutable, versioned artifacts
- snapshots are machine-readable evidence for downstream analysis
- decisions remain legible across turnover and drift

## What the steward does NOT do

- does not generate solutions or code
- does not tune models
- does not execute changes
- does not “monitor everything”
- does not replace security/compliance teams

The steward is not a gatekeeper of productivity.  
The steward is the keeper of admissibility.

## Deliverables (consumable artifacts)

1. **Decision Record** (human-readable)
   - why allowed
   - who owns it
   - which alternatives were rejected
   - what must be true for success

2. **Snapshot** (machine-readable)
   - structured evidence for tooling and analytics
   - deterministic, reproducible output

3. **Stewardship Summary** (executive-facing, v0.3 target)
   - what was admitted / blocked
   - where boundary pressure is rising
   - which decisions are aging into debt

## Operational principle

**Velocity comes from legibility, not autonomy.**  
The steward’s job is to make legibility cheap and drift expensive.

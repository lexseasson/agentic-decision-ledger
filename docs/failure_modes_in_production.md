# Production Failure Categories (Why This Exists)

Agentic systems tend to fail in production for repeatable reasons.  
These failures are rarely “model failures” in isolation — they are governance failures: missing intent, missing boundaries, and missing admissibility.

`agentic-decision-ledger` targets the failure modes that repeatedly show up in real deployments:

## 1) Scope creep via “tiny exceptions”
Boundaries erode one PR at a time:
- “just this once”
- “temporary”
- “it’s only a workflow tweak”
- “we’ll clean it up later”

Over time, the system’s effective authority silently expands beyond what anyone can defend.

## 2) Post-hoc rationalization
The system can explain *after* execution, but cannot justify *before* execution:
- approvals become narrative
- audits become storytelling
- incident reviews become archaeology

Commit-time admissibility forces justification before the change advances.

## 3) Unowned decisions
No accountable owner exists when production breaks:
- unclear approver
- unclear decision intent
- unclear rollback authority

Decision Contracts make ownership explicit and enforceable.

## 4) Non-falsifiable success criteria
Success criteria are vague or cosmetic:
- “improve performance”
- “be more robust”
- “reduce errors”

If it can’t be falsified, it can’t be governed.

## 5) Evidence drift
Assumptions, metrics, and external conditions change, but decisions don’t:
- a decision stays “approved” long after its evidence base is invalid
- teams inherit decisions without inheriting intent

The result is governance debt.

## 6) Self-governance deadlocks
A gate cannot safely govern its own evolution with the same constraints it enforces downstream.

You need:
- **maintenance contracts** for evolving the control plane
- **install contracts** for governing downstream changes

## The predictable outcome if you ignore these
Audits become archaeology.  
Turnover destroys context.  
Velocity collapses under review friction.

This project makes legibility cheap and drift expensive.

# Audit Failure Taxonomy (v0.2)

This repo is a governance/control-plane layer for agentic development: it detects and blocks policy drift, emits audit-grade artifacts, and provides deterministic evidence for review, incident response, and organizational memory.

This document defines a **failure taxonomy** used to reason about production-grade governance failures (not “bugs”). Each category is mapped to **observable signals** and **artifacts** produced by the gate/steward.

---

## How to read this taxonomy

Each category includes:

- **What it is**: the failure mode in plain architecture terms.
- **Observable signals**: what we can measure deterministically from diffs/contracts/runs.
- **Primary artifacts**: where evidence is written (audit trail + steward reports).
- **Controls**: how the system prevents or reduces the failure.
- **Why hiring managers care**: what this prevents in real-world delivery and audit.

---

## Artifact coverage map (by intent)

- `artifacts/audit/audit_trail.ndjson`  
  Append-only ledger of governance events: routing, diff strategy, contract chosen, admitted/blocked, hashes.

- `artifacts/steward/boundary_pressure_report.json`  
  Quantifies “pressure” on governance boundaries: out-of-bounds attempts, forbidden touches, surface expansion.

- `artifacts/steward/contract_drift_report.json`  
  Semantic deltas across sensitive contract fields; classifies drift as low/medium/high.

- `artifacts/steward/decision_debt_report.json`  
  Portfolio-level “decision debt” scoring: revalidation age, evidence gaps, owner ambiguity, volatility, recurrence.

- `artifacts/steward/evidence_refs.json`  
  Explicit missing/required evidence references for assumptions/KPIs/policies.

- `artifacts/steward/stewardship_summary.md`  
  1-page executive summary: “what changed, what risk increased, what to do next”.

---

## Coverage principle (non-negotiable)

This taxonomy is intentionally designed to be:
- **Deterministic**: computable from contracts + diffs + run metadata (no subjective “AI judgement” required).
- **Audit-grade**: each conclusion can be traced to evidence in `audit_trail` and hashed steward artifacts.
- **Operational**: failure categories map to **controls** you can enforce in CI and discuss in an incident review.

---

# A) Core production categories (the “original 6”)

## A1. Scope creep / authority creep
**What it is**  
A change expands allowed write surfaces or reduces exclusions, gradually converting a bounded agent into an unbounded one.

**Observable signals**
- `constraints.bounded_authority.can_write_paths` expands
- `intent.scope.excludes` shrinks or disappears
- New paths show up frequently in `changed_paths` beyond historical baseline

**Primary artifacts**
- `contract_drift_report.json` (sensitive-field drift)
- `boundary_pressure_report.json` (surface spread + recurrence)
- `audit_trail.ndjson` (who/when/route)

**Controls**
- Contract drift classification: expansion ⇒ medium/high risk
- Require explicit alternatives + rationale for expansions

**Why hiring managers care**
Prevents “silent escalation” that causes catastrophic privilege accumulation in CI/agents.

---

## A2. Forbidden-domain contact
**What it is**  
Changes touch explicitly prohibited domains (e.g., workflows, secrets, execution plane).

**Observable signals**
- Any changed path matches `cannot_touch` patterns
- Attempted modifications to `.github/workflows/`, `secrets/`, execution directories

**Primary artifacts**
- `audit_trail.ndjson` (forbidden touches, block reason)
- `boundary_pressure_report.json` (forbidden_touch_attempts)

**Controls**
- Hard block in admissibility evaluation
- Steward reports make repeated attempts visible

**Why hiring managers care**
This is the difference between “policy exists” and “policy is enforceable.”

---

## A3. Non-falsifiable success criteria (governance theater)
**What it is**  
Contracts claim “success” in ways that cannot be tested, enabling post-hoc rationalization.

**Observable signals**
- success criteria without measurable outputs
- language patterns that imply unverifiable claims

**Primary artifacts**
- Decision record check `success_criteria_falsifiable`
- Stewardship summary flags governance-quality regressions

**Controls**
- CI blocks or warns (strict mode can hard-fail)
- Decision record captures the rationale for failure

**Why hiring managers care**
Prevents “we shipped governance” that cannot survive audit or incident review.

---

## A4. Alternatives missing / weak decision quality
**What it is**  
A change is adopted without enumerating rejected alternatives; design intent becomes untraceable.

**Observable signals**
- `alternatives_rejected` absent/empty
- Repeated drift without recorded tradeoffs

**Primary artifacts**
- Decision record check `alternatives_provided`
- `decision_debt_report.json` increases debt for missing design trace

**Controls**
- Contract checks enforce baseline decision quality
- Debt scoring makes low-quality decisions visible over time

**Why hiring managers care**
Reduces knowledge loss and prevents repeated “reinvention” after turnover.

---

## A5. Ownership ambiguity / stewardship gap
**What it is**  
No accountable approver, stale handles, or unclear team ownership; governance becomes orphaned.

**Observable signals**
- `owner.team` missing
- `owner.approver` format invalid or stale/placeholder
- High debt on “owner_ambiguity”

**Primary artifacts**
- `decision_debt_report.json` (owner_ambiguity signals + recommendations)
- `stewardship_summary.md` flags “unowned governance”

**Controls**
- Require approver semantics; debt triggers revalidation
- Escalate when governance surfaces change without clear owner

**Why hiring managers care**
Orphaned control planes are incident factories.

---

## A6. Evidence rot / KPI mismatch
**What it is**  
Assumptions/KPIs/policies evolve but the contract is not revalidated; evidence diverges from reality.

**Observable signals**
- Assumptions without evidence references
- KPI names/thresholds change across docs/issues but contract doesn’t
- Drift in `intent.goal` without refreshed evidence

**Primary artifacts**
- `evidence_refs.json` (missing refs + required refs)
- `decision_debt_report.json` (evidence_gap dimension)

**Controls**
- Evidence references are explicit, reviewable, and hashable
- Revalidation policy triggers on age or boundary pressure

**Why hiring managers care**
Prevents audits failing because “the documentation says X but reality is Y.”

---

# B) Additional categories (muscle + audit reality)

## B1. Policy bypass by indirection
**What it is**  
Avoid touching forbidden paths directly, but modify a generator/script that produces them.

**Observable signals**
- Changes in scripts that generate `.github/workflows/` or execution artifacts
- Outputs appear in artifact logs or CI workspace without direct diffs to forbidden paths

**Primary artifacts**
- `audit_trail.ndjson` (records route, changed paths, and determinism inputs)
- `contract_drift_report.json` (flags expansions enabling generation paths)
- `boundary_pressure_report.json` (surface spread)

**Controls**
- Treat generator surfaces as governance surfaces (maintenance posture)
- Record generator-touch as a high-attention signal even if forbidden paths are untouched

**Why hiring managers care**
This is how real-world policy gets bypassed. Detecting it early saves weeks of incident response.

---

## B2. Permission laundering
**What it is**  
Changes appear “safe” (e.g., docs) but influence execution through templating, codegen, or side effects.

**Observable signals**
- “Docs-only” diffs that are later correlated with behavior changes
- Repeated docs-only merges around incidents or regressions (requires portfolio correlation)

**Primary artifacts**
- `boundary_pressure_report.json` (pressure on docs-only posture)
- `audit_trail.ndjson` (route + diff strategy for reproducibility)

**Controls**
- Install-demo posture stays strict; mixed changes must route to maintenance/product posture
- Evidence refs required when docs claim behavioral changes or KPIs

**Why hiring managers care**
It prevents the classic “it was just docs” incident.

---

## B3. Evidence mismatch (policy vs reality)
**What it is**  
Evidence claims (SLO/KPI/security posture) don’t match what’s enforced or measured.

**Observable signals**
- Evidence refs missing for key assumptions
- Drift in goal without updated measurement references

**Primary artifacts**
- `evidence_refs.json`
- `decision_debt_report.json`

**Controls**
- Explicit evidence refs + missing refs list
- Debt-driven revalidation triggers (time and/or pressure)

**Why hiring managers care**
Makes audits survivable and prevents “hand-wavy compliance.”

---

## B4. Meta-governance drift (constitutional drift)
**What it is**  
The gate itself changes (workflows/action/engine) in ways that weaken enforcement, without explicit “constitutional” tracking.

**Observable signals**
- Changes in `.github/workflows`, `integrations/`, `adl/`, `pyproject.toml`, `tests/`
- Reduced strictness, removed checks, altered routing logic

**Primary artifacts**
- `audit_trail.ndjson` (route=maintenance + rationale)
- `contract_drift_report.json` (sensitive deltas if the maintenance contract itself changes)
- `stewardship_summary.md` (flags meta-governance risk)

**Controls**
- Maintenance contract governs governance
- Drift classification marks safety relaxations as high risk

**Why hiring managers care**
Control planes fail when they can be changed “quietly.”

---

## B5. Non-deterministic diff selection (CI noise / false governance)
**What it is**  
Base/head selection or event handling yields inconsistent changed paths; governance becomes non-repeatable.

**Observable signals**
- Different changed path sets across reruns for the same PR
- Missing/empty base SHA in certain event types
- Route changes across reruns without code changes

**Primary artifacts**
- `audit_trail.ndjson` logs:
  - diff strategy
  - base/head SHAs present
  - event payload class (PR vs push)
  - computed changed paths count

**Controls**
- Deterministic diff strategy per event type
- Record `inputs_hash` so the run can be reproduced

**Why hiring managers care**
A governance system that isn’t deterministic isn’t governance.

---

## B6. Artifact spoofing (non-verifiable outputs)
**What it is**  
Artifacts are written but are not cryptographically tied to inputs/run state.

**Observable signals**
- Missing `inputs_hash` / `artifact_hash`
- Artifacts exist without corresponding audit entries
- Artifact fields inconsistent with changed paths / contract route

**Primary artifacts**
- `audit_trail.ndjson` with:
  - `inputs_hash`
  - per-artifact sha256 hashes
- Each steward artifact includes `integrity`

**Controls**
- Hash inputs + outputs and store in append-only audit trail
- Optionally verify hashes in CI as a separate step

**Why hiring managers care**
Prevents “compliance theater”: evidence must be verifiable.

---

## B7. Owner handle staleness / identity drift
**What it is**  
Approver/owner identifiers become stale; approvals are unenforceable or meaningless.

**Observable signals**
- approver value uses placeholders
- repeated “human:@maintainer_handle” without resolution
- no mapping to org identity (or stale mapping)

**Primary artifacts**
- `decision_debt_report.json` (owner_ambiguity dimension)
- `stewardship_summary.md` recommendation

**Controls**
- Enforce approver format and optionally validate against allowed set (future)
- Revalidation triggers when stale

**Why hiring managers care**
Makes ownership auditable and actionable.

---

## B8. Posture misclassification (wrong contract routed)
**What it is**  
The system routes a change to the wrong contract posture (install vs product vs maintenance), producing a false sense of control:
- overly strict routing blocks legitimate work, or
- overly permissive routing admits risky work.

**Observable signals**
- `route` changes for the same change-set across reruns
- “Docs-only” route when `changed_paths` includes non-doc surfaces (or the opposite)
- Base SHA missing causes routing to fall back incorrectly

**Primary artifacts**
- `audit_trail.ndjson`:
  - route + reason
  - diff strategy
  - base/head presence
  - inputs_hash
- `stewardship_summary.md` flags “routing instability”

**Controls**
- Route logic treated as governance surface (maintenance posture)
- Route reason recorded as evidence; changes to route logic require DC-REPO-001
- Portfolio correlation can detect repeated posture flips as a systemic risk

**Why hiring managers care**
Incorrect routing is equivalent to a broken access-control policy: it fails silently and causes real incidents.

---

# C) Implementation notes (what becomes “real” next)

1. These categories must be **computable deterministically** from:
   - contracts,
   - diffs/changed paths,
   - run metadata,
   - evaluation outputs.

2. Any category that cannot be measured deterministically is documented as:
   - “requires external adapter” (future), but never as a core control.

3. Every run should emit artifacts even when the gate fails:
   - failure runs are incident-response gold.

4. Portfolio-level governance (separate repo) should aggregate:
   - boundary pressure trends,
   - debt/drift rollups,
   - routing stability,
   - evidence coverage across contracts.

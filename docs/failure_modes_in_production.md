1. Silent Scope Expansion

Description
An agent gradually begins to act outside its originally intended scope without explicit authorization.

Production Impact

Small changes accumulate into system-wide risk.

Reviews miss the inflection point where behavior becomes unsafe.

Rollbacks become non-local and expensive.

Root Cause
Implicit authority inferred from past success rather than explicitly bounded intent.

Stewardship Mitigation

Explicit bounded authority in Decision Contracts.

Commit-time diff inspection against declared scope.

Boundary pressure tracking over time.

2. Post-hoc Justification Drift

Description
Rationales for decisions are reconstructed after outcomes are known.

Production Impact

Audit narratives change depending on audience.

Trust erodes across engineering, product, and leadership.

Incident response becomes defensive rather than diagnostic.

Root Cause
Intent is stored informally (prompts, chat history, tribal knowledge).

Stewardship Mitigation

Intent captured ex-ante as a contractual artifact.

Alternatives rejected must be recorded before execution.

Decision records are immutable and versioned.

3. Unowned Decisions

Description
No clear human owner can be identified for a decision that materially affected the system.

Production Impact

Escalations stall.

Accountability diffuses.

Future decisions become overly conservative.

Root Cause
Automation without explicit ownership semantics.

Stewardship Mitigation

Mandatory owner and approver fields in every Decision Contract.

Ownership treated as a governance primitive, not metadata.

4. Non-falsifiable Success

Description
A decision is declared “successful” without criteria that could ever be disproven.

Production Impact

Systems cannot be objectively evaluated.

Failures hide behind narrative success.

Continuous improvement stalls.

Root Cause
Success defined aspirationally instead of operationally.

Stewardship Mitigation

Enforced falsifiable success criteria.

Criteria evaluated independently of narrative outcomes.

Success treated as a measurable claim, not a belief.

5. Governance Self-Deadlock

Description
The governance mechanism cannot evolve without bypassing itself.

Production Impact

Informal exceptions proliferate.

Controls become performative.

Teams learn to work around governance instead of with it.

Root Cause
A single contract class attempts to govern both itself and downstream systems.

Stewardship Mitigation

Explicit separation between:

Bootstrap / maintenance contracts

Install / downstream contracts

Governance evolution treated as a first-class decision domain.

6. Archaeological Incidents

Description
Weeks or months after an incident, teams must reconstruct intent from logs and artifacts never designed to explain “why”.

Production Impact

Incident reviews turn speculative.

Lessons learned are shallow or incorrect.

Organizational memory decays.

Root Cause
Logs optimized for execution, not admissibility.

Stewardship Mitigation

Decision Records and Snapshots as primary artifacts.

Intent preserved alongside execution traces.

Replay with meaning, not just data.

Summary

These failures are not edge cases.
They are structural outcomes of agentic systems without decision stewardship.

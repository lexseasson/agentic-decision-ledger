# Decision Contract (v0.1)

A Decision Contract is a commit-time contract that makes a state transition admissible.

It is **not** a log, and **not** a prompt. It is human-owned semantics:
- intent (goal + scope)
- constraints (bounded authority)
- success criteria (falsifiable)
- owner/approver

The automation produces execution traces and evidence snapshots.

## Required fields (v0.1)
- decision_id
- title
- owner.team
- owner.approver
- intent.goal
- constraints.bounded_authority.can_write_paths
- constraints.bounded_authority.cannot_touch
- success_criteria

## Why falsifiability matters
If success criteria cannot be evaluated, admission becomes narrative, not governance.
Incident reviews fail when admission is justified post-hoc.

## Schema
See: `adl/schema/decision_contract.schema.json`

# Contract postures: install vs maintenance vs example

This repository uses three decision contracts, each representing a different **posture**.

## 1) Maintenance posture (DC-REPO-001)

**What it is:** the self-governance / bootstrap contract.  
**What it governs:** changes to the control-plane product itself.

Typical examples:
- `.github/workflows/`
- `integrations/github-action/`
- `adl/` (engine, schema, CLI)
- `pyproject.toml`, tests
- and also product-facing surfaces in this repo: `README.md`, `docs/`, `examples/`, `scripts/`, `decisions/contracts/`

**Why:** without an explicit maintenance posture, the gate cannot evolve safely and will drift into implicit exemptions or deadlocks.

## 2) Install demo posture (DC-INSTALL-DEMO-001)

**What it is:** a drop-in demo contract meant for **target repositories** adopting ADL.  
**Rule:** allows only `docs/` (and `artifacts/`) changes.  
**Purpose:** demonstrate bounded authority and show what “green vs red” looks like with minimal setup.

This contract is intentionally strict and is NOT intended to govern the evolution of this repository’s engine/workflows.

## 3) Example/demo posture (DC-2026-001)

**What it is:** a broader demo posture than install-demo.  
**Typical surface:** `docs/`, `examples/`, `scripts/`, `decisions/contracts/`, `artifacts/` while still forbidding `.github/workflows/`, `secrets/`, `trading/`.

## How CI chooses a posture

The GitHub Action selects a single governing contract per diff:

1. If the change touches maintenance surfaces, route to **DC-REPO-001**.
2. If the change is docs/artifacts only, route to **DC-INSTALL-DEMO-001**.
3. Otherwise, fallback to **DC-2026-001** (example/demo).

This keeps the gate deterministic and prevents “multi-contract collisions” on the same diff.

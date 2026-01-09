from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _list_contracts(contracts_dir: Path) -> list[Path]:
    if not contracts_dir.exists():
        return []
    return sorted([p for p in contracts_dir.glob("*.y*ml") if p.is_file()])


def _load_yaml(p: Path) -> dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        obj = yaml.safe_load(f)
    return obj if isinstance(obj, dict) else {}


def _score_contract(contract: dict[str, Any]) -> tuple[float, list[str]]:
    reasons: list[str] = []
    debt = 0.0

    if not contract.get("assumptions"):
        debt += 0.15
        reasons.append("missing_assumptions")

    if not contract.get("signals_considered"):
        debt += 0.15
        reasons.append("missing_signals_considered")

    if not contract.get("alternatives_rejected"):
        debt += 0.25
        reasons.append("missing_alternatives_rejected")

    sc = contract.get("success_criteria", [])
    if not isinstance(sc, list) or len(sc) == 0:
        debt += 0.45
        reasons.append("missing_success_criteria")

    debt = max(0.0, min(1.0, debt))
    return debt, reasons


def compute_debt_report(repo_root: Path, artifacts_dir: Path) -> dict[str, Any]:
    contracts_dir = repo_root / "decisions" / "contracts"
    contracts = _list_contracts(contracts_dir)

    items: list[dict[str, Any]] = []
    for p in contracts:
        c = _load_yaml(p)
        score, reasons = _score_contract(c)
        items.append(
            {
                "decision_id": str(c.get("decision_id", p.stem)),
                "contract_path": str(p.relative_to(repo_root).as_posix()),
                "debt_score": round(score, 3),
                "reasons": reasons,
            }
        )

    avg = round(sum(i["debt_score"] for i in items) / len(items), 3) if items else 0.0

    snapshots_dir = artifacts_dir / "snapshots"
    snapshot_count = len(list(snapshots_dir.glob("*.json"))) if snapshots_dir.exists() else 0

    return {
        "schema_version": "v0.1",
        "contracts": items,
        "portfolio": {
            "contract_count": len(items),
            "avg_debt_score": avg,
            "snapshot_count": snapshot_count,
            "drift": {
                "status": "stub_v0.1",
                "note": "Drift detection lands in v0.2+ using historical snapshots.",
            },
        },
    }

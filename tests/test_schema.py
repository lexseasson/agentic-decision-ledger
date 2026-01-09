from pathlib import Path

import yaml

from adl.engine.evaluator import evaluate_admissibility


def test_contract_schema_accepts_example() -> None:
    repo_root = Path(".").resolve()
    contract_path = repo_root / "decisions" / "contracts" / "DC-2026-001.yaml"
    assert contract_path.exists()

    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    assert isinstance(contract, dict)

    res = evaluate_admissibility(
        repo_root=repo_root,
        contract_path=contract_path,
        contract=contract,
        strict=False,
    )
    assert res.decision_id.startswith("DC-")
    assert isinstance(res.checks, list)

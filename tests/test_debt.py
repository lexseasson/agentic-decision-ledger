from pathlib import Path

from adl.engine.debt import compute_debt_report


def test_debt_report_runs() -> None:
    repo_root = Path(".").resolve()
    artifacts_dir = repo_root / "artifacts"
    report = compute_debt_report(repo_root=repo_root, artifacts_dir=artifacts_dir)
    assert "portfolio" in report
    assert "contracts" in report

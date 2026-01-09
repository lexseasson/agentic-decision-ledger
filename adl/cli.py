from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer
import yaml

from adl.artifacts.decision_record import write_decision_record
from adl.artifacts.snapshot import write_snapshot
from adl.engine.debt import compute_debt_report
from adl.engine.evaluator import evaluate_admissibility
from adl.utils.io import ensure_dir, now_utc_iso

app = typer.Typer(
    add_completion=False,
    help="Agentic Decision Ledger (adl) - commit-time decision admissibility.",
)


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    artifacts_dir: Path
    contracts_dir: Path


def _load_contract(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Contract not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Decision contract must be a YAML mapping/object.")
    return data


def _resolve_paths(repo_root: Path, artifacts_dir: Path | None) -> Paths:
    rr = repo_root.resolve()
    artifacts = (artifacts_dir or (rr / "artifacts")).resolve()
    contracts = (rr / "decisions" / "contracts").resolve()
    return Paths(repo_root=rr, artifacts_dir=artifacts, contracts_dir=contracts)


@app.command("check")
def check(
    contract: Path = typer.Option(..., "--contract", "-c", help="Path to Decision Contract YAML."),
    repo_root: Path = typer.Option(Path("."), "--repo-root", help="Repo root (default: .)."),
    artifacts_dir: Path | None = typer.Option(
        None,
        "--artifacts-dir",
        help="Artifacts dir (default: ./artifacts).",
    ),
    write_artifacts: bool = typer.Option(
        False,
        "--write-artifacts",
        help="Write decision_record + snapshot.",
    ),
    strict: bool = typer.Option(
        True,
        "--strict/--non-strict",
        help="Strict blocks on warnings.",
    ),
) -> None:
    """
    Validate a Decision Contract and run deterministic admissibility checks.
    Exit code 1 if non-admissible.
    """
    paths = _resolve_paths(repo_root, artifacts_dir)
    contract_path = contract.resolve()

    contract_obj = _load_contract(contract_path)
    result = evaluate_admissibility(
        repo_root=paths.repo_root,
        contract_path=contract_path,
        contract=contract_obj,
        strict=strict,
    )

    if write_artifacts:
        ensure_dir(paths.artifacts_dir / "decision_records")
        ensure_dir(paths.artifacts_dir / "snapshots")
        ts = now_utc_iso()

        record_path = (
            paths.artifacts_dir
            / "decision_records"
            / f"{result.decision_id}.decision_record.md"
        )
        snapshot_path = paths.artifacts_dir / "snapshots" / f"{result.decision_id}.snapshot.json"

        write_decision_record(out_path=record_path, result=result, timestamp=ts)
        write_snapshot(out_path=snapshot_path, result=result, timestamp=ts)

    typer.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))

    if not result.admitted:
        raise typer.Exit(code=1)


@app.command("record")
def record(
    contract: Path = typer.Option(..., "--contract", "-c", help="Path to Decision Contract YAML."),
    repo_root: Path = typer.Option(Path("."), "--repo-root", help="Repo root (default: .)."),
    artifacts_dir: Path | None = typer.Option(
        None,
        "--artifacts-dir",
        help="Artifacts dir (default: ./artifacts).",
    ),
    strict: bool = typer.Option(
        True,
        "--strict/--non-strict",
        help="Strict blocks on warnings.",
    ),
) -> None:
    """
    Run admissibility checks and ALWAYS write artifacts.
    Intended for CI gates.
    """
    check(
        contract=contract,
        repo_root=repo_root,
        artifacts_dir=artifacts_dir,
        write_artifacts=True,
        strict=strict,
    )


@app.command("snapshot")
def snapshot(
    contract: Path = typer.Option(..., "--contract", "-c", help="Path to Decision Contract YAML."),
    repo_root: Path = typer.Option(Path("."), "--repo-root", help="Repo root (default: .)."),
    artifacts_dir: Path | None = typer.Option(
        None,
        "--artifacts-dir",
        help="Artifacts dir (default: ./artifacts).",
    ),
) -> None:
    """
    Produce a machine-readable snapshot for the current evaluation context.
    Snapshot does not imply admission; it is evidence.
    """
    paths = _resolve_paths(repo_root, artifacts_dir)
    contract_path = contract.resolve()
    contract_obj = _load_contract(contract_path)

    result = evaluate_admissibility(
        repo_root=paths.repo_root,
        contract_path=contract_path,
        contract=contract_obj,
        strict=False,
    )

    ensure_dir(paths.artifacts_dir / "snapshots")
    ts = now_utc_iso()
    out_path = paths.artifacts_dir / "snapshots" / f"{result.decision_id}.snapshot.json"
    write_snapshot(out_path=out_path, result=result, timestamp=ts)
    typer.echo(str(out_path))


@app.command("debt")
def debt(
    repo_root: Path = typer.Option(Path("."), "--repo-root", help="Repo root (default: .)."),
    artifacts_dir: Path | None = typer.Option(
        None,
        "--artifacts-dir",
        help="Artifacts dir (default: ./artifacts).",
    ),
    out_json: bool = typer.Option(True, "--json/--no-json", help="Emit JSON to stdout."),
) -> None:
    """
    Compute decision debt/drift metrics as derived report (not contractual).
    """
    paths = _resolve_paths(repo_root, artifacts_dir)
    report = compute_debt_report(repo_root=paths.repo_root, artifacts_dir=paths.artifacts_dir)

    if out_json:
        typer.echo(json.dumps(report, indent=2, sort_keys=True))
    else:
        typer.echo("Use --json to emit report.")
        raise typer.Exit(code=2)


def main() -> None:
    try:
        app()
    except BrokenPipeError:
        sys.exit(0)


if __name__ == "__main__":
    main()

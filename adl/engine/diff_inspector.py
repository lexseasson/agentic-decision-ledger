from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from adl.engine.types import CheckResult


@dataclass(frozen=True)
class BoundaryEval:
    checks: list[CheckResult]
    warnings: list[str]
    failures: list[str]


def _run_git(repo_root: Path, args: list[str]) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    if p.returncode != 0:
        return ""
    return p.stdout.strip()


def collect_changed_paths(repo_root: Path) -> list[str]:
    staged = _run_git(repo_root, ["diff", "--cached", "--name-only"])
    if staged:
        return [line.strip() for line in staged.splitlines() if line.strip()]

    wt = _run_git(repo_root, ["diff", "--name-only"])
    if wt:
        return [line.strip() for line in wt.splitlines() if line.strip()]

    base = _run_git(repo_root, ["rev-parse", "--verify", "HEAD^"])
    if base:
        head = _run_git(repo_root, ["rev-parse", "HEAD"])
        diff = _run_git(repo_root, ["diff", "--name-only", f"{base}..{head}"])
        if diff:
            return [line.strip() for line in diff.splitlines() if line.strip()]

    return []


def _prefix_match(path: str, prefixes: list[str]) -> bool:
    norm = path.replace("\\", "/")
    for p in prefixes:
        pp = str(p).replace("\\", "/").rstrip("/") + "/"
        if norm.startswith(pp) or norm == pp.rstrip("/"):
            return True
    return False


def evaluate_boundaries(contract: dict[str, Any], changed_paths: list[str]) -> BoundaryEval:
    checks: list[CheckResult] = []
    warnings: list[str] = []
    failures: list[str] = []

    constraints: dict[str, Any] = {}
    if isinstance(contract.get("constraints"), dict):
        constraints = contract["constraints"]

    ba: dict[str, Any] = {}
    if isinstance(constraints.get("bounded_authority"), dict):
        ba = constraints["bounded_authority"]

    can_write = ba.get("can_write_paths", [])
    cannot_touch = ba.get("cannot_touch", [])

    if not isinstance(can_write, list) or not isinstance(cannot_touch, list):
        failures.append(
            "bounded_authority fields must be lists: can_write_paths and cannot_touch."
        )
        checks.append(
            CheckResult("bounded_authority_shape", "FAIL", "Invalid bounded_authority structure.")
        )
        return BoundaryEval(checks=checks, warnings=warnings, failures=failures)

    checks.append(
        CheckResult("bounded_authority_shape", "PASS", "bounded_authority is well-formed.")
    )

    implicit_allow = ["decisions/contracts/", "artifacts/", "docs/"]

    forbidden_hits: list[str] = []
    for p in changed_paths:
        if _prefix_match(p, cannot_touch):
            forbidden_hits.append(p)

    if forbidden_hits:
        failures.append(f"Forbidden paths modified: {forbidden_hits}")
        checks.append(
            CheckResult("forbidden_paths_untouched", "FAIL", "Touched forbidden paths.")
        )
    else:
        checks.append(
            CheckResult("forbidden_paths_untouched", "PASS", "No forbidden paths touched.")
        )

    out_of_bounds: list[str] = []
    allowed_prefixes = [*can_write, *implicit_allow]
    for p in changed_paths:
        if not p.strip():
            continue
        if not _prefix_match(p, allowed_prefixes):
            out_of_bounds.append(p)

    if out_of_bounds:
        failures.append(f"Out-of-bounds modifications: {out_of_bounds}")
        checks.append(
            CheckResult("bounded_authority_respected", "FAIL", "Changes exceed bounded authority.")
        )
    else:
        checks.append(
            CheckResult("bounded_authority_respected", "PASS", "Changes respect bounded authority.")
        )

    if len(changed_paths) == 0:
        warnings.append(
            "No changed paths detected. Verify git diff strategy matches your commit/CI flow."
        )
        checks.append(CheckResult("diff_detected", "WARN", "No diff detected."))
    else:
        checks.append(
            CheckResult(
                "diff_detected",
                "PASS",
                f"{len(changed_paths)} changed paths detected.",
            )
        )

    return BoundaryEval(checks=checks, warnings=warnings, failures=failures)

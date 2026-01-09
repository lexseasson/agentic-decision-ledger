from __future__ import annotations

import json
import os
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


def _run_git(repo_root: Path, args: list[str]) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    return p.returncode, p.stdout.strip()


def _prefix_match(path: str, prefixes: list[str]) -> bool:
    norm = path.replace("\\", "/")
    for p in prefixes:
        pp = str(p).replace("\\", "/").rstrip("/") + "/"
        if norm.startswith(pp) or norm == pp.rstrip("/"):
            return True
    return False


def _paths_from_github_event(repo_root: Path) -> list[str] | None:
    """
    Deterministic diff selection in CI:
    - pull_request: base sha -> head sha
    - push: before sha -> after sha
    Uses GITHUB_EVENT_PATH JSON when present.
    """
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        return None

    p = Path(event_path)
    if not p.exists():
        return None

    try:
        payload: Any = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

    event_name = os.getenv("GITHUB_EVENT_NAME", "")

    base_sha: str | None = None
    head_sha: str | None = None

    if event_name == "pull_request":
        pr = payload.get("pull_request", {})
        base_sha = pr.get("base", {}).get("sha")
        head_sha = pr.get("head", {}).get("sha")

    elif event_name == "push":
        base_sha = payload.get("before")
        head_sha = payload.get("after") or os.getenv("GITHUB_SHA")

        # GitHub uses all-zero base for some events; treat as unknown
        if isinstance(base_sha, str) and set(base_sha) == {"0"}:
            base_sha = None

    if not base_sha or not head_sha:
        return None

    code, out = _run_git(repo_root, ["diff", "--name-only", f"{base_sha}..{head_sha}"])
    if code != 0 or not out:
        return []

    return [line.strip() for line in out.splitlines() if line.strip()]


def collect_changed_paths(repo_root: Path) -> list[str]:
    # 1) CI deterministic path selection (preferred)
    ci_paths = _paths_from_github_event(repo_root=repo_root)
    if ci_paths is not None:
        return ci_paths

    # 2) Local dev: staged first
    code, staged = _run_git(repo_root, ["diff", "--cached", "--name-only"])
    if code == 0 and staged:
        return [line.strip() for line in staged.splitlines() if line.strip()]

    # 3) Local dev: working tree
    code, wt = _run_git(repo_root, ["diff", "--name-only"])
    if code == 0 and wt:
        return [line.strip() for line in wt.splitlines() if line.strip()]

    # 4) Fallback: last commit diff if available
    code, base = _run_git(repo_root, ["rev-parse", "--verify", "HEAD^"])
    if code == 0 and base:
        code2, head = _run_git(repo_root, ["rev-parse", "HEAD"])
        if code2 == 0 and head:
            code3, diff = _run_git(repo_root, ["diff", "--name-only", f"{base}..{head}"])
            if code3 == 0 and diff:
                return [line.strip() for line in diff.splitlines() if line.strip()]

    return []


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

    checks.append(CheckResult("bounded_authority_shape", "PASS", 
                              "bounded_authority is well-formed."))

    implicit_allow = ["decisions/contracts/", "artifacts/", "docs/"]

    forbidden_hits: list[str] = []
    for p in changed_paths:
        if _prefix_match(p, cannot_touch):
            forbidden_hits.append(p)

    if forbidden_hits:
        failures.append(f"Forbidden paths modified: {forbidden_hits}")
        checks.append(CheckResult("forbidden_paths_untouched", "FAIL", 
                                  "Touched forbidden paths."))
    else:
        checks.append(CheckResult("forbidden_paths_untouched", "PASS", 
                                  "No forbidden paths touched."))

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
            "No changed paths detected. Verify CI diff strategy or stage changes locally."
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

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from adl.engine.diff_inspector import collect_changed_paths, evaluate_boundaries
from adl.engine.types import AdmissibilityResult, CheckResult
from adl.utils.io import load_json_schema


def _schema_validate(contract: dict[str, Any], schema_path: Path) -> list[str]:
    schema = load_json_schema(schema_path)
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(contract), key=lambda e: e.path)
    msgs: list[str] = []
    for e in errors:
        loc = ".".join([str(p) for p in e.path]) if e.path else "<root>"
        msgs.append(f"{loc}: {e.message}")
    return msgs


def _has_falsifiable_success_criteria(contract: dict[str, Any]) -> bool:
    criteria = contract.get("success_criteria", [])
    if not isinstance(criteria, list):
        return False

    tokens = [
        "%",
        "p95",
        "p99",
        "latency",
        "blocks",
        "ci",
        "fails",
        "error",
        "slo",
        "ms",
        "seconds",
    ]
    joined = " ".join([str(x) for x in criteria]).lower()
    return any(t in joined for t in tokens)


def evaluate_admissibility(
    repo_root: Path,
    contract_path: Path,
    contract: dict[str, Any],
    strict: bool,
) -> AdmissibilityResult:
    checks: list[CheckResult] = []
    warnings: list[str] = []
    failures: list[str] = []

    decision_id = str(contract.get("decision_id", "UNKNOWN"))

    schema_path = Path(__file__).resolve().parents[1] / "schema" / "decision_contract.schema.json"
    schema_errors = _schema_validate(contract, schema_path)
    if schema_errors:
        failures.extend([f"schema: {m}" for m in schema_errors])
        checks.append(
            CheckResult("contract_schema_valid", "FAIL", "Decision contract schema violations.")
        )
    else:
        checks.append(CheckResult("contract_schema_valid", "PASS", "Contract matches schema."))

    if _has_falsifiable_success_criteria(contract):
        checks.append(
            CheckResult(
                "success_criteria_falsifiable",
                "PASS",
                "Success criteria appear falsifiable.",
            )
        )
    else:
        msg = (
            "Success criteria look non-falsifiable; "
            "add measurable thresholds or explicit CI conditions."
        )
        if strict:
            failures.append(msg)
            checks.append(CheckResult("success_criteria_falsifiable", "FAIL", msg))
        else:
            warnings.append(msg)
            checks.append(CheckResult("success_criteria_falsifiable", "WARN", msg))

    alts = contract.get("alternatives_rejected", [])
    if isinstance(alts, list) and len(alts) >= 1:
        checks.append(CheckResult("alternatives_provided", "PASS", "Alternatives are present."))
    else:
        msg = "No alternatives rejected captured. Weak audit posture."
        if strict:
            failures.append(msg)
            checks.append(CheckResult("alternatives_provided", "FAIL", msg))
        else:
            warnings.append(msg)
            checks.append(CheckResult("alternatives_provided", "WARN", msg))

    changed = collect_changed_paths(repo_root=repo_root)
    boundary = evaluate_boundaries(contract=contract, changed_paths=changed)
    
        # Hardening: in strict mode, "no diff detected" is non-admissible.
    if strict:
        for c in boundary.checks:
            if c.name == "diff_detected" and c.status == "WARN":
                failures.append(
                    "Strict mode: no diff detected. " \
                    "Stage changes with git add or ensure CI diff strategy."
                )
                break

    warnings.extend(boundary.warnings)
    failures.extend(boundary.failures)
    checks.extend(boundary.checks)

    admitted = len(failures) == 0
    return AdmissibilityResult(
        decision_id=decision_id,
        admitted=admitted,
        checks=checks,
        changed_paths=changed,
        warnings=warnings,
        failures=failures,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str  # PASS/WARN/FAIL
    detail: str


@dataclass(frozen=True)
class AdmissibilityResult:
    decision_id: str
    admitted: bool
    checks: list[CheckResult]
    changed_paths: list[str]
    warnings: list[str]
    failures: list[str]
    schema_version: str = "v0.1"

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "admitted": self.admitted,
            "schema_version": self.schema_version,
            "checks": [c.__dict__ for c in self.checks],
            "changed_paths": self.changed_paths,
            "warnings": self.warnings,
            "failures": self.failures,
        }

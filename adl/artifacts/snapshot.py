from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adl.engine.types import AdmissibilityResult


def write_snapshot(out_path: Path, result: AdmissibilityResult, timestamp: str) -> None:
    payload: dict[str, Any] = {
        "decision_id": result.decision_id,
        "timestamp": timestamp,
        "admitted": result.admitted,
        "checks": [c.__dict__ for c in result.checks],
        "changed_paths": result.changed_paths,
        "warnings": result.warnings,
        "failures": result.failures,
        "schema_version": result.schema_version,
    }
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

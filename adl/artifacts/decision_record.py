from __future__ import annotations

from pathlib import Path

from adl.engine.types import AdmissibilityResult


def write_decision_record(out_path: Path, result: AdmissibilityResult, timestamp: str) -> None:
    lines: list[str] = []
    status = "ADMITTED (commit-time)" if result.admitted else "REJECTED (commit-time)"

    lines.append(f"# Decision Record: {result.decision_id}")
    lines.append(f"Status: {status}")
    lines.append(f"Timestamp: {timestamp}")
    lines.append("")
    lines.append("## Deterministic evaluation")
    for c in result.checks:
        lines.append(f"- {c.name}: {c.status} — {c.detail}")
    lines.append("")
    lines.append("## Changed paths (evidence)")
    if result.changed_paths:
        for p in result.changed_paths:
            lines.append(f"- {p}")
    else:
        lines.append("- <none detected>")
    lines.append("")
    if result.failures:
        lines.append("## Failures (non-admissible)")
        for f in result.failures:
            lines.append(f"- {f}")
        lines.append("")
    if result.warnings:
        lines.append("## Warnings")
        for w in result.warnings:
            lines.append(f"- {w}")
        lines.append("")
    lines.append("## Notes")
    lines.append(
        "This record preserves commit-time admissibility rationale. Logs explain execution; "
        "this document explains why the transition was allowed."
    )
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")

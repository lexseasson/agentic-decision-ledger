from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from adl.engine.diff_inspector import collect_changed_paths

REPO_ROOT = Path(".")


def _normalize(paths: Iterable[str]) -> list[str]:
    return [p.replace("\\", "/") for p in paths]


def _any_prefix(paths: list[str], prefixes: list[str]) -> bool:
    for p in paths:
        for pref in prefixes:
            pref_norm = pref.rstrip("/")
            if p.startswith(pref) or p == pref_norm:
                return True
    return False


def _docs_or_artifacts_only(paths: list[str]) -> bool:
    if not paths:
        return False
    return all(p.startswith("docs/") or p.startswith("artifacts/") for p in paths)


def main() -> None:
    changed = _normalize(collect_changed_paths(REPO_ROOT))

    maint_surface = [
        "README.md",
        "docs/",
        "examples/",
        "scripts/",
        ".github/workflows/",
        "adl/",
        "integrations/",
        "pyproject.toml",
        "tests/",
    ]

    if _any_prefix(changed, maint_surface):
        print("decisions/contracts/DC-REPO-001.yaml")
        return

    if _docs_or_artifacts_only(changed):
        print("decisions/contracts/DC-INSTALL-DEMO-001.yaml")
        return

    print("decisions/contracts/DC-2026-001.yaml")


if __name__ == "__main__":
    main()

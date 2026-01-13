from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from adl.engine.diff_inspector import collect_changed_paths

REPO_ROOT = Path(".")


def norm(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def any_prefix(paths: Iterable[str], prefixes: Iterable[str]) -> bool:
    for p in paths:
        pp = norm(p)
        for pref in prefixes:
            pref_n = norm(pref)
            if pp == pref_n.rstrip("/") or pp.startswith(pref_n):
                return True
    return False


def is_docs_only(paths: list[str]) -> bool:
    if not paths:
        return False
    return all(norm(p).startswith(("docs/", "artifacts/")) for p in paths)


def main() -> None:
    changed = collect_changed_paths(REPO_ROOT)

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

    if any_prefix(changed, maint_surface):
        print("decisions/contracts/DC-REPO-001.yaml")
        return

    if is_docs_only(changed):
        print("decisions/contracts/DC-INSTALL-DEMO-001.yaml")
        return

    print("decisions/contracts/DC-2026-001.yaml")


if __name__ == "__main__":
    main()

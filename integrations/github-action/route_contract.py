from collections.abc import Iterable
from pathlib import Path

from adl.engine.diff_inspector import collect_changed_paths

REPO_ROOT = Path(".")


def _norm(p: str) -> str:
    return p.replace("\\", "/")


CHANGED = [_norm(p) for p in collect_changed_paths(REPO_ROOT)]


def any_prefix(paths: Iterable[str], prefixes: Iterable[str]) -> bool:
    for p in paths:
        for pref in prefixes:
            pref_norm = pref.rstrip("/")
            if p.startswith(pref) or p == pref_norm:
                return True
    return False


def is_docs_or_artifacts_only(paths: list[str]) -> bool:
    # Empty change sets should not be treated as docs-only
    if not paths:
        return False
    return all(p.startswith("docs/") or p.startswith("artifacts/") for p in paths)


# Maintenance surfaces (product/control-plane) => maintenance posture contract
MAINT_SURFACE = [
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

if any_prefix(CHANGED, MAINT_SURFACE):
    print("decisions/contracts/DC-REPO-001.yaml")
elif is_docs_or_artifacts_only(CHANGED):
    print("decisions/contracts/DC-INSTALL-DEMO-001.yaml")
else:
    print("decisions/contracts/DC-2026-001.yaml")

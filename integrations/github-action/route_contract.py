from pathlib import Path
from adl.engine.diff_inspector import collect_changed_paths

REPO_ROOT = Path(".")
CHANGED = collect_changed_paths(REPO_ROOT)

def any_prefix(prefixes):
    for p in CHANGED:
        pp = p.replace("\\", "/")
        for pref in prefixes:
            if pp.startswith(pref) or pp == pref.rstrip("/"):
                return True
    return False

# If README or any product/control-plane surface changes, require maintenance contract
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

if any_prefix(MAINT_SURFACE):
    print("decisions/contracts/DC-REPO-001.yaml")
else:
    # If docs-only (install demo posture)
    if all(p.replace("\\", "/").startswith("docs/") or p.replace("\\", "/").startswith("artifacts/") 
           for p in CHANGED):
        print("decisions/contracts/DC-INSTALL-DEMO-001.yaml")
    else:
        # Example contract for docs/examples/scripts-only changes
        print("decisions/contracts/DC-2026-001.yaml")

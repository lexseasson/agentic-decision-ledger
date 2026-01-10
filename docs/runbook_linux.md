
---

## 3) `docs/runbook_linux.md` completo (pegalo tal cual)

```md
# Runbook (Linux / bash)

This runbook is optimized for zero-context execution by reviewers and hiring managers.
It assumes a POSIX-like shell (bash) and Git.

## 0) Preconditions
- Linux environment (or WSL)
- Git installed (`git --version`)
- Python 3.11+ installed (`python3 --version`)
- You are inside the repo root (where `pyproject.toml` exists)

## 1) Create and activate a virtual environment
From repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ".[dev]"

# Runbook (Windows / CMD.exe)

This runbook is optimized for **zero-context execution** by reviewers and hiring managers.
It assumes Windows CMD.exe (not PowerShell).

## 0) Preconditions
- Windows 10/11
- Git installed (`git --version`)
- Python 3.11+ installed (`python --version`)
- You are inside the repo root (where `pyproject.toml` exists)

## 1) Create and activate a virtual environment
From repo root:

```bat
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip

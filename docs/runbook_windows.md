# Runbook (Windows / CMD.exe)

## Prerequisites
- Windows + `cmd.exe`
- Git installed
- Python 3.11+
- A virtualenv recommended

## Setup
```bat
cd path\to\agentic-decision-ledger
python -m venv .venv
call .venv\Scripts\activate
python -m pip install -U pip
pip install -e .

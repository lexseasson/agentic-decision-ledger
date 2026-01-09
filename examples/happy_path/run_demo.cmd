@echo off
setlocal enabledelayedexpansion

echo [HAPPY PATH] forcing an admissible change in docs/ and staging it
echo.

rem Ensure we're in a git repo
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERROR: Not inside a git repository.
  exit /b 1
)

if not exist docs mkdir docs

set FILE=docs\demo_note.md
echo demo line %DATE% %TIME%>> "%FILE%"

rem Stage the change so --cached detects it deterministically
git add "%FILE%"

echo.
echo Running admissibility gate (record)...
adl record --contract examples\happy_path\decision_contract.yaml --strict
if errorlevel 1 (
  echo.
  echo ERROR: Gate failed unexpectedly for happy path.
  exit /b 1
)

echo.
echo Done. Artifacts written under artifacts\decision_records and artifacts\snapshots
endlocal

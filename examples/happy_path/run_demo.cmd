@echo off
setlocal enabledelayedexpansion

echo [HAPPY PATH] forcing an admissible change in docs/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERROR: Not inside a git repository.
  exit /b 1
)

echo demo note >> docs\demo_note.md
git add docs\demo_note.md

echo.
echo Running admissibility gate (record)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
if errorlevel 1 (
  echo ERROR: gate failed but should have passed.
  exit /b 1
)

echo.
echo Done. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

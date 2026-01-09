@echo off
setlocal enabledelayedexpansion

echo [FAILURE MODE] forcing a forbidden change in .github/workflows/ and staging it
echo.

rem Ensure we're in a git repo
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERROR: Not inside a git repository.
  exit /b 1
)

if not exist .github mkdir .github
if not exist .github\workflows mkdir .github\workflows

set FILE=.github\workflows\_forbidden_touch.yml
echo # forbidden edit %DATE% %TIME%>> "%FILE%"

rem Stage the forbidden change
git add "%FILE%"

echo.
echo Running admissibility gate (should FAIL)...
adl record --contract examples\failure_mode\decision_contract.yaml --strict

if errorlevel 1 (
  echo.
  echo OK: Gate failed as expected (non-admissible change detected).
  exit /b 0
)

echo.
echo ERROR: Gate passed but should have failed. Investigate diff detection and boundaries.
exit /b 2

@echo off
setlocal

echo [HAPPY PATH] forcing an admissible change in docs/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 goto NOT_IN_REPO

REM Require clean repo (protect user)
git diff --quiet
if errorlevel 1 goto DIRTY_REPO
git diff --cached --quiet
if errorlevel 1 goto DIRTY_REPO

echo demo note>>docs\demo_note.md
git add docs\demo_note.md

echo.
echo Running admissibility gate (record)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup only demo artifacts (no global clean)
git reset --hard >nul 2>&1
if exist "docs\demo_note.md" del /q "docs\demo_note.md" >nul 2>&1

if not "%RC%"=="0" goto HAPPY_FAILED

echo.
echo Done. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

:HAPPY_FAILED
echo ERROR: gate failed but should have passed.
exit /b 1

:DIRTY_REPO
echo ERROR: repo is not clean. Please commit/stash first.
exit /b 1

:NOT_IN_REPO
echo ERROR: Not inside a git repository.
exit /b 1

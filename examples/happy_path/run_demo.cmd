@echo off
setlocal

echo [HAPPY PATH] forcing an admissible change in docs/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 goto NOT_IN_REPO

REM Start clean so diff is deterministic
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

echo demo note>>docs\demo_note.md
git add docs\demo_note.md

echo.
echo Running admissibility gate (record)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

if not "%RC%"=="0" goto HAPPY_FAILED

echo.
echo Done. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

:HAPPY_FAILED
echo ERROR: gate failed but should have passed.
exit /b 1

:NOT_IN_REPO
echo ERROR: Not inside a git repository.
exit /b 1

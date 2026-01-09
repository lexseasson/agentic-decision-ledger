@echo off
setlocal

REM Ensure repo root
cd /d "%~dp0.."
if errorlevel 1 (
  echo ERROR: could not cd to repo root.
  exit /b 1
)

REM Abort if workspace not clean (protect user)
git diff --quiet
if errorlevel 1 (
  echo ERROR: working tree has unstaged changes. Please commit/stash first.
  exit /b 1
)
git diff --cached --quiet
if errorlevel 1 (
  echo ERROR: index has staged changes. Please commit/stash first.
  exit /b 1
)

echo Running happy path...
call "examples\happy_path\run_demo.cmd"
if errorlevel 1 (
  echo ERROR: happy path failed.
  exit /b 1
)

echo.
echo Running failure mode...
call "examples\failure_mode\run_demo.cmd"
if errorlevel 1 (
  echo ERROR: failure mode script returned failure (it should exit 0 after expected gate failure).
  exit /b 1
)

echo.
echo All demos completed. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

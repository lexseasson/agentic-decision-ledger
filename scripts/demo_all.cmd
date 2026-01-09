@echo off
setlocal

REM Ensure we are at repo root (scripts\..)
cd /d "%~dp0.."
if errorlevel 1 (
  echo ERROR: could not cd to repo root.
  exit /b 1
)

if not exist "examples\happy_path\run_demo.cmd" (
  echo ERROR: missing examples\happy_path\run_demo.cmd
  exit /b 1
)

if not exist "examples\failure_mode\run_demo.cmd" (
  echo ERROR: missing examples\failure_mode\run_demo.cmd
  exit /b 1
)

echo Running happy path...
call "examples\happy_path\run_demo.cmd"
if errorlevel 1 (
  echo.
  echo ERROR: happy path failed.
  exit /b 1
)

REM Clean between runs to avoid cross-contamination
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

echo.
echo Running failure mode...
call "examples\failure_mode\run_demo.cmd"
if errorlevel 1 (
  echo.
  echo ERROR: failure mode script returned failure (it should return 0 after expected gate failure).
  exit /b 1
)

REM Final clean
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

echo.
echo All demos completed. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

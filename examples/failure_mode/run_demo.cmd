@echo off
setlocal enabledelayedexpansion

echo [FAILURE MODE] forcing a forbidden change in .github/workflows/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERROR: Not inside a git repository.
  exit /b 1
)

echo # forbidden touch > .github\workflows\_forbidden_touch.yml
git add .github\workflows\_forbidden_touch.yml

echo.
echo Running admissibility gate (should FAIL)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts

if errorlevel 1 (
  echo.
  echo OK: gate failed as expected (forbidden touch).
  exit /b 0
)

echo.
echo ERROR: If you see this line, something is wrong (gate should have failed).
exit /b 1

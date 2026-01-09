@echo off
setlocal

echo [FAILURE MODE] forcing a forbidden change in .github/workflows/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 goto NOT_IN_REPO

REM Start clean so diff is deterministic
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

echo # forbidden touch>.github\workflows\_forbidden_touch.yml
git add .github\workflows\_forbidden_touch.yml

echo.
echo Running admissibility gate (should FAIL)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup (always)
git reset --hard >nul 2>&1
git clean -fd >nul 2>&1

if not "%RC%"=="0" goto EXPECTED_FAIL

echo.
echo ERROR: gate passed but should have failed.
exit /b 1

:EXPECTED_FAIL
echo.
echo OK: gate failed as expected (forbidden touch).
exit /b 0

:NOT_IN_REPO
echo ERROR: Not inside a git repository.
exit /b 1

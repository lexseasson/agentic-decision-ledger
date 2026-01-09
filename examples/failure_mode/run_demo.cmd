@echo off
setlocal

echo [FAILURE MODE] forcing a forbidden change in .github/workflows/ and staging it
echo.

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 goto NOT_IN_REPO

REM Require clean repo (protect user)
git diff --quiet
if errorlevel 1 goto DIRTY_REPO
git diff --cached --quiet
if errorlevel 1 goto DIRTY_REPO

echo # forbidden touch>.github\workflows\_forbidden_touch.yml
git add .github\workflows\_forbidden_touch.yml

echo.
echo Running admissibility gate (should FAIL)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup only demo artifacts (no global clean)
git reset --hard >nul 2>&1
if exist ".github\workflows\_forbidden_touch.yml" del /q ".github\workflows\_forbidden_touch.yml" >nul 2>&1

if not "%RC%"=="0" goto EXPECTED_FAIL

echo ERROR: gate passed but should have failed.
exit /b 1

:EXPECTED_FAIL
echo OK: gate failed as expected (forbidden touch).
exit /b 0

:DIRTY_REPO
echo ERROR: repo is not clean. Please commit/stash first.
exit /b 1

:NOT_IN_REPO
echo ERROR: Not inside a git repository.
exit /b 1

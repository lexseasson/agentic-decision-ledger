@echo off
setlocal

echo [FAILURE MODE] forcing a forbidden change in .github/workflows/ and staging it
echo(

REM Ensure we are in a git repo and move to repo root
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 goto NOT_IN_REPO

for /f "delims=" %%R in ('git rev-parse --show-toplevel') do set "REPO_ROOT=%%R"
cd /d "%REPO_ROOT%"
if errorlevel 1 (
  echo ERROR: could not cd to repo root.
  exit /b 1
)

REM Allow only artifacts/ to be dirty (untracked) - everything else must be clean
call :ASSERT_CLEAN_EXCEPT_ARTIFACTS
if errorlevel 1 exit /b 1

REM Create forbidden touch
echo # forbidden touch>".github\workflows\_forbidden_touch.yml"
git add ".github\workflows\_forbidden_touch.yml" >nul 2>&1

echo(
echo Running admissibility gate (should FAIL)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup forbidden file safely (no global hard reset)
git restore --staged ".github\workflows\_forbidden_touch.yml" >nul 2>&1
git restore ".github\workflows\_forbidden_touch.yml" >nul 2>&1
if exist ".github\workflows\_forbidden_touch.yml" del /q ".github\workflows\_forbidden_touch.yml" >nul 2>&1

REM Expected: non-zero (gate fails)
if not "%RC%"=="0" goto EXPECTED_FAIL

echo ERROR: gate passed but should have failed.
exit /b 1

:EXPECTED_FAIL
echo OK: gate failed as expected (forbidden touch).
exit /b 0

:ASSERT_CLEAN_EXCEPT_ARTIFACTS
git diff --quiet
if errorlevel 1 (
  echo ERROR: working tree has tracked modifications. Please commit/stash first.
  exit /b 1
)
git diff --cached --quiet
if errorlevel 1 (
  echo ERROR: index has staged changes. Please commit/stash first.
  exit /b 1
)

for /f "delims=" %%U in ('git ls-files --others --exclude-standard') do (
  echo %%U | findstr /b /c:"artifacts/" >nul
  if errorlevel 1 (
    echo ERROR: untracked files outside artifacts/ detected: %%U
    echo Please commit/stash/clean before running demos.
    exit /b 1
  )
)

exit /b 0

:NOT_IN_REPO
echo ERROR: Not inside a git repository.
exit /b 1

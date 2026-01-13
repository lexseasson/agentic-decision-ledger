@echo off
setlocal

echo [HAPPY PATH] forcing an admissible change in docs/ and staging it
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

REM Allow only artifacts/ to be dirty (untracked). Everything else must be clean.
call :ASSERT_CLEAN_EXCEPT_ARTIFACTS
if errorlevel 1 exit /b 1

REM Demo change
echo demo note>>docs\demo_note.md
git add docs\demo_note.md >nul 2>&1

echo(
echo Running admissibility gate (record)...
adl record --contract decisions\contracts\DC-INSTALL-DEMO-001.yaml --strict --artifacts-dir artifacts
set "RC=%errorlevel%"

REM Cleanup demo file safely (no global hard reset)
git restore --staged docs\demo_note.md >nul 2>&1
git restore docs\demo_note.md >nul 2>&1
if exist "docs\demo_note.md" del /q "docs\demo_note.md" >nul 2>&1

if not "%RC%"=="0" goto HAPPY_FAILED

echo(
echo Done. Check artifacts\decision_records and artifacts\snapshots
exit /b 0

:HAPPY_FAILED
echo ERROR: gate failed but should have passed.
exit /b 1

:ASSERT_CLEAN_EXCEPT_ARTIFACTS
REM Fail if there are tracked changes anywhere
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

REM Fail if there are untracked files outside artifacts/
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

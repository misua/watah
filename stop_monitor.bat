@echo off
REM Stop cloud monitoring

cd /d "%~dp0"

echo Stopping monitors...

REM Kill pythonw processes running the scheduler
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| find "PID:"') do (
    taskkill /PID %%a /F >nul 2>&1
)

REM Also kill python processes with monitor_scheduler
for /f "tokens=2" %%a in ('wmic process where "CommandLine like '%%monitor_scheduler%%'" get ProcessId ^| findstr [0-9]') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo Done.

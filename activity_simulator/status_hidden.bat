@echo off
REM Check if the hidden service is running

echo Checking for running service...
echo.

REM Check for pythonw processes
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I "pythonw.exe" >NUL

if %ERRORLEVEL% EQU 0 (
    echo Status: RUNNING
    echo.
    echo Pythonw processes:
    wmic process where "name='pythonw.exe'" get ProcessId,CommandLine 2>nul | findstr /I "stealth"
) else (
    echo Status: NOT RUNNING
)

echo.
if exist .runtime.pid (
    echo PID file exists: .runtime.pid
    type .runtime.pid
) else (
    echo PID file not found
)

pause

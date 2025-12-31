@echo off
REM Start the activity simulator in hidden/disguised mode
cd /d "%~dp0"

REM Check if already running via PID file
if exist "activity_sim.pid" (
    for /f %%i in (activity_sim.pid) do set PID=%%i
    tasklist /FI "PID eq %PID%" 2>nul | find /I "%PID%" >nul
    if not errorlevel 1 (
        echo Service is already running (PID: %PID%)
        exit /b 1
    ) else (
        echo Stale PID file found, cleaning up...
        del activity_sim.pid 2>nul
        del .runtime.pid 2>nul
    )
)

REM Activate virtual environment if it exists
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

REM Run stealth_runner.py with python (not pythonw) for debugging
REM Use pythonw for true stealth mode once working
echo Starting activity simulator...
start /B /MIN python stealth_runner.py

REM Wait for PID file to be created
timeout /t 3 /nobreak >nul

REM Verify it started
if exist "activity_sim.pid" (
    for /f %%i in (activity_sim.pid) do set PID=%%i
    echo Service started successfully (PID: %PID%)
    echo %PID% > .runtime.pid
    echo Log file: activity_sim.log or activity_sim_stealth.log
) else (
    echo ERROR: Service failed to start!
    echo Check activity_sim_stealth.log for errors
    exit /b 1
)

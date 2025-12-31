@echo off
REM GCP Activity Monitor - Start monitoring service
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

REM Run the monitoring service directly (not in background for debugging)
echo Starting GCP monitoring service...
python gcp_monitoring.py

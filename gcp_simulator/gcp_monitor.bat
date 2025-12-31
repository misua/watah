@echo off
REM GCP Activity Monitor - Start monitoring service
cd /d "%~dp0"
echo [GCP Monitor] Current directory: %CD%

REM Check if already running via PID file
if exist "activity_sim.pid" (
    for /f %%i in (activity_sim.pid) do set PID=%%i
    tasklist /FI "PID eq %PID%" 2>nul | find /I "%PID%" >nul
    if not errorlevel 1 (
        echo [GCP Monitor] Service is already running (PID: %PID%)
        pause
        exit /b 1
    ) else (
        echo [GCP Monitor] Stale PID file found, cleaning up...
        del activity_sim.pid 2>nul
        del .runtime.pid 2>nul
    )
)

REM Activate virtual environment
echo [GCP Monitor] Activating virtual environment...
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
    echo [GCP Monitor] Activated: ..\venv
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
    echo [GCP Monitor] Activated: venv
) else (
    echo [GCP Monitor] WARNING: No virtual environment found!
)

REM Show Python being used
echo [GCP Monitor] Python: 
where python
python --version

REM Run the monitoring service
echo [GCP Monitor] Starting service...
echo ================================================
python gcp_monitoring.py

REM If we get here, the script exited
echo ================================================
echo [GCP Monitor] Service stopped
pause

@echo off
REM Azure Portal Configuration Service
REM Initializes Azure portal navigation helper

REM Check if already running
if exist ".azconfig.pid" (
    echo Azure configuration service is already running
    exit /b 1
)

REM Activate virtual environment from activity_simulator
if exist ..\activity_simulator\venv\Scripts\activate.bat (
    call ..\activity_simulator\venv\Scripts\activate.bat
)

REM Run in background with hidden window using pythonw (no console)
start /B /MIN pythonw azure_setup.py

REM Store runtime marker
echo %TIME% > .azconfig.pid

echo Azure portal helper started
timeout /t 2 /nobreak >nul

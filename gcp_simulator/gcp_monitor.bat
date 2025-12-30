@echo off
REM Start the activity simulator in hidden/disguised mode

REM Check if already running
if exist ".runtime.pid" (
    echo Service is already running
    exit /b 1
)

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run in background with hidden window
start /B /MIN pythonw stealth_runner.py

REM Store the PID (approximate - Windows limitation)
echo %TIME% > .runtime.pid

echo Service started in stealth mode
timeout /t 2 /nobreak >nul

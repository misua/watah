@echo off
cd /d "%~dp0"
echo Stopping Activity Simulator...

REM Activate virtual environment
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

REM Check if PID file exists
if not exist "activity_sim.pid" (
    echo Activity simulator is not running (no PID file found)
    del .runtime.pid 2>nul
    goto :end
)

REM Read PID and kill process
for /f %%i in (activity_sim.pid) do set PID=%%i
echo Killing process %PID%...

REM Try graceful termination first
taskkill /PID %PID% 2>nul
if errorlevel 1 (
    echo Process not found or already stopped
) else (
    echo Process terminated
)

REM Force kill if still running
timeout /t 2 /nobreak >nul
tasklist /FI "PID eq %PID%" 2>nul | find /I "%PID%" >nul
if not errorlevel 1 (
    echo Force killing...
    taskkill /F /PID %PID% 2>nul
)

REM Clean up PID files
del activity_sim.pid 2>nul
del .runtime.pid 2>nul

echo Activity simulator stopped

:end
pause

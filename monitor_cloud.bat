@echo off
REM Cloud monitoring service startup

cd /d "%~dp0"

REM Start with 2 minute delay then detach
start /B cmd /c "timeout /t 120 /nobreak >nul && start /B pythonw monitor_scheduler.py --test"

exit

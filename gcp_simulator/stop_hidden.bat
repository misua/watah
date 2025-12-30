@echo off
REM Stop the hidden activity simulator

REM Kill pythonw processes running stealth_runner
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Adobe Update Service*" 2>nul
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Windows Update*" 2>nul
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Microsoft Edge*" 2>nul

REM Fallback - kill by script name (less stealthy)
wmic process where "commandline like '%%stealth_runner%%'" delete 2>nul

REM Clean up pid file
if exist .runtime.pid del .runtime.pid
if exist activity_sim.pid del activity_sim.pid
if exist syslog.tmp del syslog.tmp

echo Service stopped
timeout /t 2 /nobreak >nul

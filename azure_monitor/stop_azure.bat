@echo off
REM Stop Azure Portal Configuration Service

REM Kill the pythonw process running azure_setup.py
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq azure_setup.py" >nul 2>&1

REM Remove PID file
if exist ".azconfig.pid" (
    del .azconfig.pid
)

echo Azure portal helper stopped
timeout /t 1 /nobreak >nul

@echo off
cd /d "%~dp0"

if exist "..\venv\Scripts\pythonw.exe" (
    start "" /B "..\venv\Scripts\pythonw.exe" gcp_monitoring.py
) else (
    start "" /B pythonw gcp_monitoring.py
)

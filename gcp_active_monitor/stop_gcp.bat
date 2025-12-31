@echo off
cd /d "%~dp0"
taskkill /F /IM pythonw.exe 2>nul
del activity_sim.pid 2>nul

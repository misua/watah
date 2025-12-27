@echo off
REM View activity simulator logs

echo === Activity Simulator Log Viewer ===
echo.

if exist activity_sim_stealth.log (
    echo Viewing stealth mode logs...
    echo Press Ctrl+C to stop watching
    echo.
    powershell -Command "Get-Content activity_sim_stealth.log -Wait -Tail 50"
) else if exist activity_sim.log (
    echo Viewing normal mode logs...
    echo Press Ctrl+C to stop watching
    echo.
    powershell -Command "Get-Content activity_sim.log -Wait -Tail 50"
) else (
    echo No log files found!
    echo Make sure the activity simulator is running.
)

pause

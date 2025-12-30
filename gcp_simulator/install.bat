@echo off
echo ========================================
echo Activity Simulator - Windows Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo Installing Activity Simulator...
echo.

REM Install the package
pip install -e .
if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    echo Try running this script as Administrator
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Initialize configuration: activity-sim init-config
echo 2. Test input injection: activity-sim test
echo 3. Start simulator: activity-sim start
echo.
echo For detailed instructions, see INSTALL.md
echo.
pause

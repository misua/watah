@echo off
REM Windows setup script for activity simulator
echo ========================================
echo Activity Simulator - Windows Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Step 1: Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies...
pip install pywin32>=306 pynput>=1.7.6 numpy>=1.24.0 scipy>=1.10.0 PyYAML>=6.0 click>=8.1.0 psutil>=5.9.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 5: Installing activity_simulator package...
pip install -e .
if %errorlevel% neq 0 (
    echo WARNING: Failed to install package in editable mode
    echo This might be okay - dependencies are installed
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To activate the virtual environment in future sessions:
echo   venv\Scripts\activate.bat
echo.
echo To run the activity simulator:
echo   start.bat
echo.
pause

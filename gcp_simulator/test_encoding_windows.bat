@echo off
REM Test the encoding fix on Windows
echo ========================================
echo Testing Encoding Fix
echo ========================================

if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo Creating test script...
echo import sys > test_unicode.py
echo import logging >> test_unicode.py
echo import io >> test_unicode.py
echo. >> test_unicode.py
echo log_file = "test_encoding.log" >> test_unicode.py
echo log_level = "INFO" >> test_unicode.py
echo. >> test_unicode.py
echo file_handler = logging.FileHandler(log_file, encoding='utf-8'^) >> test_unicode.py
echo. >> test_unicode.py
echo try: >> test_unicode.py
echo     stdout_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True^) >> test_unicode.py
echo     stream_handler = logging.StreamHandler(stdout_stream^) >> test_unicode.py
echo except (AttributeError, io.UnsupportedOperation^): >> test_unicode.py
echo     stream_handler = logging.StreamHandler(sys.stdout^) >> test_unicode.py
echo. >> test_unicode.py
echo formatter = logging.Formatter("%%^(asctime^)s - %%^(name^)s - %%^(levelname^)s - %%^(message^)s"^) >> test_unicode.py
echo file_handler.setFormatter(formatter^) >> test_unicode.py
echo stream_handler.setFormatter(formatter^) >> test_unicode.py
echo. >> test_unicode.py
echo logging.basicConfig(level=getattr(logging, log_level^), handlers=[file_handler, stream_handler]^) >> test_unicode.py
echo. >> test_unicode.py
echo logger = logging.getLogger("test"^) >> test_unicode.py
echo logger.info("^>^>^> Executing activity: mouse_movement"^) >> test_unicode.py
echo logger.info("✓ Activity completed successfully"^) >> test_unicode.py
echo logger.error("✗ Activity FAILED"^) >> test_unicode.py
echo. >> test_unicode.py
echo print("\\nTest completed! Check test_encoding.log for results."^) >> test_unicode.py

echo.
echo Running test...
python test_unicode.py

echo.
echo Cleaning up...
del test_unicode.py 2>nul

echo.
pause

@echo off
REM Email Auto-Check Service - Windows Startup Script

echo ========================================
echo Email Auto-Check Service
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install required packages
echo Installing dependencies...
pip install -q aiohttp python-dotenv

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo [OK] Starting Email Auto-Check Service
echo.
echo This service will check emails every 5 minutes
echo Press Ctrl+C to stop
echo.

REM Start the service
python email_autocheck.py

pause

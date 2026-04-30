@echo off
REM Customer Success FTE - Windows Startup Script

echo ==================================
echo Customer Success FTE - Starting...
echo ==================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create .env file with your credentials
    pause
    exit /b 1
)

REM Install dependencies
echo Checking dependencies...
pip install -q fastapi uvicorn python-dotenv openai twilio google-auth google-auth-oauthlib google-api-python-client 2>nul

REM Create necessary directories
if not exist "credentials" mkdir credentials
if not exist "logs" mkdir logs
if not exist "data" mkdir data

echo.
echo [OK] Environment ready
echo.
echo Starting API server...
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn production.api.main:app --reload --host 0.0.0.0 --port 8000

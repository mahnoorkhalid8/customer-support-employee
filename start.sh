#!/bin/bash
# Customer Success FTE - Startup Script

echo "=================================="
echo "Customer Success FTE - Starting..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with your credentials"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q fastapi uvicorn python-dotenv openai twilio google-auth google-auth-oauthlib google-api-python-client 2>/dev/null

# Create necessary directories
mkdir -p credentials logs data

echo ""
echo "✓ Environment ready"
echo ""
echo "Starting API server..."
echo "API Docs: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""

# Start the server
uvicorn production.api.main:app --reload --host 0.0.0.0 --port 8000

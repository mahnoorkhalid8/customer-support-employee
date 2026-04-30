#!/bin/bash
# Email Auto-Check Service - Linux/Mac Startup Script

echo "========================================"
echo "Email Auto-Check Service"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing dependencies..."
pip install -q aiohttp python-dotenv

# Create logs directory
mkdir -p logs

echo ""
echo "[OK] Starting Email Auto-Check Service"
echo ""
echo "This service will check emails every 5 minutes"
echo "Press Ctrl+C to stop"
echo ""

# Start the service
python email_autocheck.py

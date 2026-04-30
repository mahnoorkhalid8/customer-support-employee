#!/usr/bin/env python3
"""
Setup script for Customer Success FTE project.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_python_version():
    """Check if Python version is 3.10+."""
    print_header("Checking Python Version")

    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def check_env_file():
    """Check if .env file exists."""
    print_header("Checking Environment File")

    if not Path(".env").exists():
        print("❌ .env file not found")
        print("   Please create .env file with your credentials")
        sys.exit(1)

    print("✅ .env file found")


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Python Dependencies")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def check_docker():
    """Check if Docker is installed."""
    print_header("Checking Docker")

    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            capture_output=True
        )
        print("✅ Docker is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker not found (optional for local development)")


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")

    directories = [
        "logs",
        "credentials",
        "data"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete!")

    print("""
Next Steps:

1. Configure your .env file with actual credentials:
   - OPENAI_API_KEY
   - Database credentials (POSTGRES_*)
   - Gmail API credentials (GMAIL_*)
   - Twilio credentials (TWILIO_*)

2. Start the database:
   docker-compose up -d postgres

3. Run database migrations:
   psql -d fte_db -f production/database/schema.sql

4. Start the services:

   # Option A: Using Docker Compose (recommended)
   docker-compose up

   # Option B: Manual start
   # Terminal 1: Start API
   uvicorn production.api.main:app --reload --port 8000

   # Terminal 2: Start worker (when implemented)
   python production/workers/message_processor.py

5. Access the API:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

6. Start building:
   - Implement channel handlers in production/channels/
   - Implement agent tools in production/agent/tools.py
   - Implement message processor in production/workers/

For detailed instructions, see README.md
""")


def main():
    """Main setup function."""
    print("\n🚀 Customer Success FTE - Setup Script\n")

    check_python_version()
    check_env_file()
    install_dependencies()
    check_docker()
    create_directories()
    print_next_steps()


if __name__ == "__main__":
    main()

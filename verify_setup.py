#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script to test the Customer Success FTE setup.
"""

import asyncio
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from production.api.main import app
        print("✅ API module imported")

        from production.database.queries import init_db_pool
        print("✅ Database module imported")

        from production.kafka_client import FTEKafkaProducer
        print("✅ Kafka client imported")

        from production.agent.tools import TOOL_FUNCTIONS
        print("✅ Agent tools imported")

        from production.agent.formatters import format_for_channel
        print("✅ Agent formatters imported")

        from production.channels.web_form_handler import router
        print("✅ Web form handler imported")

        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


async def test_env_file():
    """Test that .env file exists and has required variables."""
    print("\nTesting environment configuration...")

    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False

    print("✅ .env file exists")

    # Check for critical variables
    required_vars = [
        "OPENAI_API_KEY",
        "POSTGRES_PASSWORD",
        "DATABASE_URL"
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("   (This is expected if you haven't updated .env yet)")
    else:
        print("✅ All critical environment variables set")

    return True


async def test_directory_structure():
    """Test that all required directories exist."""
    print("\nTesting directory structure...")

    required_dirs = [
        "production/agent",
        "production/channels",
        "production/workers",
        "production/api",
        "production/database",
        "context",
        "tests",
        "k8s",
        "logs",
        "credentials",
        "data"
    ]

    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ missing")
            all_exist = False

    return all_exist


async def test_context_files():
    """Test that context files exist."""
    print("\nTesting context files...")

    context_files = [
        "context/company-profile.md",
        "context/product-docs.md",
        "context/sample-tickets.json",
        "context/escalation-rules.md",
        "context/brand-voice.md"
    ]

    all_exist = True
    for file in context_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_exist = False

    return all_exist


async def main():
    """Run all verification tests."""
    print("=" * 70)
    print("  Customer Success FTE - Setup Verification")
    print("=" * 70)

    results = []

    results.append(await test_imports())
    results.append(await test_env_file())
    results.append(await test_directory_structure())
    results.append(await test_context_files())

    print("\n" + "=" * 70)
    if all(results):
        print("✅ All verification tests passed!")
        print("\nNext steps:")
        print("1. Update .env file with your actual credentials")
        print("2. Run: docker-compose up -d")
        print("3. Run: python setup.py")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("⚠️  Some verification tests failed")
        print("Please review the errors above and fix them")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

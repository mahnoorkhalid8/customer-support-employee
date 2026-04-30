"""
System Verification Script
Tests all components are properly integrated
"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test all imports work"""
    print("Testing imports...")
    try:
        from production.grok_client import get_grok_client
        from production.ai.customer_support import CustomerSupportAI
        from production.integrations.gmail.gmail_client import GmailClient
        from production.integrations.whatsapp.whatsapp_client import WhatsAppClient
        from production.api.routes.gmail_routes import router as gmail_router
        from production.api.routes.whatsapp_routes import router as whatsapp_router

        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_grok_client():
    """Test Grok client initialization"""
    print("\nTesting Grok client...")
    try:
        from production.grok_client import get_grok_client
        client = get_grok_client()
        print("✓ Grok client initialized")
        return True
    except Exception as e:
        print(f"✗ Grok client error: {e}")
        return False

def test_ai_service():
    """Test AI service initialization"""
    print("\nTesting AI service...")
    try:
        from production.ai.customer_support import CustomerSupportAI
        ai = CustomerSupportAI()
        print("✓ AI service initialized")
        return True
    except Exception as e:
        print(f"✗ AI service error: {e}")
        return False

def test_gmail_client():
    """Test Gmail client initialization"""
    print("\nTesting Gmail client...")
    try:
        from production.integrations.gmail.gmail_client import GmailClient
        client = GmailClient()
        print("✓ Gmail client initialized")
        return True
    except Exception as e:
        print(f"✗ Gmail client error: {e}")
        return False

def test_whatsapp_client():
    """Test WhatsApp client initialization"""
    print("\nTesting WhatsApp client...")
    try:
        # Check if credentials exist
        if not os.getenv("TWILIO_ACCOUNT_SID"):
            print("⚠ WhatsApp credentials not configured (optional)")
            return True

        from production.integrations.whatsapp.whatsapp_client import WhatsAppClient
        client = WhatsAppClient()
        print("✓ WhatsApp client initialized")
        return True
    except Exception as e:
        print(f"✗ WhatsApp client error: {e}")
        return False

def test_api_routes():
    """Test API routes are registered"""
    print("\nTesting API routes...")
    try:
        from production.api.main import app

        routes = [route.path for route in app.routes]

        required_routes = [
            "/gmail/webhook",
            "/gmail/check-emails",
            "/gmail/send",
            "/gmail/status",
            "/whatsapp/webhook",
            "/whatsapp/send",
            "/whatsapp/status",
            "/health"
        ]

        missing = []
        for route in required_routes:
            if route not in routes:
                missing.append(route)

        if missing:
            print(f"✗ Missing routes: {missing}")
            return False

        print(f"✓ All {len(required_routes)} routes registered")
        return True
    except Exception as e:
        print(f"✗ API routes error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\nTesting environment...")

    required = ["GROK_API_KEY"]
    optional = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]

    missing_required = []
    for var in required:
        if not os.getenv(var):
            missing_required.append(var)

    if missing_required:
        print(f"✗ Missing required: {missing_required}")
        return False

    missing_optional = []
    for var in optional:
        if not os.getenv(var):
            missing_optional.append(var)

    if missing_optional:
        print(f"⚠ Missing optional: {missing_optional}")

    print("✓ Required environment variables configured")
    return True

def test_file_structure():
    """Test required files exist"""
    print("\nTesting file structure...")

    required_files = [
        "production/grok_client.py",
        "production/ai/customer_support.py",
        "production/integrations/gmail/gmail_client.py",
        "production/integrations/whatsapp/whatsapp_client.py",
        "production/api/routes/gmail_routes.py",
        "production/api/routes/whatsapp_routes.py",
        "production/api/main.py",
        ".env",
        "SETUP.md",
        "QUICKSTART.md"
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print(f"✗ Missing files: {missing}")
        return False

    print(f"✓ All {len(required_files)} required files present")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("System Verification")
    print("=" * 60)

    tests = [
        ("Environment", test_environment),
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Grok Client", test_grok_client),
        ("AI Service", test_ai_service),
        ("Gmail Client", test_gmail_client),
        ("WhatsApp Client", test_whatsapp_client),
        ("API Routes", test_api_routes)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\n✅ System verification complete - All components ready!")
        print("\nNext steps:")
        print("1. Run: python tests/test_grok.py")
        print("2. Run: uvicorn production.api.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\n⚠ Some components need attention - check errors above")

    sys.exit(0 if passed_count == total_count else 1)

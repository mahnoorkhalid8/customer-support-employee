"""
Test script for Gmail and WhatsApp integrations.
Run this to verify your credentials and test the handlers.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Windows console compatibility - use ASCII characters
OK = "[OK]"
FAIL = "[FAIL]"
WARN = "[WARN]"

def test_gmail():
    """Test Gmail integration."""
    print("\n" + "="*60)
    print("TESTING GMAIL INTEGRATION")
    print("="*60)

    try:
        from production.channels.gmail_handler import GmailHandler

        # Check credentials
        gmail_enabled = os.getenv('GMAIL_ENABLED', 'false').lower() == 'true'
        client_id = os.getenv('GMAIL_CLIENT_ID')

        print(f"{OK} Gmail enabled: {gmail_enabled}")
        print(f"{OK} Client ID configured: {bool(client_id)}")

        if not gmail_enabled:
            print(f"{WARN} Gmail is disabled in .env (GMAIL_ENABLED=false)")
            return False

        if not client_id or client_id == 'your-client-id.apps.googleusercontent.com':
            print(f"{WARN} Gmail credentials not configured in .env")
            print("  Please set GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN")
            return False

        # Try to initialize handler
        handler = GmailHandler()
        print(f"{OK} GmailHandler initialized successfully")

        return True

    except ImportError as e:
        print(f"{FAIL} Import error: {e}")
        print("  Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        return False
    except Exception as e:
        print(f"{FAIL} Error: {e}")
        return False


def test_whatsapp():
    """Test WhatsApp integration."""
    print("\n" + "="*60)
    print("TESTING WHATSAPP INTEGRATION")
    print("="*60)

    try:
        from production.channels.whatsapp_handler import WhatsAppHandler

        # Check credentials
        whatsapp_enabled = os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true'
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

        print(f"{OK} WhatsApp enabled: {whatsapp_enabled}")
        print(f"{OK} Account SID configured: {bool(account_sid)}")
        print(f"{OK} Auth token configured: {bool(auth_token)}")
        print(f"{OK} WhatsApp number configured: {bool(whatsapp_number)}")

        if not whatsapp_enabled:
            print(f"{WARN} WhatsApp is disabled in .env (WHATSAPP_ENABLED=false)")
            return False

        if not all([account_sid, auth_token, whatsapp_number]):
            print(f"{WARN} Twilio credentials not configured in .env")
            print("  Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER")
            return False

        if account_sid.startswith('ACxxxxxxxx'):
            print(f"{WARN} Using dummy Twilio credentials")
            print("  Replace with real credentials from https://console.twilio.com")
            return False

        # Try to initialize handler
        handler = WhatsAppHandler()
        print(f"{OK} WhatsAppHandler initialized successfully")
        print(f"{OK} Using WhatsApp number: {handler.whatsapp_number}")

        return True

    except ImportError as e:
        print(f"{FAIL} Import error: {e}")
        print("  Run: pip install twilio")
        return False
    except Exception as e:
        print(f"{FAIL} Error: {e}")
        return False


def test_grok():
    """Test Grok API configuration."""
    print("\n" + "="*60)
    print("TESTING GROK API CONFIGURATION")
    print("="*60)

    try:
        from production.grok_client import get_grok_client

        api_key = os.getenv('GROK_API_KEY')
        model = os.getenv('GROK_MODEL', 'grok-beta')
        base_url = os.getenv('GROK_BASE_URL', 'https://api.x.ai/v1')

        print(f"{OK} API key configured: {bool(api_key)}")
        print(f"{OK} Model: {model}")
        print(f"{OK} Base URL: {base_url}")

        if not api_key or api_key == 'your_grok_api_key_here':
            print(f"{WARN} Grok API key not configured")
            else:
                print(f"{WARN} Grok API key not configured")
                return False

        # Try to initialize client
        client = get_grok_client()
        print(f"{OK} Grok client initialized successfully")

        return True

    except ImportError as e:
        print(f"{FAIL} Import error: {e}")
        print("  Run: pip install openai")
        return False
    except Exception as e:
        print(f"{FAIL} Error: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CUSTOMER SUCCESS FTE - INTEGRATION TEST")
    print("="*60)

    results = {
        'Grok API': test_grok(),
        'Gmail': test_gmail(),
        'WhatsApp': test_whatsapp()
    }

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, passed in results.items():
        status = f"{OK} PASS" if passed else f"{FAIL} FAIL"
        print(f"{name:20} {status}")

    all_passed = all(results.values())

    if all_passed:
        print(f"\n{OK} All integrations configured correctly!")
        print("\nNext steps:")
        print("1. Start the API server: uvicorn production.api.main:app --reload")
        print("2. Test webhooks with ngrok: ngrok http 8000")
        print("3. Configure webhook URLs in Twilio/Gmail consoles")
    else:
        print(f"\n{WARN} Some integrations need configuration")
        print("Update credentials in .env file and run this test again")

    sys.exit(0 if all_passed else 1)

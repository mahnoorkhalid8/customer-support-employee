"""
Test WhatsApp Integration
Run this to verify Twilio WhatsApp setup is working
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.integrations.whatsapp.whatsapp_client import WhatsAppClient

def test_credentials():
    """Test if Twilio credentials are configured"""
    print("Testing Twilio credentials...")

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    if not account_sid:
        print("✗ TWILIO_ACCOUNT_SID not found in .env")
        return False
    if not auth_token:
        print("✗ TWILIO_AUTH_TOKEN not found in .env")
        return False
    if not whatsapp_number:
        print("✗ TWILIO_WHATSAPP_NUMBER not found in .env")
        return False

    print(f"✓ Account SID: {account_sid[:10]}...")
    print(f"✓ Auth Token: {auth_token[:10]}...")
    print(f"✓ WhatsApp Number: {whatsapp_number}")

    return True

def test_client_initialization():
    """Test WhatsApp client initialization"""
    print("\nTesting WhatsApp client initialization...")
    try:
        client = WhatsAppClient()
        print("✓ WhatsApp client initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
        return False

def test_send_message():
    """Test sending WhatsApp message"""
    print("\nTesting WhatsApp message sending...")

    to_number = input("Enter test phone number (format: +1234567890, or press Enter to skip): ").strip()
    if not to_number:
        print("Skipped message sending test")
        return True

    try:
        client = WhatsAppClient()

        result = client.send_message(
            to=to_number,
            body="🤖 Test message from Customer Success FTE!\n\nThis is a test to verify WhatsApp integration is working."
        )

        if result['success']:
            print(f"✓ Message sent successfully!")
            print(f"  Message SID: {result['message_sid']}")
            print(f"  Status: {result['status']}")
            return True
        else:
            print(f"✗ Failed to send message: {result.get('error')}")
            return False

    except Exception as e:
        print(f"✗ Error sending message: {e}")
        return False

def test_parse_incoming():
    """Test parsing incoming webhook data"""
    print("\nTesting webhook data parsing...")

    try:
        client = WhatsAppClient()

        # Simulate Twilio webhook data
        test_data = {
            'MessageSid': 'SM1234567890',
            'From': 'whatsapp:+1234567890',
            'To': 'whatsapp:+14155238886',
            'Body': 'Hello, I need help!',
            'NumMedia': '0',
            'ProfileName': 'Test User',
            'Timestamp': '2024-01-01T12:00:00Z'
        }

        parsed = client.parse_incoming_message(test_data)

        print("✓ Webhook data parsed successfully:")
        print(f"  From: {parsed['from']}")
        print(f"  Body: {parsed['body']}")
        print(f"  Profile Name: {parsed['profile_name']}")

        return True

    except Exception as e:
        print(f"✗ Error parsing webhook data: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("WhatsApp Integration Test")
    print("=" * 60)

    # Check .env file exists
    if not os.path.exists(".env"):
        print("\n✗ .env file not found!")
        print("\nPlease create .env file with:")
        print("  TWILIO_ACCOUNT_SID=your_account_sid")
        print("  TWILIO_AUTH_TOKEN=your_auth_token")
        print("  TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886")
        sys.exit(1)

    print("\n✓ .env file found")

    # Run tests
    results = []
    results.append(("Credentials Check", test_credentials()))
    results.append(("Client Initialization", test_client_initialization()))
    results.append(("Parse Incoming Data", test_parse_incoming()))
    results.append(("Send Message", test_send_message()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n✓ All tests passed! WhatsApp integration is ready.")
        print("\nNext steps:")
        print("1. Set up ngrok: ngrok http 8000")
        print("2. Configure Twilio webhook with ngrok URL")
        print("3. Send a message to your Twilio WhatsApp number")
    else:
        print("\n✗ Some tests failed. Check the errors above.")

    sys.exit(0 if all_passed else 1)

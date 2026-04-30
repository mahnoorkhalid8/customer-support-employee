"""
Test Gmail Integration
Run this to verify Gmail setup is working
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.integrations.gmail.gmail_client import GmailClient

def test_gmail_authentication():
    """Test Gmail OAuth authentication"""
    print("Testing Gmail authentication...")
    try:
        client = GmailClient()
        success = client.authenticate()
        if success:
            print("✓ Gmail authentication successful!")
            return True
        else:
            print("✗ Gmail authentication failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_read_emails():
    """Test reading unread emails"""
    print("\nTesting email reading...")
    try:
        client = GmailClient()
        client.authenticate()
        messages = client.get_unread_messages(max_results=5)

        print(f"✓ Found {len(messages)} unread emails")

        for i, msg in enumerate(messages[:3], 1):
            print(f"\n  Email {i}:")
            print(f"    From: {msg['from']}")
            print(f"    Subject: {msg['subject']}")
            print(f"    Snippet: {msg['snippet'][:100]}...")

        return True
    except Exception as e:
        print(f"✗ Error reading emails: {e}")
        return False

def test_send_email():
    """Test sending email"""
    print("\nTesting email sending...")

    to_email = input("Enter test email address (or press Enter to skip): ").strip()
    if not to_email:
        print("Skipped email sending test")
        return True

    try:
        client = GmailClient()
        client.authenticate()

        success = client.send_reply(
            to=to_email,
            subject="Test Email from Customer Success FTE",
            body="This is a test email to verify the Gmail integration is working correctly."
        )

        if success:
            print(f"✓ Test email sent to {to_email}")
            return True
        else:
            print("✗ Failed to send email")
            return False
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Gmail Integration Test")
    print("=" * 60)

    # Check credentials file exists
    creds_path = "credentials/gmail_credentials.json"
    if not os.path.exists(creds_path):
        print(f"\n✗ Credentials file not found: {creds_path}")
        print("\nPlease follow these steps:")
        print("1. Go to Google Cloud Console")
        print("2. Enable Gmail API")
        print("3. Create OAuth2 credentials (Desktop app)")
        print("4. Download JSON and save as credentials/gmail_credentials.json")
        sys.exit(1)

    print(f"\n✓ Credentials file found: {creds_path}")

    # Run tests
    results = []
    results.append(("Authentication", test_gmail_authentication()))
    results.append(("Read Emails", test_read_emails()))
    results.append(("Send Email", test_send_email()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n✓ All tests passed! Gmail integration is ready.")
    else:
        print("\n✗ Some tests failed. Check the errors above.")

    sys.exit(0 if all_passed else 1)

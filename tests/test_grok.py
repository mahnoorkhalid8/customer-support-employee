"""
Test Grok AI Integration
Run this to verify Grok API is working
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from production.grok_client import get_grok_client, get_model_name
from production.ai.customer_support import CustomerSupportAI

def test_credentials():
    """Test if Grok API credentials are configured"""
    print("Testing Grok API credentials...")

    api_key = os.getenv("GROK_API_KEY")
    base_url = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
    model = os.getenv("GROK_MODEL", "grok-beta")

    if not api_key:
        print("✗ GROK_API_KEY not found in .env")
        return False

    print(f"✓ API Key: {api_key[:10]}...")
    print(f"✓ Base URL: {base_url}")
    print(f"✓ Model: {model}")

    return True

def test_client_initialization():
    """Test Grok client initialization"""
    print("\nTesting Grok client initialization...")
    try:
        client = get_grok_client()
        print("✓ Grok client initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error initializing client: {e}")
        return False

def test_basic_completion():
    """Test basic chat completion"""
    print("\nTesting basic chat completion...")
    try:
        client = get_grok_client()
        model = get_model_name()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, I am working!' in exactly those words."}
            ],
            max_tokens=50
        )

        reply = response.choices[0].message.content
        print(f"✓ Received response from Grok:")
        print(f"  {reply}")

        return True

    except Exception as e:
        print(f"✗ Error getting completion: {e}")
        return False

def test_customer_support_ai():
    """Test Customer Support AI service"""
    print("\nTesting Customer Support AI service...")
    try:
        ai = CustomerSupportAI()

        # Test email response
        print("\n  Testing email response generation...")
        email_response = ai.generate_email_response(
            subject="Password Reset Request",
            body="Hi, I forgot my password and need help resetting it.",
            sender="customer@example.com",
            sender_name="John Doe"
        )

        print(f"  ✓ Email response generated:")
        print(f"    Subject: {email_response['subject']}")
        print(f"    Body preview: {email_response['body'][:100]}...")

        # Test WhatsApp response
        print("\n  Testing WhatsApp response generation...")
        whatsapp_response = ai.generate_whatsapp_response(
            message="How do I track my order?",
            sender="+1234567890",
            sender_name="Jane"
        )

        print(f"  ✓ WhatsApp response generated:")
        print(f"    {whatsapp_response[:100]}...")

        return True

    except Exception as e:
        print(f"✗ Error in Customer Support AI: {e}")
        return False

def test_conversation_context():
    """Test AI with conversation history"""
    print("\nTesting conversation with context...")
    try:
        ai = CustomerSupportAI()

        conversation_history = [
            {"role": "user", "content": "I need help with my order"},
            {"role": "assistant", "content": "I'd be happy to help! Could you provide your order number?"},
            {"role": "user", "content": "It's ORDER-12345"}
        ]

        response = ai.generate_response(
            customer_message="When will it arrive?",
            channel="email",
            conversation_history=conversation_history
        )

        print(f"✓ Response with context generated:")
        print(f"  {response[:150]}...")

        return True

    except Exception as e:
        print(f"✗ Error with conversation context: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Grok AI Integration Test")
    print("=" * 60)

    # Check .env file exists
    if not os.path.exists(".env"):
        print("\n✗ .env file not found!")
        print("\nPlease create .env file with:")
        print("  GROK_API_KEY=your_grok_api_key")
        print("  GROK_MODEL=grok-beta")
        print("  GROK_BASE_URL=https://api.x.ai/v1")
        sys.exit(1)

    print("\n✓ .env file found")

    # Run tests
    results = []
    results.append(("Credentials Check", test_credentials()))
    results.append(("Client Initialization", test_client_initialization()))
    results.append(("Basic Completion", test_basic_completion()))
    results.append(("Customer Support AI", test_customer_support_ai()))
    results.append(("Conversation Context", test_conversation_context()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n✓ All tests passed! Grok AI integration is ready.")
        print("\nYour Grok API is working correctly and can:")
        print("  - Generate customer support responses")
        print("  - Handle email and WhatsApp formats")
        print("  - Maintain conversation context")
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        print("\nCommon issues:")
        print("  - Invalid API key")
        print("  - Network connectivity")
        print("  - API rate limits")

    sys.exit(0 if all_passed else 1)

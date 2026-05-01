"""
Setup Gmail credentials from environment variables
Used for deployment environments like Hugging Face Spaces
"""
import os
import json

def setup_gmail_credentials():
    """
    Create gmail_credentials.json from environment variable
    This allows storing the JSON file content as a secret in HF Spaces
    """
    credentials_json = os.getenv("GMAIL_CREDENTIALS_JSON")

    if not credentials_json:
        print("GMAIL_CREDENTIALS_JSON not found in environment")
        return False

    try:
        # Create credentials directory if it doesn't exist
        os.makedirs("credentials", exist_ok=True)

        # Parse JSON to validate it
        credentials_data = json.loads(credentials_json)

        # Write to file
        credentials_path = "credentials/gmail_credentials.json"
        with open(credentials_path, 'w') as f:
            json.dump(credentials_data, f, indent=2)

        print(f"✓ Gmail credentials file created at {credentials_path}")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in GMAIL_CREDENTIALS_JSON: {e}")
        return False
    except Exception as e:
        print(f"✗ Error setting up Gmail credentials: {e}")
        return False


def setup_gmail_token():
    """
    Create gmail_token.pickle from environment variable if available
    This allows pre-authenticated token to be stored as base64 in secrets
    """
    token_base64 = os.getenv("GMAIL_TOKEN_PICKLE_BASE64")

    if not token_base64:
        print("GMAIL_TOKEN_PICKLE_BASE64 not found (optional)")
        return False

    try:
        import base64

        # Create credentials directory if it doesn't exist
        os.makedirs("credentials", exist_ok=True)

        # Decode base64 and write to file
        token_data = base64.b64decode(token_base64)
        token_path = "credentials/gmail_token.pickle"

        with open(token_path, 'wb') as f:
            f.write(token_data)

        print(f"✓ Gmail token file created at {token_path}")
        return True

    except Exception as e:
        print(f"✗ Error setting up Gmail token: {e}")
        return False


if __name__ == "__main__":
    print("Setting up Gmail credentials...")
    setup_gmail_credentials()
    setup_gmail_token()

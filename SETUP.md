# Customer Success FTE - Setup Guide

## Overview
This guide will help you set up Gmail and WhatsApp integrations with Grok AI for automated customer support.

## Prerequisites
- Python 3.11+
- Gmail account with API access
- Twilio account with WhatsApp enabled
- Grok API key from xAI

---

## 1. Gmail Setup

### Step 1: Enable Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth2 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Download the JSON file
5. Save it as `credentials/gmail_credentials.json`

### Step 3: First-time Authentication
```bash
# Run the app - it will open a browser for OAuth consent
python -m uvicorn production.api.main:app --reload

# Or test Gmail directly
python -c "from production.integrations.gmail.gmail_client import GmailClient; client = GmailClient(); client.authenticate()"
```

This will:
- Open your browser for Google OAuth consent
- Save the token to `credentials/gmail_token.pickle`
- Future runs will use the saved token

---

## 2. WhatsApp (Twilio) Setup

### Step 1: Create Twilio Account
1. Sign up at [Twilio](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token from the dashboard

### Step 2: Enable WhatsApp Sandbox
1. In Twilio Console, go to "Messaging" > "Try it out" > "Send a WhatsApp message"
2. Follow instructions to join the sandbox (send a code to the Twilio number)
3. Note your WhatsApp sandbox number (format: `whatsapp:+14155238886`)

### Step 3: Configure Webhook
1. In Twilio Console, go to WhatsApp sandbox settings
2. Set "When a message comes in" webhook to:
   ```
   https://your-domain.com/whatsapp/webhook
   ```
3. For local testing, use [ngrok](https://ngrok.com/):
   ```bash
   ngrok http 8000
   # Use the ngrok URL: https://abc123.ngrok.io/whatsapp/webhook
   ```

---

## 3. Grok API Setup

### Get API Key
1. Sign up at [xAI](https://x.ai/)
2. Get your API key from the dashboard
3. Add to `.env` file

---

## 4. Environment Configuration

Create `.env` file in project root:

```bash
# Grok AI Configuration
GROK_API_KEY=gsk_your_actual_key_here
GROK_MODEL=grok-beta
GROK_BASE_URL=https://api.x.ai/v1

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Application Settings
PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG_MODE=true

# Feature Flags
GMAIL_ENABLED=true
WHATSAPP_ENABLED=true
WEBFORM_ENABLED=true

# CORS Settings
WEBFORM_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 5. Installation

### Option A: Local Installation (Recommended for Testing)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create credentials directory
mkdir credentials
```

### Option B: Docker Installation

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f api
```

---

## 6. Running the Application

### Start the API Server
```bash
# Development mode with auto-reload
uvicorn production.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn production.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the API
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Gmail Status: http://localhost:8000/gmail/status
- WhatsApp Status: http://localhost:8000/whatsapp/status

---

## 7. Testing the Integrations

### Test Gmail Integration

```bash
# Check for new emails and auto-respond
curl http://localhost:8000/gmail/check-emails

# Send test email
curl -X POST http://localhost:8000/gmail/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "body": "This is a test email from Customer Success FTE"
  }'
```

### Test WhatsApp Integration

```bash
# Send test WhatsApp message
curl -X POST http://localhost:8000/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Hello from Customer Success FTE!"
  }'

# Test webhook (simulate incoming message)
curl -X POST http://localhost:8000/whatsapp/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890&To=whatsapp:+14155238886&Body=Hello&MessageSid=test123&ProfileName=TestUser"
```

### Test Grok AI

```python
# Test AI response generation
from production.ai.customer_support import CustomerSupportAI

ai = CustomerSupportAI()
response = ai.generate_whatsapp_response(
    message="How do I reset my password?",
    sender="+1234567890",
    sender_name="John"
)
print(response)
```

---

## 8. Monitoring and Logs

### View Logs
```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api
```

### Check Status
```bash
# Health check
curl http://localhost:8000/health

# Gmail status
curl http://localhost:8000/gmail/status

# WhatsApp status
curl http://localhost:8000/whatsapp/status
```

---

## 9. Troubleshooting

### Gmail Issues

**Problem: "Invalid credentials"**
- Delete `credentials/gmail_token.pickle`
- Re-run authentication
- Ensure `gmail_credentials.json` is valid

**Problem: "Insufficient permissions"**
- Check OAuth scopes in Google Cloud Console
- Required scope: `https://www.googleapis.com/auth/gmail.modify`

### WhatsApp Issues

**Problem: "Authentication failed"**
- Verify Twilio Account SID and Auth Token
- Check environment variables are loaded

**Problem: "Webhook not receiving messages"**
- Verify ngrok is running (for local testing)
- Check Twilio webhook URL is correct
- Ensure webhook URL is publicly accessible

### Grok API Issues

**Problem: "API key invalid"**
- Verify GROK_API_KEY in `.env`
- Check API key is active on xAI dashboard

**Problem: "Rate limit exceeded"**
- Implement rate limiting in code
- Upgrade xAI plan if needed

---

## 10. Production Deployment

### Environment Variables
Set all environment variables in your hosting platform:
- Railway: Settings > Variables
- Render: Environment > Environment Variables
- Heroku: Settings > Config Vars

### Webhook URLs
Update Twilio webhook to production URL:
```
https://your-production-domain.com/whatsapp/webhook
```

### Gmail Pub/Sub (Optional)
For real-time Gmail notifications:
1. Set up Google Cloud Pub/Sub
2. Configure Gmail push notifications
3. Update webhook endpoint

---

## 11. Next Steps

1. **Test each integration separately** before combining
2. **Monitor logs** for errors during testing
3. **Set up proper error handling** for production
4. **Implement rate limiting** to avoid API limits
5. **Add conversation history** to database
6. **Set up monitoring** (Sentry, DataDog, etc.)

---

## Support

For issues or questions:
- Check logs first: `logs/app.log`
- Review API docs: http://localhost:8000/docs
- Test individual components before full integration

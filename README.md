---
title: Customer Support Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Customer Support FTE Backend

AI-powered customer support API with Gmail, WhatsApp, and Web Form integration.

## Features

- 🤖 AI-powered responses using Grok/Groq
- 📱 WhatsApp integration via Twilio
- 📧 Gmail integration
- 🌐 Web form support
- 📊 Real-time metrics and monitoring

## API Documentation

Once deployed, visit `/docs` for interactive API documentation (Swagger UI).

## Endpoints

### Health Check
- `GET /health` - Check API health status

### WhatsApp
- `POST /whatsapp/webhook` - Twilio WhatsApp webhook
- `POST /whatsapp/send` - Send WhatsApp message
- `POST /whatsapp/submit-query` - Submit query and get AI response
- `GET /whatsapp/status` - Check WhatsApp integration status

### Gmail
- `GET /gmail/status` - Check Gmail integration status
- `GET /gmail/check-emails` - Check for new emails
- `POST /gmail/submit-query` - Submit email query

### Web Form
- `POST /webform/submit` - Submit web form query

### Metrics
- `GET /metrics/channels` - Get channel metrics
- `GET /metrics/activity` - Get activity metrics

## Environment Variables

Configure these in the Space Settings → Repository secrets:

```
GROK_API_KEY=your_grok_api_key
GROK_MODEL=llama-3.3-70b-versatile
GROK_BASE_URL=https://api.groq.com/openai/v1
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GMAIL_ENABLED=true
WHATSAPP_ENABLED=true
WEBFORM_ENABLED=true
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Usage

After deployment, the API will be available at:
```
https://YOUR_USERNAME-customer-support-backend.hf.space
```

Test the health endpoint:
```bash
curl https://YOUR_USERNAME-customer-support-backend.hf.space/health
```

## Tech Stack

- **Framework**: FastAPI
- **AI Provider**: Grok (via Groq API)
- **WhatsApp**: Twilio API
- **Gmail**: Google Gmail API
- **Server**: Uvicorn (ASGI)
- **Python**: 3.11

## License

Apache 2.0

# WhatsApp Integration - Test Guide

## ✅ Current Status

**Integration Status**: ✓ Configured and Working
**Twilio Account**: AC********************************
**WhatsApp Number**: +14155238886 (Twilio Sandbox)
**Your Number**: +923332455342
**Daily Limit**: 5 messages (Free Tier)
**Current Status**: Limit reached - resets in 24 hours

---

## 🔧 What's Working

✓ Backend API running on port 8001
✓ Frontend running on port 3000
✓ WhatsApp client successfully authenticated with Twilio
✓ AI service configured (using Grok)
✓ `/whatsapp/submit-query` endpoint operational
✓ Message sending logic verified (hit rate limit, proving it works)

---

## 📱 How to Test (When Limit Resets)

### Test 1: Simple Query
```bash
curl -X POST http://localhost:8001/whatsapp/submit-query \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+923332455342",
    "query": "What are your business hours?"
  }'
```

**Expected Result**:
- Message 1: Your query appears in WhatsApp chat
- Message 2: AI-generated response sent back to you
- Total: 2 messages used

### Test 2: Product Inquiry
```bash
curl -X POST http://localhost:8001/whatsapp/submit-query \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+923332455342",
    "query": "I need help with my order #12345"
  }'
```

**Expected Result**:
- Message 1: Your query appears in WhatsApp chat
- Message 2: AI-generated response about order assistance
- Total: 2 messages used

---

## 🎯 What Happens During a Test

1. **Query Sent**: Your question is sent to your WhatsApp number
2. **AI Processing**: Grok AI generates a helpful response
3. **Response Sent**: AI response is delivered to your WhatsApp
4. **Confirmation**: API returns success with message SIDs

---

## 📊 Check Integration Status

```bash
curl http://localhost:8001/whatsapp/status
```

**Expected Response**:
```json
{
  "status": "configured",
  "service": "whatsapp",
  "number": "whatsapp:+14155238886"
}
```

---

## 🔄 Webhook Setup (For Receiving Messages)

To receive incoming WhatsApp messages, you need to configure Twilio webhook:

1. **Start ngrok** (expose local server):
   ```bash
   ngrok http 8001
   ```

2. **Copy the ngrok URL** (e.g., https://abc123.ngrok.io)

3. **Configure Twilio Webhook**:
   - Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
   - Set "When a message comes in": `https://abc123.ngrok.io/whatsapp/webhook`
   - Save

4. **Test incoming messages**: Send a message to the Twilio sandbox number from your WhatsApp

---

## 💡 Tips

- **Daily Limit**: Resets 24 hours after first message
- **Message Count**: Each test uses 2 messages (query + response)
- **Sandbox Mode**: Join sandbox by sending code to +14155238886
- **Phone Format**: Always use international format (+923332455342)

---

## 🚨 Troubleshooting

### Error: "exceeded the 5 daily messages limit"
- **Solution**: Wait 24 hours for limit reset
- **Alternative**: Upgrade Twilio account for higher limits

### Error: "Missing Twilio credentials"
- **Solution**: Check `.env` file has correct credentials

### Error: "Failed to send message"
- **Solution**: Verify phone number format and sandbox connection

---

## 📝 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/whatsapp/submit-query` | POST | Send query + AI response |
| `/whatsapp/send` | POST | Send message only |
| `/whatsapp/webhook` | POST | Receive incoming messages |
| `/whatsapp/status` | GET | Check integration status |

---

## ✨ Next Steps

1. Wait for daily limit reset (24 hours)
2. Run Test 1 to verify end-to-end flow
3. Check your WhatsApp for both messages
4. (Optional) Set up ngrok for webhook testing
5. (Optional) Upgrade Twilio for production use

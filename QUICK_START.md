# 🎯 Gmail FTE - Quick Start Guide

## ✅ System Status

**Backend**: http://localhost:8001 - ✓ Running
**Frontend**: http://localhost:3001 - ✓ Running
**Gmail API**: ✓ Connected
**Endpoint**: `/gmail/submit-query` - ✓ Active

---

## 🚀 How to Test Right Now

### Option 1: Test via API (Fastest)

Open a new terminal and run:

```bash
curl -X POST http://localhost:8001/gmail/submit-query \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "YOUR_EMAIL@gmail.com",
    "user_name": "Test User",
    "query": "Hi, I need help with my order #12345. Can you provide tracking information?"
  }'
```

**Replace `YOUR_EMAIL@gmail.com` with your actual email address.**

You should receive:
1. A JSON response with success message
2. An email in your inbox with AI-generated response

---

### Option 2: Test via Frontend

1. **Open browser**: http://localhost:3001

2. **Navigate to Gmail section** (click "Gmail" in the menu)

3. **If you see the old interface**, refresh the page (Ctrl+F5 or Cmd+Shift+R)

4. **Fill the form**:
   - Customer Email: your-email@example.com
   - Customer Name: John Doe
   - Customer Query: "I need help with my account"

5. **Click "Submit Query & Send AI Response"**

6. **Check your email** for the AI-generated response

---

## 📋 What Was Implemented

### Backend Changes ✓
- ✅ New endpoint: `POST /gmail/submit-query`
- ✅ Accepts: user_email, user_name, query
- ✅ Returns: success message + response preview
- ✅ Sends email via Gmail API

### Frontend Changes ✓
- ✅ New query submission form
- ✅ Three input fields (email, name, query)
- ✅ Submit button with loading state
- ✅ Success/error message display
- ✅ Response preview

### System Behavior ✓
- ✅ Does NOT read inbox emails
- ✅ Does NOT auto-process emails
- ✅ ONLY processes manually submitted queries
- ✅ Sends responses to specified email address

---

## 🧪 Test Scenarios

### Test 1: Basic Query
```json
{
  "user_email": "test@example.com",
  "user_name": "Test User",
  "query": "How do I reset my password?"
}
```

### Test 2: Order Tracking
```json
{
  "user_email": "customer@example.com",
  "user_name": "Jane Smith",
  "query": "I placed order #12345 yesterday but haven't received confirmation. Can you help?"
}
```

### Test 3: Account Issue
```json
{
  "user_email": "user@example.com",
  "query": "My account is locked and I can't log in. What should I do?"
}
```

---

## 📊 Expected Results

### Successful Response:
```json
{
  "status": "success",
  "message": "AI response sent to test@example.com",
  "response_preview": "Thank you for contacting us. I'd be happy to help..."
}
```

### What Happens:
1. ✅ Query is received by backend
2. ✅ Grok AI generates response
3. ✅ Email is sent via Gmail API
4. ✅ User receives email in inbox
5. ✅ Success message shown in dashboard

---

## 🔍 Verification Steps

### 1. Check Backend is Running
```bash
curl http://localhost:8001/health
```
Should return: `{"status":"healthy",...}`

### 2. Check Gmail Connection
```bash
curl http://localhost:8001/gmail/status
```
Should return: `{"status":"connected","service":"gmail"}`

### 3. Check API Documentation
Open: http://localhost:8001/docs
Look for: `/gmail/submit-query` endpoint

### 4. Check Frontend
Open: http://localhost:3001
Navigate to: Gmail section

---

## 🎯 Key Features

✅ **Manual Control**: Only processes queries you submit
✅ **AI-Powered**: Uses Grok AI for intelligent responses
✅ **Email Delivery**: Sends responses directly to customer's inbox
✅ **Real-time**: Processes and sends within seconds
✅ **Preview**: Shows response preview before sending
✅ **No Auto-Processing**: Won't touch your inbox emails

---

## 📝 Files Modified

### Backend
- `production/api/routes/gmail_routes.py` - Added submit-query endpoint
- `.env` - Fixed Grok model name

### Frontend
- `frontend/src/pages/Gmail.tsx` - New query form
- `frontend/src/services/api.ts` - Added submitQuery method

---

## 🆘 Troubleshooting

### Issue: "Not Found" error
**Solution**: Backend might not have reloaded. Check logs or restart backend.

### Issue: Frontend shows old interface
**Solution**: Hard refresh browser (Ctrl+F5) or clear cache.

### Issue: Email not received
**Solution**: 
1. Check Gmail status endpoint
2. Verify email address is correct
3. Check spam folder
4. Review backend logs for errors

### Issue: AI response is generic
**Solution**: This is the fallback response when Grok API fails. Check:
1. Grok API key is valid
2. Model name is correct (grok-beta)
3. Backend logs for API errors

---

## 🎉 Success Criteria

You'll know it's working when:
1. ✅ API returns success message
2. ✅ Response preview is shown
3. ✅ Email arrives in specified inbox
4. ✅ Email contains AI-generated response

---

## 📞 Quick Test Command

**Copy and paste this (replace email):**

```bash
curl -X POST http://localhost:8001/gmail/submit-query \
  -H "Content-Type: application/json" \
  -d '{"user_email":"YOUR_EMAIL@gmail.com","user_name":"Test","query":"Test query"}'
```

---

**Your Gmail FTE is ready! Test it now with the commands above.** 🚀

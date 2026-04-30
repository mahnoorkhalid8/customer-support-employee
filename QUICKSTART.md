# Customer Success FTE - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

This guide gets you up and running with Gmail and WhatsApp AI customer support.

---

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install fastapi uvicorn python-dotenv openai twilio google-auth google-auth-oauthlib google-api-python-client
```

---

## Step 2: Test Grok AI

```bash
python tests/test_grok.py
```

Expected: All tests pass ✓

---

## Step 3: Start API

```bash
uvicorn production.api.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 🎯 What Works Now

### Gmail Integration
- Auto-respond to emails with AI
- Read unread messages
- Send replies with context

### WhatsApp Integration  
- Receive messages via Twilio webhook
- Send AI-powered responses
- Handle conversations

### Grok AI
- Generate customer support responses
- Email and WhatsApp formats
- Conversation context

---

## 📚 Full Documentation

- **SETUP.md** - Detailed setup instructions
- **tests/** - Test each integration
- **/docs** - API documentation

Your AI customer support is ready!

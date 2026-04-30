# ngrok Setup Guide for WhatsApp Integration

## What is ngrok?

ngrok creates a secure tunnel from a public URL to your local server. This is **essential for local WhatsApp testing** because Twilio needs to send webhooks to your server, but your local machine isn't accessible from the internet.

---

## 📥 Installation

### Windows:
1. Download from: https://ngrok.com/download
2. Extract `ngrok.exe` to a folder (e.g., `C:\ngrok\`)
3. Add to PATH or run from the folder

### Mac/Linux:
```bash
# Using Homebrew (Mac)
brew install ngrok

# Or download directly
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin
```

---

## 🔑 Setup (One-time)

1. **Sign up** at https://dashboard.ngrok.com/signup
2. **Get your auth token** from https://dashboard.ngrok.com/get-started/your-authtoken
3. **Authenticate ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
   ```

---

## 🚀 Usage for WhatsApp Testing

### Step 1: Start Your API Server
```bash
# Make sure your API is running on port 8001
python -m uvicorn production.api.main:app --host 0.0.0.0 --port 8001 --reload
```

### Step 2: Start ngrok Tunnel
```bash
# In a new terminal
ngrok http 8001
```

You'll see output like:
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok.io -> http://localhost:8001
```

### Step 3: Copy the HTTPS URL
Copy the `https://abc123.ngrok.io` URL (yours will be different)

### Step 4: Configure Twilio Webhook

1. Go to https://console.twilio.com/
2. Navigate to: **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Find your WhatsApp Sandbox settings
4. Set **"When a message comes in"** to:
   ```
   https://abc123.ngrok.io/whatsapp/webhook
   ```
5. Method: **POST**
6. Click **Save**

### Step 5: Test It!

1. Send a WhatsApp message to your Twilio sandbox number
2. Watch the ngrok terminal - you'll see the incoming request
3. Your API will process it and send an AI response back!

---

## 🔍 Monitoring Requests

ngrok provides a web interface to inspect all requests:
- Open: http://localhost:4040
- See all incoming webhooks
- Replay requests for debugging
- View request/response details

---

## ⚠️ Important Notes

### Free Plan Limitations:
- URL changes every time you restart ngrok
- Must update Twilio webhook URL each time
- Session expires after 2 hours

### Paid Plan Benefits ($8/month):
- Fixed custom domain (e.g., `yourapp.ngrok.io`)
- No session timeouts
- No need to update webhook URL

---

## 🌐 Do You Need ngrok After Deployment?

### **NO** - ngrok is ONLY for local testing

Once you deploy to production:

### Option 1: Cloud Platform (Recommended)
Deploy to any cloud service with a public URL:
- **Railway**: https://railway.app (easiest)
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **AWS/GCP/Azure**: Full control

Your app will have a permanent URL like:
- `https://your-app.railway.app`
- `https://your-app.onrender.com`

### Option 2: Your Own Server
If you have a VPS or dedicated server:
- Get a domain name
- Set up SSL certificate (Let's Encrypt)
- Configure DNS
- Point Twilio webhook to: `https://yourdomain.com/whatsapp/webhook`

---

## 📋 Quick Reference

### Start Everything (Local Testing):

**Terminal 1 - API Server:**
```bash
cd hackathon-5
python -m uvicorn production.api.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - ngrok:**
```bash
ngrok http 8001
```

**Terminal 3 - Email Auto-Check (Optional):**
```bash
cd hackathon-5
python email_autocheck.py
```

**Browser:**
```
Open: frontend/index.html
```

---

## 🎯 Summary

| Environment | Need ngrok? | Webhook URL |
|-------------|-------------|-------------|
| **Local Testing** | ✅ YES | `https://abc123.ngrok.io/whatsapp/webhook` |
| **Production** | ❌ NO | `https://yourdomain.com/whatsapp/webhook` |

ngrok is a development tool - once deployed, your app has a real public URL and doesn't need ngrok anymore!

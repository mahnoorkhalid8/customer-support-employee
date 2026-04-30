# 🚀 Quick Deployment Guide

## Summary: Deploy in 15 Minutes

### 🔵 Step 1: Deploy Backend on Hugging Face (5 min)

1. **Create Space**: https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `customer-support-backend`
   - SDK: **Docker**
   - Click "Create Space"

2. **Clone and Push**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/customer-support-backend
   cd customer-support-backend
   
   # Copy backend files
   cp -r ../hackathon-5/production .
   cp ../hackathon-5/requirements.txt .
   cp ../hackathon-5/Dockerfile.hf Dockerfile
   
   # Create README.md (copy from README_DEPLOYMENT.md)
   
   git add .
   git commit -m "Deploy backend"
   git push
   ```

3. **Add Secrets** (in HF Space Settings → Repository secrets):
   ```
   GROK_API_KEY=your_grok_api_key_here
   GROK_MODEL=llama-3.3-70b-versatile
   GROK_BASE_URL=https://api.groq.com/openai/v1
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   GMAIL_ENABLED=true
   WHATSAPP_ENABLED=true
   WEBFORM_ENABLED=true
   ENVIRONMENT=production
   ```

4. **Get Your Backend URL**: 
   - `https://YOUR_USERNAME-customer-support-backend.hf.space`

---

### 🟢 Step 2: Deploy Frontend on Vercel (5 min)

1. **Import to Vercel**: https://vercel.com/new
   - Select your GitHub repo: `mahnoorkhalid8/customer-support-employee`
   - Click "Import"

2. **Configure Build**:
   - Framework: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Add Environment Variable**:
   ```
   VITE_API_URL=https://YOUR_USERNAME-customer-support-backend.hf.space
   ```
   (Replace YOUR_USERNAME with your HF username)

4. **Deploy**: Click "Deploy" and wait 1-2 minutes

5. **Get Your Frontend URL**: 
   - `https://your-project.vercel.app`

---

### 🔧 Step 3: Update CORS (2 min)

1. Go back to **Hugging Face Space Settings**
2. Add/Update secret:
   ```
   WEBFORM_CORS_ORIGINS=https://your-project.vercel.app
   ```
3. Restart the Space

---

### 📱 Step 4: Update Twilio Webhook (3 min)

1. Go to https://console.twilio.com
2. Navigate to: **Messaging** → **WhatsApp Sandbox Settings**
3. Update webhook URL:
   ```
   https://YOUR_USERNAME-customer-support-backend.hf.space/whatsapp/webhook
   ```
4. Save

---

## ✅ Test Your Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Check Dashboard - should show "Healthy" status
3. Try WhatsApp page (after quota resets)
4. Check API docs: `https://YOUR_HF_SPACE_URL/docs`

---

## 🔑 Credentials Summary

### What You Need:

**For Hugging Face (Backend):**
- Grok API Key (get from: https://console.groq.com)
- Twilio Account SID (get from: https://console.twilio.com)
- Twilio Auth Token (get from: https://console.twilio.com)
- WhatsApp Number (from Twilio Sandbox)

**For Vercel (Frontend):**
- ✅ Backend URL (from HF Space after deployment)

---

## 🐛 Common Issues

**Backend not starting?**
- Check HF Space logs tab
- Verify all secrets are added
- Make sure Dockerfile.hf is named exactly "Dockerfile"

**Frontend can't connect to backend?**
- Check VITE_API_URL is correct
- Verify CORS is configured with your Vercel URL
- Check browser console for errors

**WhatsApp not working?**
- Verify Twilio webhook URL is updated
- Check you have messages remaining in quota
- Ensure phone number is verified in Twilio sandbox

---

## 📞 Need Help?

Check the full guide: `README_DEPLOYMENT.md`

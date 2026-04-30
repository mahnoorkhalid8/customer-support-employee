# Deployment Guide

## 🚀 Deploy Backend on Hugging Face Spaces

### Prerequisites
- Hugging Face account (free): https://huggingface.co/join
- Git installed on your machine

### Step-by-Step Instructions

#### 1. Create a New Space on Hugging Face

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `customer-support-backend` (or your preferred name)
   - **License**: Apache 2.0
   - **Select SDK**: Choose **"Docker"**
   - **Space hardware**: Free CPU (or upgrade if needed)
4. Click **"Create Space"**

#### 2. Clone Your New Space Repository

```bash
# Clone the empty space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/customer-support-backend
cd customer-support-backend
```

#### 3. Copy Backend Files

Copy these files from your project to the space repository:

```bash
# Copy all backend files
cp -r production/ customer-support-backend/
cp requirements.txt customer-support-backend/
cp Dockerfile.hf customer-support-backend/Dockerfile
```

#### 4. Create README.md for the Space

Create a `README.md` in the space repository:

```markdown
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

## API Endpoints

- `GET /health` - Health check
- `POST /whatsapp/webhook` - WhatsApp webhook
- `POST /whatsapp/send` - Send WhatsApp message
- `POST /gmail/check` - Check Gmail inbox
- `POST /webform/submit` - Submit web form query

## Documentation

Visit `/docs` for interactive API documentation.
```

#### 5. Push to Hugging Face

```bash
cd customer-support-backend
git add .
git commit -m "Initial deployment"
git push
```

#### 6. Configure Environment Variables (Secrets)

Go to your Space settings on Hugging Face:

1. Click on **"Settings"** tab in your Space
2. Scroll to **"Repository secrets"**
3. Add the following secrets:

**Required Secrets:**

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

WEBFORM_CORS_ORIGINS=https://your-frontend.vercel.app,https://huggingface.co

ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Optional (if using Gmail):**
```
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
```

#### 7. Wait for Build

- Hugging Face will automatically build your Docker container
- Check the **"Logs"** tab to monitor the build process
- Once complete, your API will be available at: `https://YOUR_USERNAME-customer-support-backend.hf.space`

---

## 🌐 Deploy Frontend on Vercel

### Prerequisites
- Vercel account (free): https://vercel.com/signup
- GitHub account

### Step-by-Step Instructions

#### 1. Push Frontend to GitHub (if not already done)

Your frontend is already in the repository, so this step is complete.

#### 2. Import Project to Vercel

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select your GitHub repository: `mahnoorkhalid8/customer-support-employee`
4. Click **"Import"**

#### 3. Configure Build Settings

Vercel should auto-detect Vite, but verify these settings:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

#### 4. Add Environment Variables

In the Vercel project settings, add these environment variables:

**Required:**
```
VITE_API_URL=https://YOUR_USERNAME-customer-support-backend.hf.space
```

**Note:** Replace `YOUR_USERNAME` with your actual Hugging Face username.

#### 5. Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (usually 1-2 minutes)
3. Your frontend will be available at: `https://your-project.vercel.app`

#### 6. Update Backend CORS Settings

After deployment, update your Hugging Face Space secrets:

1. Go back to your Hugging Face Space settings
2. Update the `WEBFORM_CORS_ORIGINS` secret:
```
WEBFORM_CORS_ORIGINS=https://your-project.vercel.app
```

3. Restart your Space for changes to take effect

---

## 📋 Summary of Credentials Needed

### Hugging Face Spaces (Backend)

| Variable | Where to Get It | Required? |
|----------|----------------|-----------|
| `GROK_API_KEY` | https://console.groq.com | Yes |
| `TWILIO_ACCOUNT_SID` | https://console.twilio.com | Yes (for WhatsApp) |
| `TWILIO_AUTH_TOKEN` | https://console.twilio.com | Yes (for WhatsApp) |
| `TWILIO_WHATSAPP_NUMBER` | Twilio Console | Yes (for WhatsApp) |
| `GMAIL_CLIENT_ID` | Google Cloud Console | Optional (for Gmail) |
| `GMAIL_CLIENT_SECRET` | Google Cloud Console | Optional (for Gmail) |

### Vercel (Frontend)

| Variable | Value | Required? |
|----------|-------|-----------|
| `VITE_API_URL` | Your HF Space URL | Yes |

---

## 🔧 Post-Deployment Configuration

### Update Twilio Webhook URL

1. Go to https://console.twilio.com
2. Navigate to **Messaging** → **Settings** → **WhatsApp Sandbox**
3. Update the webhook URL to:
```
https://YOUR_USERNAME-customer-support-backend.hf.space/whatsapp/webhook
```

### Test Your Deployment

1. Visit your Vercel frontend URL
2. Navigate to the WhatsApp page
3. Send a test message (after your quota resets)
4. Check the API docs at: `https://YOUR_HF_SPACE_URL/docs`

---

## 🐛 Troubleshooting

### Backend Issues

- **Build fails**: Check logs in HF Space "Logs" tab
- **API not responding**: Verify all environment variables are set
- **CORS errors**: Update `WEBFORM_CORS_ORIGINS` with your Vercel URL

### Frontend Issues

- **Build fails**: Check Vercel build logs
- **API calls fail**: Verify `VITE_API_URL` is correct
- **Blank page**: Check browser console for errors

---

## 📞 Support

If you encounter issues:
1. Check the logs in both Hugging Face and Vercel
2. Verify all environment variables are correctly set
3. Ensure your API keys are valid and have sufficient quota

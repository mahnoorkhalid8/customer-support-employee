# 🔑 Where to Put Your Grok API Key

## Step 1: Get Your Grok API Key

1. Go to https://console.x.ai/
2. Sign in with your xAI account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `xai-`)

## Step 2: Add to .env File

Open the `.env` file in your project root and update:

```bash
# -----------------------------------------------------------------------------
# AI MODEL CONFIGURATION (Grok/xAI)
# -----------------------------------------------------------------------------
GROK_API_KEY=xai-YOUR-ACTUAL-KEY-HERE
GROK_MODEL=grok-beta
GROK_BASE_URL=https://api.x.ai/v1
GROK_MAX_TOKENS=4096
GROK_TEMPERATURE=0.7
```

**Replace `xai-YOUR-ACTUAL-KEY-HERE` with your actual Grok API key!**

## Step 3: That's It!

The code has been updated to use Grok instead of OpenAI. All references have been changed:

### Files Updated:
✅ `.env` - Changed OPENAI_API_KEY to GROK_API_KEY
✅ `production/grok_client.py` - New file for Grok API client
✅ `production/agent/tools.py` - Updated to use Grok client
✅ All documentation files updated

### What Changed:
- **API Key**: Now uses `GROK_API_KEY` instead of `OPENAI_API_KEY`
- **Base URL**: Points to `https://api.x.ai/v1`
- **Model**: Uses `grok-beta` (or whatever model you specify)
- **Client**: Uses OpenAI SDK with custom base URL (Grok is compatible)

## Important Notes

### 1. Grok API Compatibility
Grok API is compatible with OpenAI's API format, so we can use the OpenAI Python SDK with a custom base URL. This means:
- Same request/response format
- Same SDK methods
- Just different endpoint and API key

### 2. Embeddings
⚠️ **Important**: Grok may not have an embeddings API yet. For the knowledge base search feature, you have two options:

**Option A**: Use OpenAI embeddings separately
```bash
# Add to .env
OPENAI_API_KEY=sk-proj-xxx  # Just for embeddings
GROK_API_KEY=xai-xxx        # For chat completions
```

**Option B**: Use a different embeddings service
- Cohere
- Hugging Face
- Sentence Transformers (local)

### 3. Available Models
Check xAI documentation for available models:
- `grok-beta` - Latest Grok model
- Other models as they become available

## Testing Your Setup

```bash
# Start services
docker-compose up -d

# Test the API
curl http://localhost:8000/health

# The agent will now use Grok for responses!
```

## Environment Variables Summary

```bash
# Required
GROK_API_KEY=xai-your-key-here

# Optional (with defaults)
GROK_MODEL=grok-beta
GROK_BASE_URL=https://api.x.ai/v1
GROK_MAX_TOKENS=4096
GROK_TEMPERATURE=0.7
```

## Quick Start

1. **Edit `.env`**:
   ```bash
   GROK_API_KEY=xai-your-actual-key
   ```

2. **Start Docker**:
   ```bash
   docker-compose up -d
   ```

3. **Done!** Your agent now uses Grok API.

---

**Need help?** Check the xAI documentation at https://docs.x.ai/

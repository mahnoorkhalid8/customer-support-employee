"""
Customer Success FTE - Main FastAPI Application
"""

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

from production.database.queries import init_db_pool, close_db_pool
from production.channels.web_form_handler import router as web_form_router
from production.api.routes.gmail_routes import router as gmail_router
from production.api.routes.whatsapp_routes import router as whatsapp_router
from production.services.metrics_service import metrics_service

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Customer Success FTE API...")

    # Setup Gmail credentials from environment (for HF Spaces deployment)
    if os.getenv("GMAIL_ENABLED", "false").lower() == "true":
        try:
            from production.integrations.gmail.setup_credentials import setup_gmail_credentials, setup_gmail_token
            setup_gmail_credentials()
            setup_gmail_token()
        except Exception as e:
            logger.warning(f"Gmail credentials setup failed: {e}")

    # Initialize database only if configured
    db_url = os.getenv("DATABASE_URL")
    if db_url and not db_url.startswith("postgresql://user:password"):
        try:
            await init_db_pool()
            logger.info("Database pool initialized")
        except Exception as e:
            logger.warning(f"Database initialization failed (optional): {e}")
    else:
        logger.info("Database not configured - running without database")

    yield

    # Shutdown
    logger.info("Shutting down Customer Success FTE API...")
    try:
        await close_db_pool()
        logger.info("Database pool closed")
    except Exception as e:
        logger.debug(f"Database cleanup skipped: {e}")


# Initialize FastAPI app
app = FastAPI(
    title="Customer Success FTE API",
    description="24/7 AI-powered customer support across Email, WhatsApp, and Web",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("WEBFORM_CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(web_form_router)
app.include_router(gmail_router)
app.include_router(whatsapp_router)


# =============================================================================
# HEALTH CHECK ENDPOINT
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes probes."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "channels": {
            "email": os.getenv("GMAIL_ENABLED", "false") == "true",
            "whatsapp": os.getenv("WHATSAPP_ENABLED", "false") == "true",
            "web_form": os.getenv("WEBFORM_ENABLED", "false") == "true"
        }
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Customer Success FTE API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# =============================================================================
# WEBHOOK ENDPOINTS (Placeholders - implement in channel handlers)
# =============================================================================

@app.post("/webhooks/gmail")
async def gmail_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle Gmail push notifications via Pub/Sub.
    TODO: Implement in production/channels/gmail_handler.py
    """
    logger.info("Gmail webhook received")
    body = await request.json()

    # TODO: Process Gmail notification
    # from production.channels.gmail_handler import process_gmail_notification
    # background_tasks.add_task(process_gmail_notification, body)

    return {"status": "received", "message": "Gmail webhook handler not yet implemented"}


@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle incoming WhatsApp messages via Twilio webhook.
    TODO: Implement in production/channels/whatsapp_handler.py
    """
    logger.info("WhatsApp webhook received")

    # TODO: Validate Twilio signature
    # TODO: Process WhatsApp message

    # Return TwiML response (empty = no immediate reply)
    return Response(
        content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
        media_type="application/xml"
    )


@app.post("/webhooks/whatsapp/status")
async def whatsapp_status_webhook(request: Request):
    """Handle WhatsApp message status updates."""
    logger.info("WhatsApp status webhook received")
    form_data = await request.form()

    # TODO: Update message delivery status in database

    return {"status": "received"}


# =============================================================================
# WEB FORM ENDPOINTS (Placeholder - implement in channel handler)
# =============================================================================

@app.post("/support/submit")
async def submit_support_form(request: Request):
    """
    Handle support form submission.
    TODO: Implement in production/channels/web_form_handler.py
    """
    logger.info("Support form submission received")
    data = await request.json()

    # TODO: Validate form data
    # TODO: Create ticket
    # TODO: Publish to Kafka

    return {
        "ticket_id": "placeholder-ticket-id",
        "message": "Thank you for contacting us! Our AI assistant will respond shortly.",
        "estimated_response_time": "Usually within 5 minutes"
    }


@app.get("/support/ticket/{ticket_id}")
async def get_ticket_status(ticket_id: str):
    """Get status and conversation history for a ticket."""
    logger.info(f"Ticket status request for: {ticket_id}")

    # TODO: Fetch ticket from database

    return {
        "ticket_id": ticket_id,
        "status": "open",
        "messages": [],
        "created_at": datetime.utcnow().isoformat()
    }


# =============================================================================
# CUSTOMER LOOKUP ENDPOINTS
# =============================================================================

@app.get("/customers/lookup")
async def lookup_customer(email: str = None, phone: str = None):
    """Look up customer by email or phone across all channels."""
    if not email and not phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    logger.info(f"Customer lookup: email={email}, phone={phone}")

    # TODO: Implement customer lookup

    raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get full conversation history with cross-channel context."""
    logger.info(f"Conversation request: {conversation_id}")

    # TODO: Fetch conversation from database

    raise HTTPException(status_code=404, detail="Conversation not found")


# =============================================================================
# METRICS ENDPOINTS
# =============================================================================

@app.get("/metrics/channels")
async def get_channel_metrics():
    """Get performance metrics by channel."""
    logger.info("Channel metrics requested")

    email_stats = metrics_service.get_email_stats()
    whatsapp_stats = metrics_service.get_whatsapp_stats()

    return {
        "email": {
            "total_conversations": email_stats['total'],
            "resolved_count": email_stats['success'],
            "failed_count": email_stats['failed'],
            "success_rate": email_stats['success_rate']
        },
        "whatsapp": {
            "total_conversations": whatsapp_stats['total'],
            "resolved_count": whatsapp_stats['success'],
            "failed_count": whatsapp_stats['failed'],
            "success_rate": whatsapp_stats['success_rate']
        }
    }


@app.get("/metrics/activity")
async def get_activity_metrics(hours: int = 7):
    """Get hourly activity data for graphs."""
    logger.info(f"Activity metrics requested for last {hours} hours")

    email_activity = metrics_service.get_email_activity(hours=hours)
    whatsapp_activity = metrics_service.get_whatsapp_activity(hours=hours)

    return {
        "email": email_activity,
        "whatsapp": whatsapp_activity
    }


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": str(exc) if os.getenv("DEBUG_MODE") == "true" else "An error occurred"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "production.api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENVIRONMENT") == "development"
    )

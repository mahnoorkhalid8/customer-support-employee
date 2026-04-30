"""
Gmail Integration API Routes
Handles Gmail webhooks and operations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
import os

from production.integrations.gmail.gmail_client import GmailClient
from production.ai.customer_support import CustomerSupportAI
from production.services.metrics_service import metrics_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gmail", tags=["gmail"])

# Lazy initialization of clients
_gmail_client = None
_ai_service = None

def check_gmail_enabled():
    """Check if Gmail integration is enabled"""
    enabled = os.getenv("GMAIL_ENABLED", "false").lower() == "true"
    if not enabled:
        raise HTTPException(
            status_code=503,
            detail="Gmail integration is disabled. Set GMAIL_ENABLED=true to enable."
        )

def get_gmail_client():
    check_gmail_enabled()
    global _gmail_client
    if _gmail_client is None:
        _gmail_client = GmailClient()
    return _gmail_client

def get_ai_service():
    global _ai_service
    if _ai_service is None:
        _ai_service = CustomerSupportAI()
    return _ai_service


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    thread_id: Optional[str] = None


class QueryRequest(BaseModel):
    user_email: str
    user_name: Optional[str] = None
    query: str


@router.post("/webhook")
async def gmail_webhook(background_tasks: BackgroundTasks):
    """
    Gmail Pub/Sub webhook endpoint
    Receives notifications when new emails arrive
    """
    # Note: Gmail uses Pub/Sub for webhooks
    # This endpoint receives push notifications
    background_tasks.add_task(process_new_emails)
    return {"status": "processing"}


@router.get("/check-emails")
async def check_emails(background_tasks: BackgroundTasks):
    """
    Manually trigger email check
    Useful for testing and polling
    """
    check_gmail_enabled()
    background_tasks.add_task(process_new_emails)
    return {"status": "checking emails"}


@router.post("/send")
async def send_email(email: EmailRequest):
    """Send email manually"""
    try:
        gmail_client = get_gmail_client()
        success = gmail_client.send_reply(
            to=email.to,
            subject=email.subject,
            body=email.body,
            thread_id=email.thread_id
        )

        if success:
            return {"status": "sent", "to": email.to}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_new_emails():
    """
    Background task to process new emails
    """
    try:
        gmail_client = get_gmail_client()
        ai_service = get_ai_service()

        # Authenticate
        gmail_client.authenticate()

        # Get unread messages
        messages = gmail_client.get_unread_messages(max_results=10)

        logger.info(f"Processing {len(messages)} unread emails")

        for msg in messages:
            try:
                # Generate AI response
                response = ai_service.generate_email_response(
                    subject=msg['subject'],
                    body=msg['body'],
                    sender=msg['from']
                )

                # Send reply
                gmail_client.send_reply(
                    to=msg['from'],
                    subject=response['subject'],
                    body=response['body'],
                    thread_id=msg['thread_id']
                )

                # Mark as read
                gmail_client.mark_as_read(msg['id'])

                # Record success metric
                metrics_service.record_email_processed(success=True)

                logger.info(f"Processed email from {msg['from']}")

            except Exception as e:
                logger.error(f"Error processing email {msg['id']}: {e}")
                # Record failure metric
                metrics_service.record_email_processed(success=False)
                continue

    except Exception as e:
        logger.error(f"Error in process_new_emails: {e}")


@router.post("/submit-query")
async def submit_query(query: QueryRequest):
    """
    Submit a customer query and get AI-generated email response
    This is the main endpoint for the Gmail dashboard
    """
    try:
        gmail_client = get_gmail_client()
        ai_service = get_ai_service()

        # Authenticate
        gmail_client.authenticate()

        logger.info(f"Processing query from {query.user_email}")

        # Generate AI response
        response = ai_service.generate_email_response(
            subject="Your Support Query",
            body=query.query,
            sender=query.user_email,
            sender_name=query.user_name
        )

        # Send reply via email
        success = gmail_client.send_reply(
            to=query.user_email,
            subject=response['subject'],
            body=response['body'],
            thread_id=None
        )

        if success:
            logger.info(f"Successfully sent AI response to {query.user_email}")
            metrics_service.record_email_processed(success=True)
            return {
                "status": "success",
                "message": f"AI response sent to {query.user_email}",
                "response_preview": response['body'][:200] + "..."
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        metrics_service.record_email_processed(success=False)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def gmail_status():
    """Check Gmail integration status"""
    try:
        gmail_client = get_gmail_client()
        gmail_client.authenticate()
        return {
            "status": "connected",
            "service": "gmail"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

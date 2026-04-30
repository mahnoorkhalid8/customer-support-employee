"""
WhatsApp Integration API Routes
Handles Twilio WhatsApp webhooks
"""
from fastapi import APIRouter, HTTPException, Request, Form
from pydantic import BaseModel
from typing import Optional
import logging

from production.integrations.whatsapp.whatsapp_client import WhatsAppClient
from production.ai.customer_support import CustomerSupportAI
from production.services.metrics_service import metrics_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Lazy initialization of clients
_whatsapp_client = None
_ai_service = None

def get_whatsapp_client():
    global _whatsapp_client
    if _whatsapp_client is None:
        _whatsapp_client = WhatsAppClient()
    return _whatsapp_client

def get_ai_service():
    global _ai_service
    if _ai_service is None:
        _ai_service = CustomerSupportAI()
    return _ai_service


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...),
    ProfileName: Optional[str] = Form(None),
    NumMedia: Optional[str] = Form("0")
):
    """
    Twilio WhatsApp webhook endpoint
    Receives incoming WhatsApp messages
    """
    try:
        whatsapp_client = get_whatsapp_client()
        ai_service = get_ai_service()

        # Parse incoming message
        message_data = {
            'From': From,
            'To': To,
            'Body': Body,
            'MessageSid': MessageSid,
            'ProfileName': ProfileName,
            'NumMedia': NumMedia
        }

        parsed = whatsapp_client.parse_incoming_message(message_data)

        logger.info(f"Received WhatsApp from {parsed['from']}: {parsed['body']}")

        # Generate AI response
        ai_response = ai_service.generate_whatsapp_response(
            message=parsed['body'],
            sender=parsed['from'],
            sender_name=parsed['profile_name']
        )

        # Send response
        result = whatsapp_client.send_message(
            to=parsed['from'],
            body=ai_response
        )

        if result['success']:
            logger.info(f"Sent WhatsApp response to {parsed['from']}")
            # Record success metric
            metrics_service.record_whatsapp_processed(success=True)
            return {"status": "success", "message_sid": result['message_sid']}
        else:
            logger.error(f"Failed to send WhatsApp: {result['error']}")
            # Record failure metric
            metrics_service.record_whatsapp_processed(success=False)
            raise HTTPException(status_code=500, detail=result['error'])

    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        # Record failure metric
        metrics_service.record_whatsapp_processed(success=False)
        raise HTTPException(status_code=500, detail=str(e))


class WhatsAppSendRequest(BaseModel):
    to: str
    message: str


@router.post("/send")
async def send_whatsapp(request: WhatsAppSendRequest):
    """
    Send WhatsApp message manually

    Args:
        to: Phone number (format: +1234567890)
        message: Message text
    """
    try:
        whatsapp_client = get_whatsapp_client()
        result = whatsapp_client.send_message(to=request.to, body=request.message)

        if result['success']:
            return {
                "status": "sent",
                "to": request.to,
                "message_sid": result['message_sid']
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'Failed to send message')
            )

    except Exception as e:
        logger.error(f"Error sending WhatsApp: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class WhatsAppQueryRequest(BaseModel):
    phone_number: str
    query: str


@router.post("/submit-query")
async def submit_query(request: WhatsAppQueryRequest):
    """
    Submit a customer query and get AI-generated WhatsApp response

    This endpoint:
    1. Sends the customer's question to their WhatsApp
    2. Generates an AI response
    3. Sends the AI response as a reply

    Args:
        phone_number: Customer's phone number
        query: Customer's question
    """
    try:
        whatsapp_client = get_whatsapp_client()
        ai_service = get_ai_service()

        logger.info(f"Processing WhatsApp query for {request.phone_number}")

        # Step 1: Send the customer's question first
        question_result = whatsapp_client.send_message(
            to=request.phone_number,
            body=request.query
        )

        if not question_result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send question: {question_result.get('error')}"
            )

        # Step 2: Generate AI response
        ai_response = ai_service.generate_whatsapp_response(
            message=request.query,
            sender=request.phone_number,
            sender_name=None
        )

        # Step 3: Send AI response
        answer_result = whatsapp_client.send_message(
            to=request.phone_number,
            body=ai_response
        )

        if answer_result['success']:
            logger.info(f"Successfully sent AI response to {request.phone_number}")
            metrics_service.record_whatsapp_processed(success=True)
            return {
                "status": "success",
                "message": f"Query sent and AI response delivered to {request.phone_number}",
                "question_sid": question_result['message_sid'],
                "answer_sid": answer_result['message_sid'],
                "response_preview": ai_response[:200] + "..."
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send AI response: {answer_result.get('error')}"
            )

    except Exception as e:
        logger.error(f"Error processing WhatsApp query: {e}")
        metrics_service.record_whatsapp_processed(success=False)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def whatsapp_status():
    """Check WhatsApp integration status"""
    try:
        whatsapp_client = get_whatsapp_client()
        # Check if credentials are configured
        if whatsapp_client.account_sid and whatsapp_client.auth_token:
            return {
                "status": "configured",
                "service": "whatsapp",
                "number": whatsapp_client.whatsapp_number
            }
        else:
            return {
                "status": "not_configured",
                "error": "Missing Twilio credentials"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

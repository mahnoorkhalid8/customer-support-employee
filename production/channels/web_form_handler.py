"""
Web form channel handler.

This module handles:
- Support form submission endpoint
- Form validation
- Ticket status retrieval
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid
import logging

from production.database.queries import (
    get_customer_by_email,
    create_customer,
    create_ticket,
    get_ticket
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/support", tags=["support-form"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class SupportFormSubmission(BaseModel):
    """Support form submission model with validation."""

    name: str = Field(..., min_length=2, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    subject: str = Field(..., min_length=5, max_length=500, description="Issue subject")
    category: str = Field(..., description="Issue category")
    message: str = Field(..., min_length=10, max_length=5000, description="Detailed message")
    priority: Optional[str] = Field("medium", description="Priority level")
    attachments: Optional[List[str]] = Field(default=[], description="Attachment URLs or base64")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v.strip()

    @validator('message')
    def message_must_have_content(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Message must be at least 10 characters')
        return v.strip()

    @validator('category')
    def category_must_be_valid(cls, v):
        valid_categories = [
            'general',
            'technical',
            'billing',
            'feedback',
            'bug_report',
            'feature_request'
        ]
        if v not in valid_categories:
            raise ValueError(f'Category must be one of: {", ".join(valid_categories)}')
        return v

    @validator('priority')
    def priority_must_be_valid(cls, v):
        if v is None:
            return 'medium'
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if v not in valid_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return v


class SupportFormResponse(BaseModel):
    """Response model for form submission."""

    ticket_id: str
    message: str
    estimated_response_time: str


class TicketStatusResponse(BaseModel):
    """Response model for ticket status."""

    ticket_id: str
    status: str
    messages: List[dict]
    created_at: str
    last_updated: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/submit", response_model=SupportFormResponse)
async def submit_support_form(submission: SupportFormSubmission):
    """
    Handle support form submission.

    This endpoint:
    1. Validates the submission
    2. Creates or retrieves customer record
    3. Creates a ticket in the system
    4. Publishes to Kafka for agent processing
    5. Returns confirmation to user
    """
    try:
        logger.info(f"Support form submission from {submission.email}")

        # Get or create customer
        customer = await get_customer_by_email(submission.email)

        if customer:
            customer_id = customer['id']
            logger.info(f"Existing customer found: {customer_id}")
        else:
            customer_id = await create_customer(
                email=submission.email,
                name=submission.name
            )
            logger.info(f"New customer created: {customer_id}")

        # Create ticket
        # TODO: Create conversation first, then ticket
        conversation_id = str(uuid.uuid4())  # Placeholder

        ticket_id = await create_ticket(
            customer_id=customer_id,
            conversation_id=conversation_id,
            source_channel='web_form',
            subject=submission.subject,
            category=submission.category,
            priority=submission.priority
        )

        # Create normalized message for agent processing
        message_data = {
            'channel': 'web_form',
            'channel_message_id': ticket_id,
            'customer_email': submission.email,
            'customer_name': submission.name,
            'customer_id': customer_id,
            'subject': submission.subject,
            'content': submission.message,
            'category': submission.category,
            'priority': submission.priority,
            'received_at': datetime.utcnow().isoformat(),
            'metadata': {
                'form_version': '1.0',
                'attachments': submission.attachments
            }
        }

        # TODO: Publish to Kafka for agent processing
        # from production.kafka_client import get_producer, TOPICS
        # producer = await get_producer()
        # await producer.publish(TOPICS['tickets_incoming'], message_data)

        logger.info(f"Ticket created: {ticket_id}")

        return SupportFormResponse(
            ticket_id=ticket_id,
            message="Thank you for contacting us! Our AI assistant will respond shortly.",
            estimated_response_time="Usually within 5 minutes"
        )

    except Exception as e:
        logger.error(f"Error processing form submission: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process your request. Please try again."
        )


@router.get("/ticket/{ticket_id}", response_model=TicketStatusResponse)
async def get_ticket_status(ticket_id: str):
    """
    Get status and conversation history for a ticket.

    Args:
        ticket_id: Ticket UUID

    Returns:
        Ticket status and message history
    """
    try:
        logger.info(f"Ticket status request: {ticket_id}")

        # Get ticket from database
        ticket = await get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # TODO: Get conversation messages
        messages = []

        return TicketStatusResponse(
            ticket_id=ticket_id,
            status=ticket['status'],
            messages=messages,
            created_at=ticket['created_at'].isoformat(),
            last_updated=ticket['updated_at'].isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving ticket status: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve ticket status"
        )


@router.get("/categories")
async def get_categories():
    """Get list of valid support categories."""
    return {
        "categories": [
            {"value": "general", "label": "General Question"},
            {"value": "technical", "label": "Technical Support"},
            {"value": "billing", "label": "Billing Inquiry"},
            {"value": "bug_report", "label": "Bug Report"},
            {"value": "feature_request", "label": "Feature Request"},
            {"value": "feedback", "label": "Feedback"}
        ]
    }


@router.get("/priorities")
async def get_priorities():
    """Get list of valid priority levels."""
    return {
        "priorities": [
            {"value": "low", "label": "Low - Not urgent"},
            {"value": "medium", "label": "Medium - Need help soon"},
            {"value": "high", "label": "High - Urgent issue"},
            {"value": "critical", "label": "Critical - System down"}
        ]
    }

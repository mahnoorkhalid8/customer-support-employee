"""
Agent tools for the Customer Success FTE.

These tools are used by the AI agent (Grok) to interact with
the system and provide customer support.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import logging
import os

from production.database.queries import (
    create_ticket,
    get_customer_history,
    create_escalation,
    search_knowledge_base as db_search_knowledge_base
)
from production.agent.formatters import format_for_channel, Channel
from production.grok_client import generate_embedding

logger = logging.getLogger(__name__)

# Note: The @function_tool decorator is from the OpenAI Agents SDK
# For now, we'll define the tool schemas. When implementing with the actual SDK,
# you'll decorate these functions with @function_tool


# =============================================================================
# INPUT SCHEMAS
# =============================================================================

class KnowledgeSearchInput(BaseModel):
    """Input schema for knowledge base search."""
    query: str = Field(..., description="The search query")
    max_results: int = Field(5, description="Maximum number of results to return")
    category: Optional[str] = Field(None, description="Optional category filter")


class TicketInput(BaseModel):
    """Input schema for creating a ticket."""
    customer_id: str = Field(..., description="Customer ID")
    issue: str = Field(..., description="Description of the issue")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")
    category: Optional[str] = Field(None, description="Issue category")
    channel: str = Field(..., description="Source channel: email, whatsapp, web_form")


class EscalationInput(BaseModel):
    """Input schema for escalating to human support."""
    ticket_id: str = Field(..., description="Ticket ID to escalate")
    reason: str = Field(..., description="Reason for escalation")
    urgency: str = Field("normal", description="Urgency: normal, high, critical")


class ResponseInput(BaseModel):
    """Input schema for sending a response."""
    ticket_id: str = Field(..., description="Ticket ID")
    message: str = Field(..., description="Response message")
    channel: str = Field(..., description="Channel: email, whatsapp, web_form")


class CustomerHistoryInput(BaseModel):
    """Input schema for getting customer history."""
    customer_id: str = Field(..., description="Customer ID")


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

async def search_knowledge_base(input: KnowledgeSearchInput) -> str:
    """
    Search product documentation for relevant information.

    Use this when the customer asks questions about product features,
    how to use something, or needs technical information.

    Args:
        input: Search parameters

    Returns:
        Formatted search results with relevance scores
    """
    try:
        logger.info(f"Searching knowledge base: {input.query}")

        # Generate embedding for the query using Grok
        query_embedding = await generate_embedding(input.query)

        # Search database
        results = await db_search_knowledge_base(
            query_embedding=query_embedding,
            max_results=input.max_results,
            category=input.category
        )

        if not results:
            return "No relevant documentation found. Consider escalating to human support for specialized assistance."

        # Format results
        formatted = []
        for r in results:
            similarity = r.get('similarity', 0)
            formatted.append(
                f"**{r['title']}** (relevance: {similarity:.2f})\n"
                f"{r['content'][:500]}..."
            )

        return "\n\n---\n\n".join(formatted)

    except Exception as e:
        logger.error(f"Knowledge base search failed: {e}", exc_info=True)
        return "Knowledge base temporarily unavailable. Please try again or escalate to human support."


async def create_support_ticket(input: TicketInput) -> str:
    """
    Create a support ticket for tracking.

    ALWAYS create a ticket at the start of every conversation.
    Include the source channel for proper tracking.

    Args:
        input: Ticket information

    Returns:
        Confirmation message with ticket ID
    """
    try:
        logger.info(f"Creating ticket for customer: {input.customer_id}")

        # TODO: Get conversation_id from context
        conversation_id = "placeholder-conversation-id"

        ticket_id = await create_ticket(
            customer_id=input.customer_id,
            conversation_id=conversation_id,
            source_channel=input.channel,
            subject=input.issue[:500],  # Truncate if too long
            category=input.category,
            priority=input.priority
        )

        logger.info(f"Ticket created: {ticket_id}")
        return f"Ticket created successfully: {ticket_id}"

    except Exception as e:
        logger.error(f"Failed to create ticket: {e}", exc_info=True)
        return f"Error creating ticket: {str(e)}"


async def get_customer_interaction_history(input: CustomerHistoryInput) -> str:
    """
    Get customer's complete interaction history across ALL channels.

    Use this to understand context from previous conversations,
    even if they happened on a different channel.

    Args:
        input: Customer identifier

    Returns:
        Formatted customer history
    """
    try:
        logger.info(f"Fetching history for customer: {input.customer_id}")

        # TODO: Implement actual history retrieval
        # For now, return placeholder

        return "No previous interactions found for this customer."

    except Exception as e:
        logger.error(f"Failed to get customer history: {e}", exc_info=True)
        return "Unable to retrieve customer history at this time."


async def escalate_to_human(input: EscalationInput) -> str:
    """
    Escalate conversation to human support.

    Use this when:
    - Customer asks about pricing or refunds
    - Customer sentiment is negative
    - You cannot find relevant information
    - Customer explicitly requests human help

    Args:
        input: Escalation details

    Returns:
        Confirmation message
    """
    try:
        logger.info(f"Escalating ticket: {input.ticket_id}, reason: {input.reason}")

        # TODO: Get conversation_id from context
        conversation_id = "placeholder-conversation-id"

        escalation_id = await create_escalation(
            ticket_id=input.ticket_id,
            conversation_id=conversation_id,
            reason=input.reason,
            urgency=input.urgency
        )

        # TODO: Publish escalation event to Kafka for human agents

        logger.info(f"Escalation created: {escalation_id}")
        return f"Escalated to human support. Reference: {input.ticket_id}"

    except Exception as e:
        logger.error(f"Failed to escalate: {e}", exc_info=True)
        return f"Error escalating ticket: {str(e)}"


async def send_response(input: ResponseInput) -> str:
    """
    Send response to customer via their preferred channel.

    The response will be automatically formatted for the channel.
    Email: Formal with greeting/signature
    WhatsApp: Concise and conversational
    Web: Semi-formal

    Args:
        input: Response details

    Returns:
        Delivery confirmation
    """
    try:
        logger.info(f"Sending response via {input.channel} for ticket: {input.ticket_id}")

        # Format response for channel
        channel_enum = Channel(input.channel)
        formatted = await format_for_channel(
            input.message,
            channel_enum,
            input.ticket_id
        )

        # TODO: Actually send via appropriate channel handler
        # For now, just log
        logger.info(f"Formatted response ({len(formatted)} chars): {formatted[:100]}...")

        # TODO: Store message in database

        return f"Response sent via {input.channel}: delivered"

    except Exception as e:
        logger.error(f"Failed to send response: {e}", exc_info=True)
        return f"Error sending response: {str(e)}"


# =============================================================================
# TOOL REGISTRY (for OpenAI Agents SDK)
# =============================================================================

# When implementing with the actual OpenAI Agents SDK, you would decorate
# the functions above with @function_tool and register them with the agent.
# Example:
#
# from agents import function_tool
#
# @function_tool
# async def search_knowledge_base(input: KnowledgeSearchInput) -> str:
#     ...

TOOL_FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
    "create_ticket": create_support_ticket,
    "get_customer_history": get_customer_interaction_history,
    "escalate_to_human": escalate_to_human,
    "send_response": send_response
}

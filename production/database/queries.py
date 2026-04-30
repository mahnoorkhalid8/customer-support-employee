"""
Database connection and query utilities.
"""

import asyncpg
import os
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def init_db_pool():
    """Initialize the database connection pool."""
    global _pool

    if _pool is not None:
        return _pool

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")

    _pool = await asyncpg.create_pool(
        database_url,
        min_size=int(os.getenv("POSTGRES_MIN_POOL_SIZE", "5")),
        max_size=int(os.getenv("POSTGRES_MAX_POOL_SIZE", "20")),
        command_timeout=60,
    )

    logger.info("Database connection pool initialized")
    return _pool


async def close_db_pool():
    """Close the database connection pool."""
    global _pool

    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


async def get_db_pool() -> asyncpg.Pool:
    """Get the database connection pool."""
    global _pool

    if _pool is None:
        await init_db_pool()

    return _pool


@asynccontextmanager
async def get_db_connection():
    """Context manager for database connections."""
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        yield connection


# =============================================================================
# CUSTOMER QUERIES
# =============================================================================

async def get_customer_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get customer by email address."""
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM customers WHERE email = $1",
            email
        )
        return dict(row) if row else None


async def get_customer_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    """Get customer by phone number."""
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT c.* FROM customers c
            JOIN customer_identifiers ci ON c.id = ci.customer_id
            WHERE ci.identifier_type = 'whatsapp' AND ci.identifier_value = $1
            """,
            phone
        )
        return dict(row) if row else None


async def create_customer(
    email: Optional[str] = None,
    phone: Optional[str] = None,
    name: Optional[str] = None,
    company: Optional[str] = None,
    plan_type: str = "starter"
) -> str:
    """Create a new customer and return customer_id."""
    async with get_db_connection() as conn:
        customer_id = await conn.fetchval(
            """
            INSERT INTO customers (email, phone, name, company, plan_type)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            email, phone, name, company, plan_type
        )
        return str(customer_id)


# =============================================================================
# CONVERSATION QUERIES
# =============================================================================

async def create_conversation(
    customer_id: str,
    channel: str
) -> str:
    """Create a new conversation."""
    async with get_db_connection() as conn:
        conversation_id = await conn.fetchval(
            """
            INSERT INTO conversations (customer_id, initial_channel, status)
            VALUES ($1, $2, 'active')
            RETURNING id
            """,
            customer_id, channel
        )
        return str(conversation_id)


async def get_active_conversation(customer_id: str) -> Optional[Dict[str, Any]]:
    """Get active conversation for customer (within last 24 hours)."""
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM conversations
            WHERE customer_id = $1
              AND status = 'active'
              AND started_at > NOW() - INTERVAL '24 hours'
            ORDER BY started_at DESC
            LIMIT 1
            """,
            customer_id
        )
        return dict(row) if row else None


async def get_conversation_history(conversation_id: str) -> List[Dict[str, Any]]:
    """Get all messages in a conversation."""
    async with get_db_connection() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM messages
            WHERE conversation_id = $1
            ORDER BY created_at ASC
            """,
            conversation_id
        )
        return [dict(row) for row in rows]


# =============================================================================
# MESSAGE QUERIES
# =============================================================================

async def store_message(
    conversation_id: str,
    channel: str,
    direction: str,
    role: str,
    content: str,
    channel_message_id: Optional[str] = None,
    tokens_used: Optional[int] = None,
    latency_ms: Optional[int] = None,
    tool_calls: Optional[List[Dict]] = None
) -> str:
    """Store a message in the database."""
    async with get_db_connection() as conn:
        message_id = await conn.fetchval(
            """
            INSERT INTO messages (
                conversation_id, channel, direction, role, content,
                channel_message_id, tokens_used, latency_ms, tool_calls
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
            """,
            conversation_id, channel, direction, role, content,
            channel_message_id, tokens_used, latency_ms, tool_calls or []
        )
        return str(message_id)


# =============================================================================
# TICKET QUERIES
# =============================================================================

async def create_ticket(
    customer_id: str,
    conversation_id: str,
    source_channel: str,
    subject: Optional[str] = None,
    category: Optional[str] = None,
    priority: str = "medium"
) -> str:
    """Create a support ticket."""
    async with get_db_connection() as conn:
        ticket_id = await conn.fetchval(
            """
            INSERT INTO tickets (
                customer_id, conversation_id, source_channel,
                subject, category, priority, status
            )
            VALUES ($1, $2, $3, $4, $5, $6, 'open')
            RETURNING id
            """,
            customer_id, conversation_id, source_channel,
            subject, category, priority
        )
        return str(ticket_id)


async def get_ticket(ticket_id: str) -> Optional[Dict[str, Any]]:
    """Get ticket by ID."""
    async with get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM tickets WHERE id = $1",
            ticket_id
        )
        return dict(row) if row else None


async def update_ticket_status(
    ticket_id: str,
    status: str,
    resolution_notes: Optional[str] = None
) -> None:
    """Update ticket status."""
    async with get_db_connection() as conn:
        await conn.execute(
            """
            UPDATE tickets
            SET status = $1,
                resolution_notes = $2,
                resolved_at = CASE WHEN $1 IN ('resolved', 'closed') THEN NOW() ELSE NULL END
            WHERE id = $3
            """,
            status, resolution_notes, ticket_id
        )


# =============================================================================
# KNOWLEDGE BASE QUERIES
# =============================================================================

async def search_knowledge_base(
    query_embedding: List[float],
    max_results: int = 5,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search knowledge base using vector similarity."""
    async with get_db_connection() as conn:
        if category:
            rows = await conn.fetch(
                """
                SELECT id, title, content, category,
                       1 - (embedding <=> $1::vector) as similarity
                FROM knowledge_base
                WHERE category = $2
                ORDER BY embedding <=> $1::vector
                LIMIT $3
                """,
                query_embedding, category, max_results
            )
        else:
            rows = await conn.fetch(
                """
                SELECT id, title, content, category,
                       1 - (embedding <=> $1::vector) as similarity
                FROM knowledge_base
                ORDER BY embedding <=> $1::vector
                LIMIT $2
                """,
                query_embedding, max_results
            )

        return [dict(row) for row in rows]


# =============================================================================
# ESCALATION QUERIES
# =============================================================================

async def create_escalation(
    ticket_id: str,
    conversation_id: str,
    reason: str,
    urgency: str = "normal"
) -> str:
    """Create an escalation record."""
    async with get_db_connection() as conn:
        escalation_id = await conn.fetchval(
            """
            INSERT INTO escalations (ticket_id, conversation_id, reason, urgency, status)
            VALUES ($1, $2, $3, $4, 'pending')
            RETURNING id
            """,
            ticket_id, conversation_id, reason, urgency
        )

        # Update ticket status
        await conn.execute(
            "UPDATE tickets SET status = 'escalated' WHERE id = $1",
            ticket_id
        )

        # Update conversation status
        await conn.execute(
            """
            UPDATE conversations
            SET status = 'escalated', escalation_reason = $1
            WHERE id = $2
            """,
            reason, conversation_id
        )

        return str(escalation_id)


# =============================================================================
# METRICS QUERIES
# =============================================================================

async def record_metric(
    metric_name: str,
    metric_value: float,
    channel: Optional[str] = None,
    dimensions: Optional[Dict] = None
) -> None:
    """Record a metric."""
    async with get_db_connection() as conn:
        await conn.execute(
            """
            INSERT INTO agent_metrics (metric_name, metric_value, channel, dimensions)
            VALUES ($1, $2, $3, $4)
            """,
            metric_name, metric_value, channel, dimensions or {}
        )


async def get_channel_metrics(hours: int = 24) -> List[Dict[str, Any]]:
    """Get metrics by channel for the last N hours."""
    async with get_db_connection() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM channel_metrics_view
            """,
        )
        return [dict(row) for row in rows]

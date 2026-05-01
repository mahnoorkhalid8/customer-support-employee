"""
AI client configuration for Grok API.

This module provides a wrapper around the Grok API (xAI) that's compatible
with OpenAI's interface.
"""

import os
from groq import Groq
import logging

logger = logging.getLogger(__name__)


def get_grok_client() -> Groq:
    """
    Get configured Grok API client using official Groq SDK.

    Returns:
        Groq client configured for API access
    """
    api_key = os.getenv("GROK_API_KEY")

    if not api_key:
        raise ValueError("GROK_API_KEY environment variable not set")

    client = Groq(
        api_key=api_key,
        timeout=30.0,  # 30 second timeout
        max_retries=2  # Retry up to 2 times
    )

    logger.info(f"Grok client initialized with official Groq SDK")
    return client


def get_model_name() -> str:
    """Get the Grok model name from environment."""
    return os.getenv("GROK_MODEL", "grok-beta")


def get_max_tokens() -> int:
    """Get max tokens from environment."""
    return int(os.getenv("GROK_MAX_TOKENS", "4096"))


def get_temperature() -> float:
    """Get temperature from environment."""
    return float(os.getenv("GROK_TEMPERATURE", "0.7"))


async def generate_embedding(text: str) -> list[float]:
    """
    Generate embeddings for text.

    Note: Grok may not have embeddings API yet. You might need to use
    OpenAI's embeddings API separately or use a different service.

    Args:
        text: Text to embed

    Returns:
        Embedding vector
    """
    # TODO: Check if Grok has embeddings API
    # For now, return a placeholder or use OpenAI embeddings separately
    logger.warning("Grok embeddings not implemented. Using placeholder.")
    return [0.0] * 1536  # Placeholder embedding


async def chat_completion(messages: list, **kwargs) -> dict:
    """
    Create a chat completion using Grok API.

    Args:
        messages: List of message dicts with 'role' and 'content'
        **kwargs: Additional parameters (temperature, max_tokens, etc.)

    Returns:
        Completion response
    """
    client = get_grok_client()

    response = client.chat.completions.create(
        model=get_model_name(),
        messages=messages,
        temperature=kwargs.get('temperature', get_temperature()),
        max_tokens=kwargs.get('max_tokens', get_max_tokens()),
        **kwargs
    )

    return response

"""
Hugging Face Inference API client configuration.

This module provides a wrapper around the HF Inference API for free AI generation.
"""

import os
from huggingface_hub import InferenceClient
import logging

logger = logging.getLogger(__name__)


def get_hf_client() -> InferenceClient:
    """
    Get configured Hugging Face Inference API client.

    Returns:
        InferenceClient configured for API access
    """
    api_key = os.getenv("HF_API_KEY")

    # HF API key is optional - can use free tier without it
    if api_key:
        client = InferenceClient(token=api_key)
        logger.info("HF Inference client initialized with API key")
    else:
        client = InferenceClient()
        logger.info("HF Inference client initialized (free tier, no API key)")

    return client


def get_model_name() -> str:
    """Get the HF model name from environment."""
    # Default to Llama 3.2 3B - free and fast
    return os.getenv("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")


def get_max_tokens() -> int:
    """Get max tokens from environment."""
    return int(os.getenv("HF_MAX_TOKENS", "1000"))


def get_temperature() -> float:
    """Get temperature from environment."""
    return float(os.getenv("HF_TEMPERATURE", "0.7"))

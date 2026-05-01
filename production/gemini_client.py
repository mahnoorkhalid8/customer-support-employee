"""
Gemini AI client configuration.

This module provides a wrapper around Google's Gemini API.
"""

import os
import logging

# Import with explicit error handling for namespace package issues
try:
    import google.generativeai as genai
except ImportError as e:
    # Fallback: try importing the module directly
    import sys
    import importlib.util
    spec = importlib.util.find_spec("google.generativeai")
    if spec is None:
        raise ImportError(f"google-generativeai package not found. Install with: pip install google-generativeai") from e
    genai = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(genai)

logger = logging.getLogger(__name__)


def get_gemini_client():
    """
    Get configured Gemini API client.

    Returns:
        Configured Gemini client
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    logger.info(f"Gemini client initialized with model: {get_model_name()}")
    return genai


def get_model_name() -> str:
    """Get the Gemini model name from environment."""
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")


def get_max_tokens() -> int:
    """Get max tokens from environment."""
    return int(os.getenv("GEMINI_MAX_TOKENS", "4096"))


def get_temperature() -> float:
    """Get temperature from environment."""
    return float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

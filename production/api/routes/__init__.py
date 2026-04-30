"""
API routes package
"""
from production.api.routes.gmail_routes import router as gmail_router
from production.api.routes.whatsapp_routes import router as whatsapp_router

__all__ = ['gmail_router', 'whatsapp_router']

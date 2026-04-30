"""
Basic tests for the Customer Success FTE API.
"""

import pytest
from httpx import AsyncClient
from production.api.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "channels" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


@pytest.mark.asyncio
async def test_support_form_validation():
    """Test support form validation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with invalid data (name too short)
        response = await client.post("/support/submit", json={
            "name": "A",
            "email": "invalid-email",
            "subject": "Hi",
            "category": "general",
            "message": "Short"
        })
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_categories():
    """Test getting support categories."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/support/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) > 0


@pytest.mark.asyncio
async def test_get_priorities():
    """Test getting priority levels."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/support/priorities")
        assert response.status_code == 200
        data = response.json()
        assert "priorities" in data
        assert len(data["priorities"]) > 0

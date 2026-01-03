"""
Tests for Health Check Endpoints

Tests the root and health check endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint returns correct response."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "bankAPI is running!"
    assert data["version"] == "0.1.0"
    assert data["docs"] == "/docs"


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    """Test health check endpoint returns healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

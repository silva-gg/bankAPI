"""
Tests for Authentication Endpoints

Tests user registration, login, profile management, and admin operations.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserRegistration:
    """Tests for user registration endpoint."""
    
    async def test_register_user_success(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "user_number": "111222333",
            "user_fullname": "John Doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["user_number"] == user_data["user_number"]
        assert data["email"] == user_data["email"]
        assert data["user_fullname"] == "John Doe"
        assert "password" not in data
        assert "hashed_password" not in data
        assert data["is_active"] is True
        assert data["is_superuser"] is False
    
    async def test_register_duplicate_user_number(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate user number fails."""
        user_data = {
            "user_number": test_user["user_number"],
            "user_fullname": "Jane Doe",
            "email": "different@example.com",
            "password": "SecurePass123!"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate email fails."""
        user_data = {
            "user_number": "999888777",
            "user_fullname": "Jane Doe",
            "email": test_user["email"],
            "password": "SecurePass123!"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 409
        assert "already" in response.json()["detail"].lower()
    
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email fails."""
        user_data = {
            "user_number": "111222333",
            "user_fullname": "John Doe",
            "email": "invalid-email",
            "password": "SecurePass123!"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 422
    
    async def test_register_weak_password(self, client: AsyncClient):
        """Test registration with weak password fails."""
        user_data = {
            "user_number": "111222333",
            "user_fullname": "John Doe",
            "email": "john@example.com",
            "password": "weak"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 422
    
    async def test_register_invalid_fullname(self, client: AsyncClient):
        """Test registration with invalid full name fails."""
        user_data = {
            "user_number": "111222333",
            "user_fullname": "John",  # Only one name
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
        
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 422


@pytest.mark.asyncio
class TestUserLogin:
    """Tests for user login endpoint."""
    
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """Test successful login."""
        credentials = {
            "user_number": test_user["user_number"],
            "password": test_user["password"]
        }
        
        response = await client.post("/auth/login", json=credentials)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    async def test_login_wrong_password(self, client: AsyncClient, test_user: dict):
        """Test login with incorrect password fails."""
        credentials = {
            "user_number": test_user["user_number"],
            "password": "WrongPassword123!"
        }
        
        response = await client.post("/auth/login", json=credentials)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user fails."""
        credentials = {
            "user_number": "999999999",
            "password": "SomePassword123!"
        }
        
        response = await client.post("/auth/login", json=credentials)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestCurrentUser:
    """Tests for current user endpoints."""
    
    async def test_get_current_user(self, client: AsyncClient, test_user: dict, auth_headers: dict):
        """Test getting current user information."""
        response = await client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["user_number"] == test_user["user_number"]
        assert data["email"] == test_user["email"]
        assert "password" not in data
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication fails."""
        response = await client.get("/auth/me")
        assert response.status_code == 401
    
    async def test_update_current_user_email(self, client: AsyncClient, auth_headers: dict):
        """Test updating current user email."""
        update_data = {
            "email": "newemail@example.com"
        }
        
        response = await client.patch("/auth/me", headers=auth_headers, json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == update_data["email"]
    
    async def test_update_current_user_fullname(self, client: AsyncClient, auth_headers: dict):
        """Test updating current user full name."""
        update_data = {
            "user_fullname": "Updated Name"
        }
        
        response = await client.patch("/auth/me", headers=auth_headers, json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_fullname"] == "Updated Name"
    
    async def test_update_current_user_password(self, client: AsyncClient, test_user: dict, auth_headers: dict):
        """Test updating current user password."""
        update_data = {
            "password": "NewSecurePass123!"
        }
        
        response = await client.patch("/auth/me", headers=auth_headers, json=update_data)
        assert response.status_code == 200
        
        # Test login with new password
        credentials = {
            "user_number": test_user["user_number"],
            "password": update_data["password"]
        }
        login_response = await client.post("/auth/login", json=credentials)
        assert login_response.status_code == 200


@pytest.mark.asyncio
class TestAdminOperations:
    """Tests for admin-only endpoints."""
    
    async def test_list_users_as_admin(self, client: AsyncClient, test_user: dict, test_admin: dict, admin_headers: dict):
        """Test admin can list all users."""
        response = await client.get("/auth/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 2  # At least test_user and test_admin
    
    async def test_list_users_as_regular_user_fails(self, client: AsyncClient, auth_headers: dict):
        """Test regular user cannot list all users."""
        response = await client.get("/auth/users", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_list_users_with_filters(self, client: AsyncClient, test_user: dict, admin_headers: dict):
        """Test listing users with filters."""
        response = await client.get(
            f"/auth/users?is_active=true",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        for user in data["items"]:
            assert user["is_active"] is True
    
    async def test_delete_user_as_admin(self, client: AsyncClient, test_user: dict, admin_headers: dict):
        """Test admin can delete a user."""
        response = await client.delete(
            f"/auth/users/{test_user['uuid5']}",
            headers=admin_headers
        )
        assert response.status_code == 204
    
    async def test_delete_user_as_regular_user_fails(self, client: AsyncClient, test_user: dict, auth_headers: dict):
        """Test regular user cannot delete users."""
        response = await client.delete(
            f"/auth/users/{test_user['uuid5']}",
            headers=auth_headers
        )
        assert response.status_code == 403
    
    async def test_admin_cannot_delete_themselves(self, client: AsyncClient, test_admin: dict, admin_headers: dict):
        """Test admin cannot delete their own account."""
        response = await client.delete(
            f"/auth/users/{test_admin['uuid5']}",
            headers=admin_headers
        )
        assert response.status_code == 403
        assert "cannot delete" in response.json()["detail"].lower()

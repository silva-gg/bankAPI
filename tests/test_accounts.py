"""
Tests for Account Endpoints

Tests account creation, listing, retrieval, update, and deletion.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAccountCreation:
    """Tests for account creation endpoint."""
    
    async def test_create_savings_account(self, client: AsyncClient, auth_headers: dict):
        """Test creating a savings account."""
        account_data = {
            "account_type": "savings",
            "password": "AccountPass123!"
        }
        
        response = await client.post("/accounts/", headers=auth_headers, json=account_data)
        assert response.status_code == 201
        data = response.json()
        assert data["account_type"] == "savings"
        assert "account_number" in data
        assert data["is_active"] is True
        assert "password" not in data
        assert "hashed_password" not in data
    
    async def test_create_checking_account(self, client: AsyncClient, auth_headers: dict):
        """Test creating a checking account."""
        account_data = {
            "account_type": "checking",
            "password": "AccountPass123!"
        }
        
        response = await client.post("/accounts/", headers=auth_headers, json=account_data)
        assert response.status_code == 201
        data = response.json()
        assert data["account_type"] == "checking"
    
    async def test_create_business_account(self, client: AsyncClient, auth_headers: dict):
        """Test creating a business account."""
        account_data = {
            "account_type": "business",
            "password": "AccountPass123!"
        }
        
        response = await client.post("/accounts/", headers=auth_headers, json=account_data)
        assert response.status_code == 201
        data = response.json()
        assert data["account_type"] == "business"
    
    async def test_create_account_without_auth_fails(self, client: AsyncClient):
        """Test creating account without authentication fails."""
        account_data = {
            "account_type": "savings",
            "password": "AccountPass123!"
        }
        
        response = await client.post("/accounts/", json=account_data)
        assert response.status_code == 401
    
    async def test_create_account_invalid_type(self, client: AsyncClient, auth_headers: dict):
        """Test creating account with invalid type fails."""
        account_data = {
            "account_type": "invalid_type",
            "password": "AccountPass123!"
        }
        
        response = await client.post("/accounts/", headers=auth_headers, json=account_data)
        assert response.status_code == 422


@pytest.mark.asyncio
class TestAccountListing:
    """Tests for account listing endpoints."""
    
    async def test_list_my_accounts(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test listing logged-in user's accounts."""
        response = await client.get("/accounts/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1
        # Verify account is in the list
        account_numbers = [acc["account_number"] for acc in data["items"]]
        assert test_account["account_number"] in account_numbers
    
    async def test_list_my_accounts_filter_by_type(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering user's accounts by type."""
        response = await client.get(
            f"/accounts/me?account_type={test_account['account_type']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        for account in data["items"]:
            assert account["account_type"] == test_account["account_type"]
    
    async def test_list_my_accounts_filter_by_active(self, client: AsyncClient, auth_headers: dict):
        """Test filtering user's accounts by active status."""
        response = await client.get("/accounts/me?is_active=true", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        for account in data["items"]:
            assert account["balance"] >= 0
    
    async def test_list_all_accounts_as_admin(self, client: AsyncClient, test_account: dict, admin_headers: dict):
        """Test admin can list all accounts."""
        response = await client.get("/accounts/", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    async def test_list_all_accounts_as_regular_user_fails(self, client: AsyncClient, auth_headers: dict):
        """Test regular user cannot list all accounts."""
        response = await client.get("/accounts/", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_list_accounts_without_auth_fails(self, client: AsyncClient):
        """Test listing accounts without authentication fails."""
        response = await client.get("/accounts/me")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestAccountRetrieval:
    """Tests for account retrieval by ID."""
    
    async def test_get_account_by_id_as_admin(self, client: AsyncClient, test_account: dict, admin_headers: dict):
        """Test admin can get account by ID."""
        response = await client.get(
            f"/accounts/{test_account['id']}",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["account_number"] == test_account["account_number"]
    
    async def test_get_account_by_id_as_regular_user_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test regular user cannot get account by ID."""
        response = await client.get(
            f"/accounts/{test_account['id']}",
            headers=auth_headers
        )
        assert response.status_code == 403
    
    async def test_get_nonexistent_account(self, client: AsyncClient, admin_headers: dict):
        """Test getting non-existent account returns 404."""
        fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
        response = await client.get(
            f"/accounts/{fake_uuid}",
            headers=admin_headers
        )
        assert response.status_code == 404


@pytest.mark.asyncio
class TestAccountUpdate:
    """Tests for account update endpoint."""
    
    async def test_update_account_as_admin(self, client: AsyncClient, test_account: dict, admin_headers: dict):
        """Test admin can update account."""
        update_data = {
            "password": "NewAccountPass123!"
        }
        
        response = await client.patch(
            f"/accounts/{test_account['id']}",
            headers=admin_headers,
            json=update_data
        )
        assert response.status_code == 200
    
    async def test_update_account_as_regular_user_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test regular user cannot update account."""
        update_data = {
            "password": "NewAccountPass123!"
        }
        
        response = await client.patch(
            f"/accounts/{test_account['id']}",
            headers=auth_headers,
            json=update_data
        )
        assert response.status_code == 403
    
    async def test_update_nonexistent_account(self, client: AsyncClient, admin_headers: dict):
        """Test updating non-existent account returns 404."""
        fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
        update_data = {
            "password": "NewAccountPass123!"
        }
        
        response = await client.patch(
            f"/accounts/{fake_uuid}",
            headers=admin_headers,
            json=update_data
        )
        assert response.status_code == 404


@pytest.mark.asyncio
class TestAccountDeletion:
    """Tests for account deletion endpoint."""
    
    async def test_delete_account_as_admin(self, client: AsyncClient, test_account: dict, admin_headers: dict):
        """Test admin can delete account."""
        response = await client.delete(
            f"/accounts/{test_account['id']}",
            headers=admin_headers
        )
        assert response.status_code == 204
        
        # Verify account is deleted
        get_response = await client.get(
            f"/accounts/{test_account['id']}",
            headers=admin_headers
        )
        assert get_response.status_code == 404
    
    async def test_delete_account_as_regular_user_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test regular user cannot delete account."""
        response = await client.delete(
            f"/accounts/{test_account['id']}",
            headers=auth_headers
        )
        assert response.status_code == 403
    
    async def test_delete_nonexistent_account(self, client: AsyncClient, admin_headers: dict):
        """Test deleting non-existent account returns 404."""
        fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
        response = await client.delete(
            f"/accounts/{fake_uuid}",
            headers=admin_headers
        )
        assert response.status_code == 404


@pytest.mark.asyncio
class TestAccountPagination:
    """Tests for account pagination."""
    
    async def test_pagination_page_size(self, client: AsyncClient, auth_headers: dict):
        """Test pagination with custom page size."""
        # Create multiple accounts
        for i in range(5):
            account_data = {
                "account_type": "savings",
                "password": f"AccountPass{i}123!"
            }
            await client.post("/accounts/", headers=auth_headers, json=account_data)
        
        # Test pagination
        response = await client.get("/accounts/me?page=1&size=2", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) <= 2

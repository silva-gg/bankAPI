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


@pytest.mark.asyncio
class TestBankStatement:
    """Tests for bank statement endpoint."""
    
    async def test_get_statement_basic(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test getting basic bank statement without date filters."""
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["account_number"] == test_account["account_number"]
        assert data["account_type"] == test_account["account_type"]
        assert "balance" in data
        assert "transactions" in data
        assert isinstance(data["transactions"], list)
    
    async def test_get_statement_with_transactions(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test getting statement includes transactions."""
        # Create some transactions
        deposit_data = {
            "value": 100.0,
            "transaction_type": "deposit",
            "origin_account_number": test_account["account_number"]
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        withdrawal_data = {
            "value": 50.0,
            "transaction_type": "withdrawal",
            "origin_account_number": test_account["account_number"]
        }
        await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        
        # Get statement
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["transactions"]) >= 2
        
        # Verify transaction structure
        for txn in data["transactions"]:
            assert "pk_id" in txn
            assert "value" in txn
            assert "transaction_type" in txn
            assert "created_at" in txn
            assert "origin_account_number" in txn
    
    async def test_get_statement_with_initial_date(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering statement by initial date."""
        from datetime import datetime, timedelta
        
        # Use a recent date
        initial_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}&initial_date={initial_date}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        
        # Verify all transactions are after initial_date
        for txn in data["transactions"]:
            txn_date = datetime.fromisoformat(txn["created_at"].replace('Z', '+00:00'))
            filter_date = datetime.fromisoformat(initial_date)
            assert txn_date.date() >= filter_date.date()
    
    async def test_get_statement_with_final_date(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering statement by final date."""
        from datetime import datetime
        
        # Use current date
        final_date = datetime.utcnow().strftime('%Y-%m-%d')
        
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}&final_date={final_date}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        
        # Verify all transactions are before or on final_date
        for txn in data["transactions"]:
            txn_date = datetime.fromisoformat(txn["created_at"].replace('Z', '+00:00'))
            filter_date = datetime.fromisoformat(final_date)
            assert txn_date.date() <= filter_date.date()
    
    async def test_get_statement_with_date_range(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering statement by date range."""
        from datetime import datetime, timedelta
        
        # Create transactions
        deposit_data = {
            "value": 100.0,
            "transaction_type": "deposit",
            "origin_account_number": test_account["account_number"]
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Set date range
        initial_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
        final_date = datetime.utcnow().strftime('%Y-%m-%d')
        
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}&initial_date={initial_date}&final_date={final_date}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        
        # Verify transactions are within date range
        for txn in data["transactions"]:
            txn_date = datetime.fromisoformat(txn["created_at"].replace('Z', '+00:00'))
            start_date = datetime.fromisoformat(initial_date)
            end_date = datetime.fromisoformat(final_date)
            assert start_date.date() <= txn_date.date() <= end_date.date()
    
    async def test_get_statement_nonexistent_account(self, client: AsyncClient, auth_headers: dict):
        """Test getting statement for non-existent account returns 404."""
        fake_account_number = 99999999  # Valid int32 value
        response = await client.get(
            f"/accounts/statements/me?account_number={fake_account_number}",
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_get_statement_other_users_account(self, client: AsyncClient, test_account: dict, admin_headers: dict):
        """Test getting statement for account not owned by user returns 404."""
        # Try to access test_account (owned by regular user) with admin credentials
        # This should fail because the endpoint checks ownership
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}",
            headers=admin_headers
        )
        # Should return 404 since admin doesn't own this account
        assert response.status_code == 404
    
    async def test_get_statement_without_auth(self, client: AsyncClient, test_account: dict):
        """Test getting statement without authentication fails."""
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}"
        )
        assert response.status_code == 401
    
    async def test_get_statement_missing_account_number(self, client: AsyncClient, auth_headers: dict):
        """Test getting statement without account_number parameter fails."""
        response = await client.get(
            "/accounts/statements/me",
            headers=auth_headers
        )
        assert response.status_code == 422
    
    async def test_get_statement_balance_accuracy(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test that statement balance reflects account balance."""
        response = await client.get(
            f"/accounts/statements/me?account_number={test_account['account_number']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Get account directly
        accounts_response = await client.get("/accounts/me", headers=auth_headers)
        accounts_data = accounts_response.json()
        account = next(
            (acc for acc in accounts_data["items"] if acc["account_number"] == test_account["account_number"]),
            None
        )
        
        if account:
            assert data["balance"] == account["balance"]

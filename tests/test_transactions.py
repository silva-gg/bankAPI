"""
Tests for Transaction Endpoints

Tests transaction creation, deposits, withdrawals, transfers, and listing.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestDeposits:
    """Tests for deposit transactions."""
    
    async def test_create_deposit(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test creating a deposit transaction."""
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": 500.00,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        assert response.status_code == 201
        data = response.json()
        assert data["value"] == 500.00
        assert data["transaction_type"] == "deposit"
        assert "id" in data
        assert "created_at" in data
    
    async def test_deposit_increases_balance(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test that deposit increases account balance."""
        initial_balance = test_account["balance"]
        deposit_amount = 1000.00
        
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": deposit_amount,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        assert response.status_code == 201
        
        # Check account balance increased
        accounts_response = await client.get("/accounts/me", headers=auth_headers)
        accounts = accounts_response.json()["items"]
        updated_account = next(
            acc for acc in accounts if acc["account_number"] == test_account["account_number"]
        )
        assert updated_account["balance"] == initial_balance + deposit_amount
    
    async def test_deposit_negative_value_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test deposit with negative value fails."""
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": -100.00,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        assert response.status_code == 422
    
    async def test_deposit_without_auth_fails(self, client: AsyncClient, test_account: dict):
        """Test deposit without authentication fails."""
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": 100.00,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", json=transaction_data)
        assert response.status_code == 401
    
    async def test_deposit_nonexistent_account_fails(self, client: AsyncClient, auth_headers: dict):
        """Test deposit to non-existent account fails."""
        transaction_data = {
            "origin_account_number": 9999999999,
            "value": 100.00,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        assert response.status_code == 404


@pytest.mark.asyncio
class TestWithdrawals:
    """Tests for withdrawal transactions."""
    
    async def test_create_withdrawal(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test creating a withdrawal transaction."""
        # First deposit some money
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": 1000.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Now withdraw
        withdrawal_data = {
            "origin_account_number": test_account["account_number"],
            "value": 200.00,
            "transaction_type": "withdrawal"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        assert response.status_code == 201
        data = response.json()
        assert data["value"] == 200.00
        assert data["transaction_type"] == "withdrawal"
    
    async def test_withdrawal_decreases_balance(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test that withdrawal decreases account balance."""
        # Deposit money first
        deposit_amount = 1000.00
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": deposit_amount,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Get current balance
        accounts_response = await client.get("/accounts/me", headers=auth_headers)
        accounts = accounts_response.json()["items"]
        account = next(
            acc for acc in accounts if acc["account_number"] == test_account["account_number"]
        )
        current_balance = account["balance"]
        
        # Withdraw
        withdrawal_amount = 300.00
        withdrawal_data = {
            "origin_account_number": test_account["account_number"],
            "value": withdrawal_amount,
            "transaction_type": "withdrawal"
        }
        response = await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        assert response.status_code == 201
        
        # Check balance decreased
        accounts_response = await client.get("/accounts/me", headers=auth_headers)
        accounts = accounts_response.json()["items"]
        updated_account = next(
            acc for acc in accounts if acc["account_number"] == test_account["account_number"]
        )
        assert updated_account["balance"] == current_balance - withdrawal_amount
    
    async def test_withdrawal_insufficient_funds(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test withdrawal with insufficient funds fails."""
        # Try to withdraw more than balance (without special withdrawal limit)
        withdrawal_data = {
            "origin_account_number": test_account["account_number"],
            "value": 999999.00,
            "transaction_type": "withdrawal"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()
    
    async def test_withdrawal_daily_limit(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test withdrawal daily limit enforcement."""
        # First deposit a large amount
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": 10000.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Make multiple withdrawals (default limit is typically 3)
        withdrawal_data = {
            "origin_account_number": test_account["account_number"],
            "value": 100.00,
            "transaction_type": "withdrawal"
        }
        
        # Make withdrawals up to the limit
        for i in range(3):
            response = await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
            assert response.status_code == 201
        
        # Next withdrawal should fail due to daily limit
        response = await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        assert response.status_code == 400
        assert "limit" in response.json()["detail"].lower()


@pytest.mark.asyncio
class TestTransfers:
    """Tests for transfer transactions."""
    
    async def test_create_transfer(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test creating a transfer between accounts."""
        # Create destination account
        dest_account_data = {
            "account_type": "checking",
            "password": "DestPass123!"
        }
        dest_response = await client.post("/accounts/", headers=auth_headers, json=dest_account_data)
        dest_account = dest_response.json()
        
        # Deposit money to source account
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": 1000.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Transfer money
        transfer_data = {
            "origin_account_number": test_account["account_number"],
            "destination_account_number": dest_account["account_number"],
            "value": 500.00,
            "transaction_type": "transfer"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transfer_data)
        assert response.status_code == 201
        data = response.json()
        assert data["value"] == 500.00
        assert data["transaction_type"] == "transfer"
    
    async def test_transfer_without_destination_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test transfer without destination account fails."""
        transfer_data = {
            "origin_account_number": test_account["account_number"],
            "value": 100.00,
            "transaction_type": "transfer"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transfer_data)
        assert response.status_code == 400
        assert "destination" in response.json()["detail"].lower()
    
    async def test_transfer_to_nonexistent_account_fails(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test transfer to non-existent account fails."""
        # Deposit money first
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": 1000.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        # Try to transfer
        transfer_data = {
            "origin_account_number": test_account["account_number"],
            "destination_account_number": 9999999999,
            "value": 100.00,
            "transaction_type": "transfer"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transfer_data)
        assert response.status_code == 404
    
    async def test_transfer_insufficient_funds(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test transfer with insufficient funds fails."""
        # Create destination account
        dest_account_data = {
            "account_type": "checking",
            "password": "DestPass123!"
        }
        dest_response = await client.post("/accounts/", headers=auth_headers, json=dest_account_data)
        dest_account = dest_response.json()
        
        # Try to transfer without sufficient balance
        transfer_data = {
            "origin_account_number": test_account["account_number"],
            "destination_account_number": dest_account["account_number"],
            "value": 999999.00,
            "transaction_type": "transfer"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transfer_data)
        assert response.status_code == 400
        assert "insufficient" in response.json()["detail"].lower()


@pytest.mark.asyncio
class TestTransactionListing:
    """Tests for transaction listing endpoints."""
    
    async def test_list_my_transactions(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test listing logged-in user's transactions."""
        # Create a transaction
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": 250.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        
        # List transactions
        response = await client.get("/transactions/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1
    
    async def test_list_transactions_filter_by_type(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering transactions by type."""
        # Create deposits and withdrawals
        deposit_data = {
            "origin_account_number": test_account["account_number"],
            "value": 500.00,
            "transaction_type": "deposit"
        }
        await client.post("/transactions/", headers=auth_headers, json=deposit_data)
        
        withdrawal_data = {
            "origin_account_number": test_account["account_number"],
            "value": 100.00,
            "transaction_type": "withdrawal"
        }
        await client.post("/transactions/", headers=auth_headers, json=withdrawal_data)
        
        # Filter by deposit
        response = await client.get(
            "/transactions/me?transaction_type=deposit",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for transaction in data["items"]:
            assert transaction["transaction_type"] == "deposit"
    
    async def test_list_transactions_filter_by_value(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test filtering transactions by minimum value."""
        # Create transactions with different values
        for value in [100.00, 500.00, 1000.00]:
            transaction_data = {
                "origin_account_number": test_account["account_number"],
                "value": value,
                "transaction_type": "deposit"
            }
            await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        
        # Filter by value >= 500
        response = await client.get(
            "/transactions/me?value=500",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for transaction in data["items"]:
            assert transaction["value"] >= 500.00
    
    async def test_list_all_transactions_as_admin(self, client: AsyncClient, admin_headers: dict):
        """Test admin can list all transactions."""
        response = await client.get("/transactions/", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
    
    async def test_list_all_transactions_as_regular_user_fails(self, client: AsyncClient, auth_headers: dict):
        """Test regular user cannot list all transactions."""
        response = await client.get("/transactions/", headers=auth_headers)
        assert response.status_code == 403
    
    async def test_get_transaction_by_id(self, client: AsyncClient, test_account: dict, auth_headers: dict):
        """Test getting a specific transaction by ID."""
        # Create a transaction
        transaction_data = {
            "origin_account_number": test_account["account_number"],
            "value": 300.00,
            "transaction_type": "deposit"
        }
        create_response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        transaction = create_response.json()
        
        # Get transaction by ID
        response = await client.get(f"/transactions/{transaction['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction["id"]
        assert data["value"] == 300.00


@pytest.mark.asyncio
class TestTransactionPermissions:
    """Tests for transaction permission checks."""
    
    async def test_cannot_transact_on_other_users_account(self, client: AsyncClient, test_account: dict, test_admin: dict, auth_headers: dict):
        """Test user cannot make transactions on accounts they don't own."""
        # Create an account for admin
        admin_token_response = await client.post(
            "/auth/login",
            json={
                "user_number": test_admin["user_number"],
                "password": test_admin["password"]
            }
        )
        admin_token = admin_token_response.json()["access_token"]
        admin_auth_headers = {"Authorization": f"Bearer {admin_token}"}
        
        admin_account_data = {
            "account_type": "savings",
            "password": "AdminAccountPass123!"
        }
        admin_account_response = await client.post(
            "/accounts/",
            headers=admin_auth_headers,
            json=admin_account_data
        )
        admin_account = admin_account_response.json()
        
        # Try to deposit to admin's account with regular user token
        transaction_data = {
            "origin_account_number": admin_account["account_number"],
            "value": 500.00,
            "transaction_type": "deposit"
        }
        
        response = await client.post("/transactions/", headers=auth_headers, json=transaction_data)
        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

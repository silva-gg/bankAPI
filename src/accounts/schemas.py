"""
Account Pydantic Schemas

Defines validation and serialization schemas for bank account operations.
"""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import UUID5, Field, PositiveFloat, constr
from src.users.schemas import UserOut
from src.contrib.schemas import BaseSchema, OutMixin
from src.contrib.schemas import AccountType
from src.transactions.schemas import TransactionSummary

class Account(BaseSchema):
    """
    Base Schema for Account Entity
    
    Attributes:
        account_type: Type of account (savings or checking)
    """

    account_type: Annotated[
        AccountType,
        Field(
            description='Type of account (e.g., savings, checking)',
            example='savings',
            max_length=50
        )
    ]

  


class AccountIn(Account):
    """
    Input Schema for Creating Bank Account
    
    Used for POST requests to create new accounts.
    """

    password: Annotated[
        str,
        Field(
            description='Password for the account',
            example='SecurePass123!',
            min_length=8,
            max_length=128
        )
    ]


class AccountOut(Account, OutMixin):
    """
    Output Schema for Account
    
    Used for API responses. Includes account details without password.
    """
    account_number: Annotated[
        int,
        Field(
            description='Account number',
            example=1234567890,
            ge=1
        )
    ]

    owner: Annotated[
        UUID5,
        Field(
            description='UUID of the account owner',
            example='550e8400-e29b-41d4-a716-446655440000'
        )
    ]

    is_active: Annotated[
        bool,
        Field(
            description='Indicates if the account is active',
            example=True
        )
    ]
    
    created_at: Annotated[
        datetime,
        Field(
            description='Timestamp when the account was created',
            example='2023-01-01T12:00:00Z'
        )
    ]


class AccountUpdate(BaseSchema):
    """
    Update Schema for Account
    
    Used for PATCH requests. All fields are optional for partial updates.
    """
    password: Annotated[
        Optional[str],
        Field(
            None,
            description='New password for the account',
            min_length=8,
            max_length=255
        )
    ]

class AccountAdminUpdate(AccountUpdate):
    """
    Admin Update Schema for Account
    
    Allows admins to update withdrawal limits.
    """
    daily_withdrawal_limit: Annotated[
        Optional[int],
        Field(
            None,
            description='Daily limit for successful withdrawal attempts',
            ge=0
        )
    ]

    special_withdrawal_limit: Annotated[
        Optional[float],
        Field(
            None,
            description='Maximum amount allowed for special withdrawals',
            ge=0.0
        )
    ]

class AccountList(BaseSchema):
    """
    Simplified Schema for List Responses
    
    Used for GET /accounts endpoint. Includes only essential fields.
    """
    account_number: Annotated[
        int,
        Field(
            description='Account number',
            example=1234567890
        )
    ]

    account_type: Annotated[
        AccountType,
        Field(
            description='Type of account',
            example='savings'
        )
    ]

    balance: Annotated[
        float,
        Field(
            description='Current balance of the account',
            example=1500.75
        )
    ]

class AccountStatement(AccountOut):
    """
    Schema for Account Statement
    
    Extends AccountOut to include transaction history and current balance.
    """
    balance: Annotated[
        float,
        Field(
            description='Current balance of the account',
            example=1500.75
        )
    ]
    
    transactions: Annotated[
        list['TransactionSummary'],
        Field(
            description='List of transactions associated with the account'
        )
    ]


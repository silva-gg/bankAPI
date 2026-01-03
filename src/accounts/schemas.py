"""
Example Entity Pydantic Schemas

This file defines the data validation and serialization schemas using Pydantic.

Instructions for creating your own schemas:
1. Import BaseSchema and OutMixin from api.contrib.schemas
2. Create a base schema with all fields
3. Create Input schema (for POST requests) - inherits from base
4. Create Output schema (for responses) - inherits from base + OutMixin
5. Create Update schema (for PATCH requests) - all fields optional
6. Use Annotated with Field for validation and documentation

Pydantic Field parameters:
- description: Field description for API docs
- example: Example value for API docs
- max_length: Maximum string length
- min_length: Minimum string length
- ge: Greater than or equal (for numbers)
- le: Less than or equal (for numbers)
- gt: Greater than (for numbers)
- lt: Less than (for numbers)
- pattern: Regex pattern for strings

Common types:
- str: String
- int: Integer
- float: Float
- bool: Boolean
- datetime: DateTime
- UUID4: UUID
- Optional[type]: Optional field (can be None)
- list[type]: List of items
"""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import UUID5, Field, PositiveFloat, constr
from src.users.schemas import UserOut
from src.contrib.schemas import BaseSchema, OutMixin
from src.contrib.schemas import AccountType


class Account(BaseSchema):
    """
    Base Schema for Account Entity
    This schema includes all fields for the Account entity.

    Instructions:
    - Define all fields that exist in the database model
    - Use Annotated with Field for validation and documentation
    - This schema is inherited by Input, Output, and Update schemas
    
    Attributes:
        owner: Annotated[UUID5, Field(...)]
        owner_name: Annotated[str, Field(...)]
        account_number: Annotated[str, Field(...)]
        account_type: Annotated[str, Field(...)]
        balance: Annotated[float, Field(...)]
        is_active: Annotated[bool, Field(...)]
        created_at: Annotated[datetime, Field(...)]
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
    Input Schema for Creating Example Entity
    
    This schema is used for POST requests (creating new entities).
    It inherits all fields from the base schema.
    
    Instructions:
    - Add any fields that are required only on creation (e.g., password)
    - Remove any fields that shouldn't be settable by users (e.g., id, timestamps)
    - Keep fields that users should provide when creating
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
    Output Schema for Example Entity
    
    This schema is used for API responses (GET, POST, PATCH).
    It includes all fields from the base schema plus id and created_at from OutMixin.
    
    Instructions:
    - This automatically includes: id (UUID) and created_at (datetime)
    - Add any computed fields or relationships
    - Don't include sensitive fields (e.g., passwords)
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
    
    # Example: Add computed field
    # @property
    # def full_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"
    
    # Example: Add relationship
    # from api.categories.schemas import CategoryOut
    # category: Annotated[CategoryOut, Field(description='Related category')]


class AccountUpdate(BaseSchema):
    """
    Update Schema for Account Entity
    This schema is used for PATCH requests (updating existing entities).
    All fields are optional to allow partial updates.
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
    Update Schema for Account Entity
    This schema is used for PATCH requests (updating existing entities).
    All fields are optional to allow partial updates.
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
    
    This schema is used when returning lists of entities.
    It includes only essential fields to reduce response size.
    
    Instructions:
    - Include only the most important fields
    - Use this for GET /entities (list endpoint)
    - Keep response size small for better performance
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
    
    # Add id and created_at if needed
    # But typically you want to keep list responses lightweight

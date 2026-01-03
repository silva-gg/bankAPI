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

from typing import Annotated, Optional
from pydantic import UUID4, Field, PositiveFloat, constr
from src.contrib.schemas import BaseSchema, OutMixin,TransactionType


class Transaction(BaseSchema):
    """
    Base Example Entity Schema
    
    This schema defines all fields for the entity.
    It's used as a base for Input and Output schemas.
    
    Instructions:
    - Replace these fields with your actual entity fields
    - Use Annotated with Field for validation and documentation
    - Add validation rules as needed
    """
    value: Annotated[
        PositiveFloat,
        Field(
            description='Numeric value for the transaction (must be positive)',
            example=100.50,
            ge=0.0
        )
    ]

    transaction_type: Annotated[
        TransactionType,
        Field(
            description='Type of transaction (deposit or withdrawal)',
            example='deposit'
        )
    ]


class TransactionIn(Transaction):
    """
    Input Schema for Creating Example Entity
    
    This schema is used for POST requests (creating new entities).
    It inherits all fields from the base schema.
    
    Instructions:
    - Add any fields that are required only on creation (e.g., password)
    - Remove any fields that shouldn't be settable by users (e.g., id, timestamps)
    - Keep fields that users should provide when creating
    """
    origin_account_number: Annotated[
        int,
        Field(
            description='Account number associated with the transaction',
            example=1234567890
        )
    ]
    
    # Example: Add password field only for creation
    # password: Annotated[str, Field(description='User password', min_length=8)]


class TransactionOut(Transaction, OutMixin):
    """
    Output Schema for Example Entity
    
    This schema is used for API responses (GET, POST, PATCH).
    It includes all fields from the base schema plus id and created_at from OutMixin.
    
    Instructions:
    - This automatically includes: id (UUID) and created_at (datetime)
    - Add any computed fields or relationships
    - Don't include sensitive fields (e.g., passwords)
    """
    pass
    # Example: Add computed field
    # @property
    # def full_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"
    
    # Example: Add relationship
    # from api.categories.schemas import CategoryOut
    # category: Annotated[CategoryOut, Field(description='Related category')]


class TransactionList(BaseSchema):
    """
    Simplified Schema for List Responses
    
    This schema is used when returning lists of entities.
    It includes only essential fields to reduce response size.
    
    Instructions:
    - Include only the most important fields
    - Use this for GET /entities (list endpoint)
    - Keep response size small for better performance
    """
    
    value: Annotated[float, Field(description='Transaction value')]
    transaction_type: Annotated[TransactionType, Field(description='Type of transaction')]
    created_at: Annotated[
        Optional[str],
        Field(description='Timestamp when the transaction was created')
    ]
    origin_account_number: Annotated[
        int,
        Field(
            description='Account number associated with the transaction',
            example=1234567890
        )
    ]

"""
Transaction Pydantic Schemas

Defines validation and serialization schemas for transaction operations.
"""

from typing import Annotated, Optional
from pydantic import UUID4, Field, PositiveFloat, constr
from src.contrib.schemas import BaseSchema, OutMixin,TransactionType


class Transaction(BaseSchema):
    """
    Base Transaction Schema
    
    Defines fields for transaction operations.
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
    Input Schema for Creating Transaction
    
    Used for POST requests to create deposits or withdrawals.
    """
    origin_account_number: Annotated[
        int,
        Field(
            description='Account number associated with the transaction',
            example=1234567890
        )
    ]
    destination_account_number: Annotated[
        Optional[int],
        Field(
            None,
            description='Destination account number for transfers (optional)',
            example=9876543210
        )
    ]


class TransactionOut(Transaction, OutMixin):
    """
    Output Schema for Transaction
    
    Used for API responses. Includes transaction details with timestamps.
    """
    pass


class TransactionList(BaseSchema):
    """
    Simplified Schema for List Responses
    
    Used for GET /transactions endpoint.
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

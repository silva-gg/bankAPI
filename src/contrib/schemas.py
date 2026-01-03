"""
Base Pydantic Schemas

Provides base schema classes for request/response validation.
"""

from typing import Annotated
from pydantic import UUID4, BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class BaseSchema(PydanticBaseModel):
    """
    Base Pydantic schema for all entities
    
    Configuration:
    - extra='forbid': Reject any extra fields not defined in the schema
    - from_attributes=True: Allow creating schemas from ORM models
    """
    
    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class OutMixin(BaseSchema):
    """
    Mixin for output schemas that includes common response fields
    
    Fields:
    - id: UUID identifier
    - created_at: Timestamp of creation
    """
    
    id: Annotated[UUID4, Field(description='Unique identifier')]
    created_at: Annotated[datetime, Field(description='Creation timestamp')]


class PaginationParams(BaseSchema):
    """Schema for pagination parameters"""
    
    page: Annotated[int, Field(default=1, ge=1, description='Page number')]
    size: Annotated[int, Field(default=50, ge=1, le=100, description='Items per page')]


class MessageResponse(BaseSchema):
    """Generic message response schema"""
    
    message: Annotated[str, Field(description='Response message')]


class AccountType(str, Enum):
    """Account type enumeration"""
    SAVINGS = 'savings'
    CHECKING = 'checking'
    BUSINESS = 'business'


class TransactionType(str, Enum):
    """Transaction type enumeration"""
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
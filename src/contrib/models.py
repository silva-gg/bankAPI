"""
Base Database Models

Provides the base model class that all entity models inherit from.
"""

from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class BaseModel(DeclarativeBase):
    """
    Base model for all database entities
    
    Provides:
    - id: UUID field for unique identification across entities
    - DeclarativeBase: SQLAlchemy ORM base class
    """
    
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        unique=True,
        index=True,
    )

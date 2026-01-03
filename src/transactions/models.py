"""
Example Entity Database Models

This file defines the database schema for the example entity using SQLAlchemy ORM.

Instructions for creating your own models:
1. Import the BaseModel from api.contrib.models
2. Define your model class inheriting from BaseModel
3. Set the __tablename__ attribute (use plural, snake_case)
4. Define columns using Mapped and mapped_column
5. Add relationships if needed with foreign keys

Column types commonly used:
- Integer: For integer numbers
- String(length): For text with max length
- Float: For decimal numbers
- Boolean: For true/false values
- DateTime: For timestamps
- ForeignKey: For relationships

Example relationships:
- One-to-Many: Use relationship() with back_populates
- Many-to-One: Use ForeignKey and relationship()
- Many-to-Many: Create an association table

After creating/modifying models:
1. Run: alembic revision --autogenerate -m "Description of changes"
2. Run: alembic upgrade head
"""

from datetime import datetime, timezone
from uuid import UUID as UUIDType, uuid4
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.models import BaseModel
from src.contrib.schemas import TransactionType
from sqlalchemy import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.accounts.models import AccountModel

class TransactionModel(BaseModel):
    """
    Example Entity Database Model
    
    This is a template showing different field types and configurations.
    Replace this with your actual entity model.
    
    Attributes:
        pk_id: Primary key (auto-increment integer)
        name: Entity name (required, max 100 chars)
        description: Entity description (optional, text field)
        value: Numeric value (optional, float)
        is_active: Active status flag (default True)
        created_at: Creation timestamp (auto-set)
        
    Table name: example_entities
    """
    
    __tablename__ = 'transactions'
    
    # Primary Key - Auto-generated UUID field
    pk_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
        index=True,
        comment='Primary key'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment='Creation timestamp'
    )

    origin_account_number: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('accounts.account_number'),
        nullable=False,
        comment='Origin account number'
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment='Transaction value'
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        comment='Type of transaction (e.g., deposit, withdrawal)'
    )

    account: Mapped['AccountModel'] = relationship(
        back_populates="transactions",
        lazy='selectin'
    )
    
    # Examples of other field types:
    
    # Unique field:
    # code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Field with check constraint:
    # age: Mapped[int] = mapped_column(Integer, CheckConstraint('age >= 0'), nullable=False)
    
    # Enum field:
    # from enum import Enum
    # class Status(str, Enum):
    #     ACTIVE = "active"
    #     INACTIVE = "inactive"
    # status: Mapped[str] = mapped_column(String(20), default=Status.ACTIVE, nullable=False)
    
    # Foreign Key example (Many-to-One):
    # category_id: Mapped[int] = mapped_column(ForeignKey("categories.pk_id"), nullable=False)
    # category: Mapped['CategoryModel'] = relationship(back_populates="examples", lazy='selectin')
    
    # One-to-Many relationship example (in parent model):
    # examples: Mapped[list['ExampleEntityModel']] = relationship(back_populates="category", lazy='selectin')
    
    def __repr__(self) -> str:
        """String representation of the model"""
        return f"<TransactionModel(id={self.pk_id}, origin_account={self.origin_account}, value={self.value}, type={self.transaction_type})>"

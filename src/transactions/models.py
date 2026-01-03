"""
Transaction Database Models

Defines the database schema for financial transactions.
"""

from datetime import datetime, timezone
from uuid import UUID as UUIDType, uuid4
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.models import BaseModel
from src.contrib.schemas import TransactionType
from sqlalchemy import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.accounts.models import AccountModel

class TransactionModel(BaseModel):
    """
    Transaction Database Model
    
    Represents financial transactions (deposits and withdrawals).
    
    Attributes:
        pk_id: Primary key (UUID)
        created_at: Transaction timestamp
        origin_account_number: Account involved in transaction
        value: Transaction amount
        transaction_type: Type (deposit or withdrawal)
        account: Related account
    """
    
    __tablename__ = 'transactions'
    
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

    destination_account_number: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('accounts.account_number'),
        nullable=True,
        comment='Destination account number (for transfers, optional when applicable)'
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
        foreign_keys=[origin_account_number],
        lazy='selectin'
    )
    
    def __repr__(self) -> str:
        """String representation of the model"""
        return f"<Transaction(id={self.pk_id}, account={self.origin_account_number}, value={self.value}, type={self.transaction_type})>"

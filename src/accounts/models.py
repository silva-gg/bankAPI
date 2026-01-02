from datetime import datetime
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.models import BaseModel, AccountType
from uuid import UUID as UUIDType, uuid4, uuid5
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.models import UserModel


class AccountModel(BaseModel):
    """
    Account Database Model
    
    Data for bank accounts.
    
    Attributes:
        pk_id: Primary key (auto-increment integer)
        owner: UUID5 of the account owner (foreign key to UserModel)
        owner_name: Name of the account owner (required, max 100 chars)
        account_number: Account number (required, max 20 chars)
        account_type: Type of account (e.g., savings, checking)
        balance: Current balance (float)
        is_active: Active status flag (default True)
        created_at: Creation timestamp (auto-set)

        
    Table name: accounts
    """
    
    __tablename__ = 'accounts'
    
    # Primary Key - Auto-incrementing integer
    account_number: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='Primary key'
    )

    owner: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.uuid5'),
        nullable=False,
    )
    owner_user: Mapped['UserModel'] = relationship(
        back_populates="accounts",
        lazy='selectin'
    )
    account_type: Mapped[AccountType] = mapped_column(
        String(50),
        nullable=False,
        comment='Account type'
    )
    balance: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment='Current balance'
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment='Active status'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Creation timestamp'
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Hashed account password'
    )

    def __repr__(self) -> str:
        """String representation of the model"""
        return f"<Account(id={self.account_number}, owner_name='{self.owner_name}')>"

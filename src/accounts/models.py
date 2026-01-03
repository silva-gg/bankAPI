from datetime import datetime, timezone
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Float, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.schemas import AccountType
from src.contrib.models import BaseModel
from uuid import UUID as UUIDType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.models import UserModel
    from src.transactions.models import TransactionModel


class AccountModel(BaseModel):
    """
    Account Database Model
    
    Represents bank accounts with balance tracking and withdrawal limits.
    
    Attributes:
        account_number: Primary key (auto-increment integer)
        owner: UUID5 of the account owner (foreign key to UserModel)
        account_type: Type of account (savings or checking)
        balance: Current balance
        is_active: Active status flag
        created_at: Creation timestamp
        hashed_password: Hashed account password
        daily_withdrawal_limit: Daily withdrawal attempt limit
        special_withdrawal_limit: Maximum special withdrawal amount
        used_special_withdrawal: Amount used from special withdrawal
        transactions: Related transactions
    """
    
    __tablename__ = 'accounts'
    
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
        Enum(AccountType, values_callable=lambda x: [e.value for e in x]),
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
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment='Creation timestamp'
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Hashed account password'
    )

    daily_withdrawal_limit: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
        comment='Daily limit for successful withdrawal attempts'
    )

    special_withdrawal_limit: Mapped[float] = mapped_column(
        Float,
        default=500.0,
        nullable=False,
        comment='Maximum amount allowed for special withdrawals'
    )

    used_special_withdrawal: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment='Amount already used from special withdrawal limit'
    )

    transactions: Mapped[list['TransactionModel']] = relationship(
        back_populates="account",
        lazy='selectin'
    )

    def __repr__(self) -> str:
        """String representation of the model"""
        return f"<Account(number={self.account_number}, type={self.account_type}, balance={self.balance})>"

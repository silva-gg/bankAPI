"""
User Database Models

This file defines the database schema for users and authentication.
"""

from datetime import datetime
from uuid import UUID as UUIDType, uuid5,  NAMESPACE_DNS
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.models import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.accounts.models import AccountModel
class UserModel(BaseModel):
    """
    User Model for Authentication
    
    Stores user credentials and authentication information.
    
    Attributes:
        uuid5: Unique user identifier - Primary Key
        username: Unique username
        email: User email address
        hashed_password: Bcrypt hashed password
        is_active: Whether user account is active
        is_superuser: Whether user has admin privileges
        created_at: Account creation timestamp
    """
    
    __tablename__ = 'users'

    uuid5: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        comment='uuid5 unique user identifier'
    )
    
    user_fullname: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default='John Doe',
        comment='User full name'
    )
    
    user_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        comment='Governmental ID number'
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment='User email address'
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Hashed user password'
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment='Account active status'
    )
    
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment='Admin privileges'
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Account creation timestamp'
    )

    accounts: Mapped[List['AccountModel']] = relationship(
        back_populates="owner_user",
        lazy='selectin'
    )

    @classmethod
    def generate_uuid_from_id_number(cls, id_number: int) -> UUIDType:
        """Generate deterministic UUID v5 from governmental ID number"""
        return uuid5(NAMESPACE_DNS, str(id_number))
    
    def __repr__(self) -> str:
        return f"<User(id={self.uuid5}, fullname='{self.user_fullname}', email='{self.email}')>"

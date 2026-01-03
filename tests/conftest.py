"""
Pytest Configuration and Fixtures

This module contains shared fixtures for all test modules.
"""

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.main import app
from src.contrib.models import BaseModel as Base
from src.configs.database import get_session as get_db_session
from src.users.auth import create_access_token


# Test database URL - using environment variable or default
TEST_DB_URL = os.getenv(
    "DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/bankapi_test"
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DB_URL,
        echo=False,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database tables and provide a database session for each test.
    Tables are created before each test and dropped after.
    """
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()
    
    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing API endpoints.
    Overrides the database session dependency.
    """
    
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db: AsyncSession) -> dict:
    """Create a test user and return user data with password."""
    from src.users.models import UserModel
    from src.users.auth import hash_password
    from datetime import datetime, timezone
    
    user_data = {
        "user_number": "123456789",
        "user_fullname": "Test User",
        "email": "testuser@example.com",
        "password": "TestPass123!",
    }
    
    user = UserModel(
        uuid5=UserModel.generate_uuid_from_id_number(user_data["user_number"]),
        user_number=user_data["user_number"],
        user_fullname=user_data["user_fullname"],
        email=user_data["email"],
        hashed_password=hash_password(user_data["password"]),
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc)
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    return {**user_data, "uuid5": str(user.uuid5)}


@pytest.fixture
async def test_admin(test_db: AsyncSession) -> dict:
    """Create a test admin user and return user data with password."""
    from src.users.models import UserModel
    from src.users.auth import hash_password
    from datetime import datetime, timezone
    
    admin_data = {
        "user_number": "987654321",
        "user_fullname": "Admin User",
        "email": "admin@example.com",
        "password": "AdminPass123!",
    }
    
    admin = UserModel(
        uuid5=UserModel.generate_uuid_from_id_number(admin_data["user_number"]),
        user_number=admin_data["user_number"],
        user_fullname=admin_data["user_fullname"],
        email=admin_data["email"],
        hashed_password=hash_password(admin_data["password"]),
        is_active=True,
        is_superuser=True,
        created_at=datetime.now(timezone.utc)
    )
    
    test_db.add(admin)
    await test_db.commit()
    await test_db.refresh(admin)
    
    return {**admin_data, "uuid5": str(admin.uuid5)}


@pytest.fixture
def user_token(test_user: dict) -> str:
    """Generate JWT token for test user."""
    from datetime import timedelta
    from src.configs.settings import settings
    
    access_token = create_access_token(
        data={"sub": test_user["user_number"]},
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    )
    return access_token


@pytest.fixture
def admin_token(test_admin: dict) -> str:
    """Generate JWT token for test admin."""
    from datetime import timedelta
    from src.configs.settings import settings
    
    access_token = create_access_token(
        data={"sub": test_admin["user_number"]},
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    )
    return access_token


@pytest.fixture
def auth_headers(user_token: str) -> dict:
    """Return authorization headers for test user."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    """Return authorization headers for admin user."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
async def test_account(test_db: AsyncSession, test_user: dict) -> dict:
    """Create a test bank account and return account data."""
    from src.accounts.models import AccountModel
    from src.users.auth import hash_password
    from datetime import datetime, timezone
    
    account_data = {
        "account_type": "savings",
        "password": "AccountPass123!",
    }
    
    account = AccountModel(
        owner=test_user["uuid5"],
        account_type=account_data["account_type"],
        hashed_password=hash_password(account_data["password"]),
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    
    test_db.add(account)
    await test_db.commit()
    await test_db.refresh(account)
    
    return {
        **account_data,
        "account_number": account.account_number,
        "id": str(account.id),
        "balance": account.balance,
    }

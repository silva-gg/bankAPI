# BankAPI Test Suite

This directory contains comprehensive integration tests for the BankAPI application.

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_health.py` - Health check endpoint tests
- `test_auth.py` - Authentication and user management tests
- `test_accounts.py` - Bank account management tests
- `test_transactions.py` - Transaction (deposit, withdrawal, transfer) tests

## Running Tests Locally

### Prerequisites

1. PostgreSQL database running (or use Docker)
2. Python 3.11+ installed
3. Dependencies installed

### Setup

1. Install dependencies using Poetry:
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install all dependencies including dev dependencies
poetry install --with dev

# Activate the virtual environment (optional, commands can also use 'poetry run')
poetry shell
```

2. Set up test database:
```bash
# Using Docker
docker run --name bankapi-test-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=bankapi_test -p 5432:5432 -d postgres:15

# Or use docker-compose
docker-compose up -d
```

3. Configure environment variables:
```bash
export DB_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bankapi_test"
export SECRET_KEY="test-secret-key-for-testing"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_DAYS="30"
```

### Run Tests

```bash
# Run all tests (using poetry)
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_auth.py -v

# Run specific test class
poetry run pytest tests/test_auth.py::TestUserRegistration -v

# Run specific test
poetry run pytest tests/test_auth.py::TestUserRegistration::test_register_user_success -v
```

Alternatively, if you're inside the Poetry shell (after running `poetry shell`):
```bash
# All commands can be run without 'poetry run' prefix
pytest
pytest --cov=src --cov-report=html
```

## Test Coverage

The test suite covers:

### Authentication (`test_auth.py`)
- ✅ User registration (success, duplicates, validation)
- ✅ User login (success, wrong password, non-existent user)
- ✅ Current user operations (get, update email, fullname, password)
- ✅ Admin operations (list users, delete users, permissions)

### Accounts (`test_accounts.py`)
- ✅ Account creation (savings, checking, business)
- ✅ Account listing (my accounts, all accounts, filters)
- ✅ Account retrieval by ID
- ✅ Account updates
- ✅ Account deletion
- ✅ Pagination

### Transactions (`test_transactions.py`)
- ✅ Deposits (success, validation, balance updates)
- ✅ Withdrawals (success, insufficient funds, daily limits)
- ✅ Transfers (success, validation, insufficient funds)
- ✅ Transaction listing (filters, pagination)
- ✅ Permission checks

### Health (`test_health.py`)
- ✅ Root endpoint
- ✅ Health check endpoint

## CI/CD Integration

Tests are automatically run on every commit via GitHub Actions. See `.github/workflows/ci-cd.yml` for the workflow configuration.

### GitHub Actions Workflow

The workflow includes:
- PostgreSQL service container
- Python environment setup
- Dependency installation
- Database migrations
- Linting with Ruff
- Test execution with coverage reporting
- Security scanning with Safety and Bandit

### Required Secrets

The following secrets should be configured in your GitHub repository:

- `SECRET_KEY` - JWT secret key for token generation
- `CODECOV_TOKEN` (optional) - For coverage reporting to Codecov

## Test Fixtures

Available fixtures in `conftest.py`:

- `client` - Async HTTP client for making requests
- `test_db` - Test database session
- `test_user` - Regular user with credentials
- `test_admin` - Admin user with credentials
- `user_token` - JWT token for test user
- `admin_token` - JWT token for admin user
- `auth_headers` - Authorization headers for test user
- `admin_headers` - Authorization headers for admin user
- `test_account` - Bank account for test user

## Writing New Tests

Example test structure:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_my_endpoint(client: AsyncClient, auth_headers: dict):
    """Test description"""
    response = await client.get("/my-endpoint", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

## Troubleshooting

### Database Connection Issues

If tests fail with database connection errors:

1. Check PostgreSQL is running: `pg_isready -h localhost -p 5432`
2. Verify DB_URL environment variable
3. Ensure test database exists: `createdb bankapi_test`

### Import Errors

If you get import errors:

1. Ensure you're in the project root directory
2. Install all dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.11+)

### Test Failures

If tests fail unexpectedly:

1. Check database is clean (tests create/drop tables automatically)
2. Verify environment variables are set correctly
3. Run tests with verbose output: `pytest -vv`
4. Check for port conflicts (default PostgreSQL port is 5432)

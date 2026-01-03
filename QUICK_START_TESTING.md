# Quick Start Guide for Testing

This is a quick reference for running tests. For detailed information, see `tests/README.md`.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx email-validator
```

## Setup Database

```bash
# Option 1: Docker
docker run --name bankapi-test-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bankapi_test \
  -p 5432:5432 -d postgres:15

# Option 2: Local PostgreSQL
createdb bankapi_test
```

## Environment Variables

```bash
export DB_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bankapi_test"
export SECRET_KEY="test-secret-key-for-testing"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_DAYS="30"
```

Or create a `.env` file:
```env
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bankapi_test
SECRET_KEY=test-secret-key-for-testing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
```

## Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific file
pytest tests/test_auth.py -v

# Watch mode (requires pytest-watch)
ptw
```

## Common Commands

```bash
# Run only fast tests
pytest -m "not slow"

# Run with detailed output
pytest -vv

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Collect tests without running
pytest --collect-only
```

## GitHub Actions

To run tests in CI:

1. Add `SECRET_KEY` to GitHub repository secrets
2. Push to main/master/develop branch or create PR
3. View results in Actions tab

## Test Structure

- 63 total tests
- 4 test files covering all endpoints
- Multiple scenarios per endpoint (success, errors, permissions)

## Coverage

After running with coverage:
```bash
# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Check database exists
psql -l | grep bankapi_test
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Tests Hang
- Check for database locks
- Restart PostgreSQL
- Clear pytest cache: `rm -rf .pytest_cache`

## Next Steps

- Read `tests/README.md` for detailed documentation
- Check `TESTING_IMPLEMENTATION.md` for implementation details
- Review `.github/SETUP_GUIDE.md` for CI/CD setup

---

**Need help?** Open an issue on GitHub or check the full documentation.

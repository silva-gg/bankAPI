"""
API Router Configuration

This file aggregates all entity routers and registers them with the main API router.
Add your new entity routers here following the pattern shown in the example.

Instructions:
1. Import your entity controller's router
2. Include it in the api_router with appropriate prefix and tags
3. The prefix should be plural (e.g., '/users', '/products')
4. Tags are used for grouping in the API documentation
"""

from fastapi import APIRouter
from src.users.controller import router as users_router
from src.accounts.controller import router as accounts_router
from src.transactions.controller import router as transactions_router
# Create main API router
api_router = APIRouter()

# Register authentication/user router
api_router.include_router(
    users_router,
    prefix='/auth',
    tags=['authentication']
)

# Register entity routers

api_router.include_router(
    accounts_router, 
    prefix='/accounts', 
    tags=['accounts']
)

# Transaction router
api_router.include_router(
    transactions_router,
    prefix='/transactions',
    tags=['transactions']
)

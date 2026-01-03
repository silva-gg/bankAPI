"""
API Router Configuration

Aggregates all entity routers and registers them with the main API router.
"""

from fastapi import APIRouter
from src.users.controller import router as users_router
from src.accounts.controller import router as accounts_router
from src.transactions.controller import router as transactions_router

api_router = APIRouter()

api_router.include_router(
    users_router,
    prefix='/auth',
    tags=['🔑 Authentication']
)

api_router.include_router(
    accounts_router, 
    prefix='/accounts', 
    tags=['🏦 Accounts']
)

api_router.include_router(
    transactions_router,
    prefix='/transactions',
    tags=['💸 Transactions']
)

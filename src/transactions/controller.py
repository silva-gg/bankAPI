"""
Example Entity API Controller

This file defines the API endpoints (routes) for the example entity.
It implements CRUD operations: Create, Read, Update, Delete.

Instructions for creating your own controller:
1. Import necessary modules and your schemas/models
2. Create a router instance
3. Implement endpoints following REST conventions:
   - POST /   : Create new entity
   - GET /    : List all entities (with pagination)
   - GET /{id}: Get single entity by ID
   - PATCH /{id}: Update entity
   - DELETE /{id}: Delete entity
4. Use proper HTTP status codes
5. Handle exceptions appropriately
6. Add query parameters for filtering
7. Document endpoints with summary and description

HTTP Status Codes:
- 200 OK: Successful GET request
- 201 Created: Successful POST request
- 204 No Content: Successful DELETE request
- 400 Bad Request: Invalid input
- 404 Not Found: Resource not found
- 409 Conflict: Duplicate resource
- 500 Internal Server Error: Server error

Error Handling:
- Use HTTPException for expected errors
- Catch IntegrityError for database constraint violations
- Log unexpected errors
"""

from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from src.accounts.models import AccountModel
from src.contrib.schemas import TransactionType
from src.contrib.dependencies import DatabaseDependency, CurrentUser
from src.contrib.dependencies import RequireAdmin
from .schemas import (
    TransactionIn,
    TransactionOut,
    TransactionList
)
from .models import TransactionModel


# Create router instance
# This will be registered in api/routers.py
router = APIRouter()


# Note: This template uses Basic Auth for simplicity.
# You can also use JWT auth by importing CurrentUser instead:
# from api.contrib.dependencies import CurrentUser
# Then use CurrentUser in your endpoints instead of CurrentUser


@router.post(
    '/',
    summary='Register a new transaction',
    description='Register a new transaction with the provided data (requires authentication)',
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut
)
async def register_transaction(
    db_session: DatabaseDependency,
    current_user: CurrentUser, # JWT auth
    transaction_in: TransactionIn = Body(
        ...,
        description='Transaction data to create'
    )
):
    """
    Create a new example entity
    
    Requires HTTP Basic Authentication.
    
    Args:
        db_session: Database session (injected)
        current_user: Current authenticated user (injected)
        entity_in: Input data for the new entity
        
    Returns:
        ExampleEntityOut: Created entity with id and created_at
        
    Raises:
        HTTPException 401: If authentication fails
        HTTPException 409: If entity already exists (duplicate)
        HTTPException 500: If database error occurs
        
    Example with curl:
        curl -u username:password -X POST http://localhost:8000/examples \
          -H "Content-Type: application/json" \
          -d '{"name": "Example Item", "value": 99.99, "is_active": true}'
    """
    try:
        # Create output schema with UUID and timestamp
        transaction_out = TransactionOut(
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            **transaction_in.model_dump()
        )
        
        # Create database model from output schema
        transaction_model = TransactionModel(**transaction_out.model_dump())
        
        # Set necessary values to validate the transaction
        value = transaction_in.value
        transaction_type = transaction_in.transaction_type
        account_model = await db_session.get(
            AccountModel,
            transaction_in.origin_account_number
        )
        account_withdrawals_today = await select(TransactionModel).filter(
            TransactionModel.origin_account_number == transaction_in.origin_account_number,
            TransactionModel.transaction_type == TransactionType.WITHDRAWAL,
            TransactionModel.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        )
        withdraw_limit = account_model.daily_withdrawal_limit
        special_withdraw_limit = account_model.special_withdrawal_limit
        balance = account_model.balance
        used_special_withdraw = account_model.used_special_withdrawal
        if not account_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Account with number {transaction_in.origin_account_number} not found'
            )
        elif account_model.owner != current_user.uuid5 and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to perform transactions on this account'
            )
        elif transaction_type == TransactionType.DEPOSIT:
            # Deposits always succeed because of Pydantic validation
            return transaction_out
        elif transaction_type == TransactionType.WITHDRAWAL:
            # Check daily withdrawal limit
            result = await db_session.execute(account_withdrawals_today)
            withdrawals_today = result.scalars().all()
            if len(withdrawals_today) >= withdraw_limit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Daily withdrawal limit exceeded'
                )
            # Check sufficient balance including special withdrawal limit
            available_balance = balance + (special_withdraw_limit - used_special_withdraw)
            if value > available_balance:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Insufficient funds for this withdrawal'
                )
            # Update used special withdrawal if necessary
            if value > balance:
                account_model.used_special_withdrawal += (value - balance)
                db_session.add(account_model)
                await db_session.commit()
                return transaction_out
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Transaction in constraint violation: {str(e)}'
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while registering the transaction: {str(e)}'
        )

@router.get(
    '/me',
    summary='List all logged user\'s transactions',
    description='Retrieves a paginated list of all transactions with optional filtering',
    status_code=status.HTTP_200_OK,
    response_model=Page[TransactionOut],
)
async def get_all_transactions(
    db_session: DatabaseDependency,
    current_user: CurrentUser,  # JWT auth
    value: Optional[float] = Query(
        None,
        description='Filter by transaction value - greater than or equal to'
    ),
    transaction_type: Optional[TransactionType] = Query(
        None,
        description='Filter by transaction type (deposit or withdrawal)'
    ),
) -> Page[TransactionOut]:
    """
    Get all example entities with optional filters
    
    Args:
        db_session: Database session (injected)
        name: Optional name filter (partial match)
        is_active: Optional active status filter
        
    Returns:
        Page[ExampleEntityOut]: Paginated list of entities
        
    Example:
        GET /examples?name=test&is_active=true&page=1&size=10
    """
    # Start with base query
    query = select(TransactionModel).filter(TransactionModel.origin_account.in_(
        select(AccountModel.id).filter(AccountModel.owner == current_user.uuid5)
        ))
    
    # Apply filters if provided
    if value is not None:
        query = query.filter(TransactionModel.value >= value)
    
    if transaction_type is not None:
        query = query.filter(TransactionModel.transaction_type == transaction_type)
    
    # Add ordering
    query = query.order_by(TransactionModel.created_at.desc())
    
    # Execute query
    result = await db_session.execute(query)
    transactions = result.scalars().all()
    
    # Convert to output schemas and paginate
    return paginate([
        TransactionOut.model_validate(transaction)
        for transaction in transactions
    ])

@router.get(
    '/',
    summary='List all transactions (Admin only)',
    description='Retrieves a paginated list of all transactions with optional filtering',
    status_code=status.HTTP_200_OK,
    response_model=Page[TransactionOut],
)
async def get_all_transactions(
    db_session: DatabaseDependency,
    admin: RequireAdmin,  # Requires admin privileges
    value: Optional[float] = Query(
        None,
        description='Filter by transaction value - greater than or equal to'
    ),
    transaction_type: Optional[TransactionType] = Query(
        None,
        description='Filter by transaction type (deposit or withdrawal)'
    ),
) -> Page[TransactionOut]:
    """
    Get all example entities with optional filters
    
    Args:
        db_session: Database session (injected)
        name: Optional name filter (partial match)
        is_active: Optional active status filter
        
    Returns:
        Page[ExampleEntityOut]: Paginated list of entities
        
    Example:
        GET /examples?name=test&is_active=true&page=1&size=10
    """
    # Start with base query
    query = select(TransactionModel)
    
    # Apply filters if provided
    if value is not None:
        query = query.filter(TransactionModel.value >= value)
    
    if transaction_type is not None:
        query = query.filter(TransactionModel.transaction_type == transaction_type)
    
    # Add ordering
    query = query.order_by(TransactionModel.created_at.desc())
    
    # Execute query
    result = await db_session.execute(query)
    transactions = result.scalars().all()
    
    # Convert to output schemas and paginate
    return paginate([
        TransactionOut.model_validate(transaction)
        for transaction in transactions
    ])


@router.get(
    '/{entity_id}',
    summary='Get transaction by ID',
    description='Retrieves a single transaction by its UUID',
    status_code=status.HTTP_200_OK,
    response_model=TransactionOut
)
async def get_transaction_by_id(
    transaction_id: UUID4,
    db_session: DatabaseDependency
):
    """
    Get a single example entity by ID
    
    Args:
        entity_id: UUID of the entity
        db_session: Database session (injected)
        
    Returns:
        ExampleEntityOut: Entity data
        
    Raises:
        HTTPException 404: If entity not found
        
    Example:
        GET /examples/550e8400-e29b-41d4-a716-446655440000
    """
    # Query for entity by UUID
    result = await db_session.execute(
        select(TransactionModel).filter_by(id=transaction_id)
    )
    transaction = result.scalars().first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Transaction with id {transaction_id} not found'
        )
    
    return TransactionOut.model_validate(transaction)



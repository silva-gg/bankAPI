"""
Account API Controller

Provides endpoints for bank account management including creation, retrieval, and updates.
"""

from datetime import datetime, timezone
from uuid import uuid4, uuid5
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate
from src.contrib.schemas import AccountType
from src.contrib.dependencies import DatabaseDependency, CurrentUser, RequireAdmin
from src.users.auth import hash_password
from .schemas import (
    AccountIn,
    AccountOut,
    AccountUpdate,
    AccountList
)
from .models import AccountModel


router = APIRouter()


@router.post(
    '/',
    summary='Create a new Account',
    description='Creates a new account with the provided data (requires authentication)',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountOut
)
async def create_account(
    db_session: DatabaseDependency,
    current_user: CurrentUser,  # Requires JWT Authentication
    account_in: AccountIn = Body(
        ...,
        description='Account data to create'
    )
) -> AccountOut:
    """
    Create a new bank account for the authenticated user
    
    Args:
        db_session: Database session (injected)
        current_user: Current authenticated user (injected)
        account_in: Account creation data including type and password
        
    Returns:
        AccountOut: Created account information
        
    Raises:
        HTTPException 401: If authentication fails
        HTTPException 409: If account creation fails due to constraints
        HTTPException 500: If database error occurs
    """
    try:
        # Get authenticated user ID
        loggedin_user_id = current_user.uuid5
        
        # Create account model
        account_data = account_in.model_dump(exclude={'password'})
        account_model = AccountModel(
            owner=loggedin_user_id,
            created_at=datetime.now(timezone.utc),
            is_active=True,
            hashed_password=hash_password(account_in.password),
            **account_data
        )
        
        db_session.add(account_model)
        await db_session.commit()
        await db_session.refresh(account_model)
        
        return AccountOut.model_validate(account_model)
        
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Account already exists or constraint violation: {str(e)}'
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while creating the account: {str(e)}'
        )


@router.get(
    '/me',
    summary='List all logged user\'s accounts',
    description='Retrieves a paginated list of all accounts owned by the logged-in user with optional filtering',
    status_code=status.HTTP_200_OK,
    response_model=Page[AccountList],
)
async def get_all_my_accounts(
    db_session: DatabaseDependency,
    current_user: CurrentUser,
    is_active: Optional[bool] = Query(
        None,
        description='Filter by active status'
    ),
    account_type: Optional[AccountType] = Query(
        None,
        description='Filter by account type (exact match)',
        examples='savings'
    )

) -> Page[AccountList]:
    """
    Get all example entities with optional filters
    
    Args:
        db_session: Database session (injected)
        name: Optional name filter (partial match)
        is_active: Optional active status filter
        
    Returns:
        Page[AccountOut]: Paginated list of entities
        
    Example:
        GET /examples?name=test&is_active=true&page=1&size=10
    """
    # Start with base query
    query = select(AccountModel).where(AccountModel.owner == current_user.uuid5)
    
    # Apply filters if provided
    
    if is_active is not None:
        query = query.filter(AccountModel.is_active == is_active)
    
    if account_type:
        query = query.filter(AccountModel.account_type == account_type)
    # Add ordering
    query = query.order_by(AccountModel.created_at.desc())
    
    # Execute query
    result = await db_session.execute(query)
    entities = result.scalars().all()
    
    # Convert to output schemas and paginate
    return paginate([
        AccountList.model_validate(entity)
        for entity in entities
    ])


@router.get(
    '/',
    summary='List all accounts (Admin only)',
    description='Retrieves a paginated list of all accounts with optional single filtering - choose one filter at a time',
    status_code=status.HTTP_200_OK,
    response_model=Page[AccountOut],
)
async def get_all_accounts(
    db_session: DatabaseDependency,
    admin: RequireAdmin,
    owner_uuid: Optional[str] = Query(
        None,
        description='Filter by owner UUID (case-insensitive partial match)',
        examples='550e8400-e29b-41d4-a716-446655440000'
    ),
    is_active: Optional[bool] = Query(
        None,
        description='Filter by active status'
    ),
    owner_number: Optional[str] = Query(
        None,
        description='Filter by owner user number - Governmental ID number (exact match)',
        examples='123456789'
    )

) -> Page[AccountOut]:
    """
    Get all example entities with optional filters
    
    Args:
        db_session: Database session (injected)
        name: Optional name filter (partial match)
        is_active: Optional active status filter
        
    Returns:
        Page[AccountOut]: Paginated list of entities
        
    Example:
        GET /examples?name=test&is_active=true&page=1&size=10
    """
    # Start with base query
    query = select(AccountModel)
    
    # Apply filters if provided
    if owner_uuid:
        try:
            from uuid import UUID
            owner_uuid_obj = UUID(owner_uuid)
            query = query.filter(AccountModel.owner == owner_uuid_obj)
        except ValueError:
            # Invalid UUID format, skip filter
            pass
    
    if is_active is not None:
        query = query.filter(AccountModel.is_active == is_active)
    
    if owner_number:
        from src.users.models import UserModel
        query = query.join(UserModel, AccountModel.owner == UserModel.uuid5).filter(
            UserModel.user_number == owner_number
        )
    # Add ordering
    query = query.order_by(AccountModel.created_at.desc())
    
    # Execute query
    result = await db_session.execute(query)
    entities = result.scalars().all()
    
    # Convert to output schemas and paginate
    return paginate([
        AccountOut.model_validate(entity)
        for entity in entities
    ])

@router.get(
    '/{account_id}',
    summary='Get account by ID (Admin only)',
    description='Retrieves any single account by its UUID',
    status_code=status.HTTP_200_OK,
    response_model=AccountOut
)
async def get_account_by_id(
    account_id: UUID4,
    admin: RequireAdmin,  # Requires Admin JWT Authentication
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
        select(AccountModel).filter_by(id=account_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {account_id} not found'
        )
    
    return AccountOut.model_validate(entity)


@router.patch(
    '/{account_id}',
    summary='Update account (Admin only)',
    description='Updates an existing account with partial data (requires authentication)',
    status_code=status.HTTP_200_OK,
    response_model=AccountOut
)
async def update_account(
    account_id: UUID4,
    db_session: DatabaseDependency,
    admin: RequireAdmin,  # Requires Admin JWT Authentication
    entity_update: AccountUpdate = Body(
        ...,
        description='Fields to update (all optional)'
    )
):
    """
    Update an existing example entity
    
    Args:
        entity_id: UUID of the entity to update
        db_session: Database session (injected)
        entity_update: Fields to update
        
    Returns:
        ExampleEntityOut: Updated entity data
        
    Raises:
        HTTPException 404: If entity not found
        HTTPException 500: If database error occurs
        
    Example request body:
        {
            "name": "Updated Name",
            "is_active": false
        }
    """
    # Get existing entity
    result = await db_session.execute(
        select(AccountModel).filter_by(id=account_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {account_id} not found'
        )
    
    try:
        # Update only provided fields
        update_data = entity_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(entity, field, value)
        
        # Commit changes
        await db_session.commit()
        await db_session.refresh(entity)
        
        return AccountOut.model_validate(entity)
        
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Update violates constraint: {str(e)}'
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while updating the entity: {str(e)}'
        )


@router.delete(
    '/{account_id}',
    summary='Delete Account',
    description='Deletes an account by its UUID (requires authentication)',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(
    account_id: UUID4,
    db_session: DatabaseDependency,
    admin: RequireAdmin  # Requires Admin JWT Authentication
):
    """
    Delete an example entity
    
    Args:
        entity_id: UUID of the entity to delete
        db_session: Database session (injected)
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: If entity not found
        HTTPException 500: If database error occurs
        
    Example:
        DELETE /examples/550e8400-e29b-41d4-a716-446655440000
    """
    # Get existing entity
    result = await db_session.execute(
        select(AccountModel).filter_by(id=account_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {account_id} not found'
        )
    
    try:
        # Delete entity
        await db_session.delete(entity)
        await db_session.commit()
        
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while deleting the entity: {str(e)}'
        )


# Additional endpoint examples:

# Count entities
# @router.get('/count', response_model=dict)
# async def count_entities(db_session: DatabaseDependency):
#     """Get total count of entities"""
#     from sqlalchemy import func
#     result = await db_session.execute(
#         select(func.count()).select_from(ExampleEntityModel)
#     )
#     count = result.scalar()
#     return {'count': count}


# Bulk create
# @router.post('/bulk', response_model=list[ExampleEntityOut])
# async def bulk_create(
#     db_session: DatabaseDependency,
#     entities: list[ExampleEntityIn] = Body(...)
# ):
#     """Create multiple entities at once"""
#     created_entities = []
#     for entity_in in entities:
#         entity_out = ExampleEntityOut(
#             id=uuid4(),
#             created_at=datetime.utcnow(),
#             **entity_in.model_dump()
#         )
#         entity_model = ExampleEntityModel(**entity_out.model_dump())
#         db_session.add(entity_model)
#         created_entities.append(entity_out)
#     
#     await db_session.commit()
#     return created_entities


# Search endpoint
# @router.get('/search', response_model=Page[ExampleEntityOut])
# async def search_entities(
#     db_session: DatabaseDependency,
#     q: str = Query(..., description='Search query')
# ):
#     """Full-text search across multiple fields"""
#     query = select(ExampleEntityModel).filter(
#         or_(
#             ExampleEntityModel.name.ilike(f'%{q}%'),
#             ExampleEntityModel.description.ilike(f'%{q}%')
#         )
#     )
#     result = await db_session.execute(query)
#     entities = result.scalars().all()
#     return paginate([ExampleEntityOut.model_validate(e) for e in entities])

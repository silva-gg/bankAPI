"""
Shared Dependencies

Provides FastAPI dependencies used across the application.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.configs.database import get_session
from src.users.models import UserModel
from src.users.auth import decode_access_token


DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_session)
) -> UserModel:
    """
    Validate JWT token and return current user
    
    Args:
        credentials: HTTP authorization credentials
        db_session: Database session
        
    Returns:
        UserModel: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode token
    user_number = decode_access_token(token)
    if user_number is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    # Get user from database
    result = await db_session.execute(
        select(UserModel).filter_by(user_number=user_number)
    )
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user account'
        )
    
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]


async def require_admin(current_user: CurrentUser) -> UserModel:
    """
    Ensure current user has admin permissions
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserModel: Current user (if admin)
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin privileges required'
        )
    return current_user


RequireAdmin = Annotated[UserModel, Depends(require_admin)]

from src.users.basic_auth import get_current_user_basic, require_admin_basic

CurrentUserBasic = Annotated[UserModel, Depends(get_current_user_basic)]
RequireAdminBasic = Annotated[UserModel, Depends(require_admin_basic)]

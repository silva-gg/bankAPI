"""
Application Settings

Handles application configuration using Pydantic Settings.
Environment variables are automatically loaded from .env file.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Database Configuration
    DB_URL: str = Field(
        default='postgresql+asyncpg://api_user:api_password@localhost/api_database',
        description='Database connection URL'
    )
    
    # Application Configuration
    APP_NAME: str = Field(
        default='bankAPI',
        description='Application name'
    )
    
    APP_VERSION: str = Field(
        default='0.1.0',
        description='Application version'
    )
    
    DEBUG: bool = Field(
        default=False,
        description='Debug mode'
    )
    
    # JWT Authentication Configuration
    SECRET_KEY: str = Field(
        default='your-secret-key-change-this-in-production-use-openssl-rand-hex-32',
        description='Secret key for JWT token generation (CHANGE IN PRODUCTION!)'
    )
    
    ALGORITHM: str = Field(
        default='HS256',
        description='JWT algorithm'
    )
    
    ACCESS_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        description='JWT token expiration in days'
    )
    
    class Config:
        """Pydantic configuration"""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
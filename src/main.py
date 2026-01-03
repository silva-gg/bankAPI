"""
Main FastAPI Application Entry Point

This file initializes the FastAPI application and includes all routers.
Customize the title, description, and version according to your project.
"""

from fastapi import FastAPI
from src.routers import api_router
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager

# Create FastAPI application instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    # Startup
    print("🚀 bankAPI started successfully!")
    yield
    # Shutdown
    print("👋 bankAPI shutting down...")


app = FastAPI(
    title='🏧 bankAPI',
    description='A simple banking API built with FastAPI',
    version='0.1.0',
    docs_url='/docs',  # Swagger UI
    redoc_url='/redoc',  # ReDoc disabled
    lifespan=lifespan
)

# Include all API routers
app.include_router(api_router)

# Add pagination support
add_pagination(app)


@app.get('/', tags=['⚙️ Health'])
async def root():
    """
    Root endpoint - Health check
    
    Returns:
        dict: API status and version
    """
    return {
        'message': 'bankAPI is running!',
        'version': '0.1.0',
        'docs': '/docs'
    }


@app.get('/health', tags=['⚙️ Health'])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: Health status
    """
    return {'status': 'healthy'}




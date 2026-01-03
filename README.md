# 🏧 bankAPI

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-11-blue.svg)](https://www.postgresql.org/)

**A simplified banking API built with FastAPI.** This project demonstrates a basic banking system with user management, accounts, and transactions.

## 🎯 Overview

This is a simplified banking API that demonstrates:

- **User Management** - User registration and authentication using JWT tokens
- **Bank Accounts** - Create and manage bank accounts with different types (savings, checking)
- **Transactions** - Deposit and withdrawal operations with balance tracking
- **Security** - Password hashing with Argon2, JWT authentication, and account-level passwords
- **Limits & Controls** - Daily withdrawal limits and special withdrawal features

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [API Structure](#-api-structure)
- [Authentication](#-authentication)
- [Project Structure](#-project-structure)

## ✨ Features

### Core Features
- **🔐 JWT Authentication** - Secure user authentication with Argon2 password hashing
- **👤 User Management** - User registration and login with government ID numbers
- **🏦 Bank Accounts** - Create and manage accounts with different types (savings, checking)
- **💸 Transactions** - Deposit and withdrawal operations with automatic balance updates
- **🛡️ Security Controls** - Daily withdrawal limits and special withdrawal allowances
- **⚡ Asynchronous** - Full async/await support for optimal performance
- **📄 Auto Documentation** - Interactive Swagger UI and ReDoc
- **📊 Pagination** - Built-in pagination for all list endpoints
- **🗄️ Database Migrations** - Version control for your database with Alembic
- **🐳 Docker Support** - PostgreSQL container included

## 🚀 Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for Python
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints
- **[PostgreSQL](https://www.postgresql.org/)** - Powerful, open source database
- **[JWT](https://jwt.io/)** - JSON Web Tokens for authentication
- **[Argon2](https://github.com/hynek/argon2-cffi)** - Secure password hashing
- **[Docker](https://www.docker.com/)** - Containerization platform

## 📦 Prerequisites

- Python 3.11 or higher
- PostgreSQL (or use the included Docker setup)
- pip or Poetry for package management

## ⚡ Quick Start

Get your API running in 5 minutes:

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd bankAPI

# 2. Install dependencies
pip install -r requirements.txt
# or with Poetry: poetry install && poetry shell

# 3. Start database
docker-compose up -d

# 4. Run migrations
alembic upgrade head

# 5. Start the API
uvicorn src.main:app --reload
```

**That's it!** Your API is now running at http://localhost:8000

Visit http://localhost:8000/docs to see the interactive documentation.

## 🔐 Authentication

This API uses JWT-based authentication. Users must register and login to access protected endpoints.

### Registration

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "user_number": "123456789",
    "user_fullname": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_number": "123456789",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using Protected Endpoints

```bash
# Get current user info
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create an account
curl -X POST "http://localhost:8000/accounts" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "account_type": "savings",
    "password": "AccountPass123!"
  }'
```

## 🏗️ API Structure

The API provides three main resource groups:

### 1. Authentication (`/auth`)
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `GET /auth/me` - Get current user information
- `PATCH /auth/me` - Update current user
- `GET /auth/users` - List all users (admin only)
- `DELETE /auth/users/{user_id}` - Delete a user (admin only)

### 2. Accounts (`/accounts`)
- `POST /accounts` - Create a new bank account
- `GET /accounts` - List all accounts for current user
- `GET /accounts/{account_number}` - Get account details
- `PATCH /accounts/{account_number}` - Update account password

### 3. Transactions (`/transactions`)
- `POST /transactions` - Create a new transaction (deposit/withdrawal)
- `GET /transactions` - List all transactions
- `GET /transactions/account/{account_number}` - Get transactions for specific account

## 📁 Project Structure

```
bankAPI/
├── src/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── routers.py                # API router configuration
│   ├── configs/                  # Configuration files
│   │   ├── database.py           # Database connection setup
│   │   └── settings.py           # Application settings
│   ├── contrib/                  # Shared/common modules
│   │   ├── dependencies.py       # Shared dependencies
│   │   ├── models.py             # Base database models
│   │   └── schemas.py            # Base Pydantic schemas
│   ├── users/                    # User authentication module
│   │   ├── controller.py         # Auth endpoints
│   │   ├── models.py             # User database model
│   │   ├── schemas.py            # User Pydantic schemas
│   │   ├── auth.py               # JWT utilities
│   │   └── basic_auth.py         # HTTP Basic Auth (optional)
│   ├── accounts/                 # Bank accounts module
│   │   ├── controller.py         # Account endpoints
│   │   ├── models.py             # Account database model
│   │   └── schemas.py            # Account Pydantic schemas
│   └── transactions/             # Transactions module
│       ├── controller.py         # Transaction endpoints
│       ├── models.py             # Transaction database model
│       └── schemas.py            # Transaction Pydantic schemas
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration versions
│   └── env.py                    # Alembic environment
├── alembic.ini                   # Alembic configuration
├── docker-compose.yml            # Docker services
├── pyproject.toml                # Project dependencies
├── requirements.txt              # Pip dependencies
└── README.md                     # This file
```

## 🔒 Security Notes

- **Change SECRET_KEY in production!** Generate a secure key: `openssl rand -hex 32`
- Store secrets in environment variables, never in code
- Use HTTPS in production
- Keep dependencies updated: `pip list --outdated`
- Passwords are hashed using Argon2 (secure and modern)
- JWT tokens expire after 30 days (configurable in settings)

## 📄 License

This project is available under the MIT License.

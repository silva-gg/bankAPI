# HTTP Basic Authentication Guide

This guide explains how to use HTTP Basic Authentication with the bankAPI - an alternative to JWT for simple use cases.

## What is Basic Authentication?

HTTP Basic Authentication is a simple authentication scheme built into HTTP. You just send your user number/email and password with each request - no tokens to manage!

**Simple!** Just: `curl -u user_number:password http://localhost:8000/accounts`

## Why Basic Auth?

**Dead Simple:**
- ✅ No token management
- ✅ Works everywhere (curl, browsers, scripts)
- ✅ No extra API calls needed
- ✅ Perfect for getting started quickly

**When to Use:**
- 🎯 Scripts and automation (Python, Bash, PowerShell)
- 🎯 Command-line tools
- 🎯 Internal APIs
- 🎯 Development and testing
- 🎯 Quick prototypes

**Note:** Basic Auth is implemented but not currently used in the API endpoints. All endpoints use JWT authentication. This is available as an option if you want to enable it.

## Quick Start (30 seconds)

### 1. Register

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

### 2. Use it!

```bash
# Use with user_number
curl -u 123456789:SecurePass123! http://localhost:8000/accounts

# Or use with email
curl -u john@example.com:SecurePass123! http://localhost:8000/accounts
```

## Examples

### Create an Account

```bash
curl -u 123456789:SecurePass123! \
  -X POST http://localhost:8000/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_type": "savings",
    "password": "AccountPass123!"
  }'
```

### List Accounts

```bash
curl -u 123456789:SecurePass123! http://localhost:8000/accounts
```

### Create a Transaction

```bash
curl -u 123456789:SecurePass123! \
  -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "origin_account_number": 1,
    "value": 100.50,
    "transaction_type": "deposit"
  }'
```

## Using in Your Code

### Python (requests)

```python
import requests

# Super simple!
response = requests.get(
    'http://localhost:8000/accounts',
    auth=('123456789', 'SecurePass123!')
)
print(response.json())
```

### Python (httpx) - async

```python
import httpx

async with httpx.AsyncClient(
    auth=('123456789', 'SecurePass123!')
) as client:
    response = await client.get('http://localhost:8000/accounts')
    print(response.json())
```

### JavaScript/Node.js

```javascript
// Using fetch
const user_number = '123456789';
const password = 'SecurePass123!';
const auth = btoa(`${user_number}:${password}`);

fetch('http://localhost:8000/accounts', {
  headers: {
    'Authorization': `Basic ${auth}`
  }
})
.then(r => r.json())
.then(data => console.log(data));
```

### PowerShell

```powershell
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("123456789:SecurePass123!"))
Invoke-RestMethod -Uri "http://localhost:8000/accounts" `
  -Headers @{Authorization = "Basic $cred"}
```

## Testing with Swagger

1. Go to http://localhost:8000/docs
2. Click any protected endpoint
3. Click "Try it out"
4. Enter username and password when prompted
5. Test away!

## Protecting Your Endpoints

To enable Basic Auth in your endpoints, change from `CurrentUser` to `CurrentUserBasic`:

### Simple Protection

```python
from src.contrib.dependencies import CurrentUserBasic

@router.get('/my-endpoint')
async def my_endpoint(current_user: CurrentUserBasic):
    # Only authenticated users can access this
    return {"message": f"Hello {current_user.user_fullname}!"}
```

### Admin Only

```python
from src.contrib.dependencies import RequireAdminBasic

@router.delete('/admin/dangerous-stuff')
async def admin_only(admin: RequireAdminBasic):
    # Only admins can access this
    return {"message": "Admin access granted"}
```

## Complete Python Script Example

```python
#!/usr/bin/env python3
"""
Simple API client using Basic Auth
"""
import requests
import sys

BASE_URL = "http://localhost:8000"
USER_NUMBER = "123456789"
PASSWORD = "SecurePass123!"

class APIClient:
    def __init__(self):
        self.auth = (USER_NUMBER, PASSWORD)
    
    def create_account(self, account_type, password):
        response = requests.post(
            f"{BASE_URL}/accounts",
            auth=self.auth,
            json={"account_type": account_type, "password": password}
        )
        return response.json()
    
    def list_accounts(self):
        response = requests.get(
            f"{BASE_URL}/accounts",
            auth=self.auth
        )
        return response.json()
    
    def create_transaction(self, account_number, value, transaction_type):
        response = requests.post(
            f"{BASE_URL}/transactions",
            auth=self.auth,
            json={
                "origin_account_number": account_number,
                "value": value,
                "transaction_type": transaction_type
            }
        )
        return response.json()

if __name__ == "__main__":
    client = APIClient()
    
    # Create account
    account = client.create_account("savings", "AccountPass123!")
    print(f"Created: {account}")
    
    # List accounts
    accounts = client.list_accounts()
    print(f"Total accounts: {accounts['total']}")
```

## Security Notes

### Development (localhost)
✅ Basic Auth is perfect - simple and secure enough

### Production
⚠️ **Use HTTPS!** Basic Auth sends credentials with every request
- Set up SSL/TLS certificate
- Use nginx or similar as reverse proxy
- Consider rate limiting

### Quick Security Checklist
- [ ] HTTPS in production (mandatory!)
- [ ] Strong passwords
- [ ] Rate limiting to prevent brute force
- [ ] Monitor failed login attempts
- [ ] Use environment variables for credentials

## Also Available: JWT Auth

The API currently uses JWT authentication by default. See [AUTHENTICATION.md](AUTHENTICATION.md) for JWT details.

## When to Use What?

| Use Case | Use This |
|----------|----------|
| Scripts & CLI tools | ✅ Basic Auth |
| Internal APIs | ✅ Basic Auth |
| Quick prototypes | ✅ Basic Auth |
| Web applications | JWT Token (Current) |
| Mobile apps | JWT Token (Current) |
| Need token refresh | JWT Token (Current) |

## Common Issues

### 401 Unauthorized
- Check user number/email and password are correct
- Verify account is active
- Use user_number OR email (not both)

### 403 Forbidden
- User doesn't have required permissions
- For admin routes, user needs `is_superuser = true`

## Tips

**Store credentials securely:**
```python
import os
user_number = os.getenv('API_USER_NUMBER')
password = os.getenv('API_PASSWORD')
```

**Test quickly with curl:**
```bash
# Save credentials
export API_USER="123456789:SecurePass123!"

# Use them
curl -u $API_USER http://localhost:8000/accounts
```

**Debug auth issues:**
```bash
# See the Authorization header being sent
curl -v -u 123456789:SecurePass123! http://localhost:8000/accounts 2>&1 | grep Authorization
```

---

**That's it!** Basic Auth keeps things simple and gets you building features fast. 🚀

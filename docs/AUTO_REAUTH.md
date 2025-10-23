# Automatic Token Re-authentication

## Overview

The Arzeka Payment client now supports **automatic token re-authentication**. When a token expires, the client automatically re-authenticates using stored credentials before making any payment request. This eliminates the need to manually check token validity and re-authenticate.

## Features

- ✅ **Automatic Token Validation**: Checks token validity before each API request
- ✅ **Seamless Re-authentication**: Automatically re-authenticates when token expires
- ✅ **Credential Storage**: Securely stores username and password for re-authentication
- ✅ **Error Handling**: Provides clear error messages when re-authentication fails
- ✅ **Works Everywhere**: Available for both client instances and convenience functions

## How It Works

### 1. Initial Authentication

When you first authenticate, the client stores your credentials:

```python
from arzeka import ArzekaPayment

client = ArzekaPayment()
client.authenticate("your_username", "your_password")
```

Behind the scenes, the client stores:
- `_token`: The access token
- `_expires_at`: Token expiration timestamp
- `_username`: Your username (for re-authentication)
- `_password`: Your password (for re-authentication)

### 2. Automatic Token Checking

Before each API request (`initiate_payment` or `check_payment`), the client automatically:

1. Checks if the token is still valid using `is_token_valid()`
2. If valid → proceeds with the request
3. If expired → automatically re-authenticates using stored credentials
4. Then proceeds with the request

### 3. No Manual Intervention Required

You don't need to check token validity or re-authenticate manually:

```python
# Old way (manual)
if not client.is_token_valid():
    client.authenticate("username", "password")
response = client.initiate_payment(...)

# New way (automatic)
response = client.initiate_payment(...)  # Auto re-auth if needed!
```

## Usage Examples

### Example 1: Basic Usage

```python
from arzeka import ArzekaPayment

# Create client and authenticate once
client = ArzekaPayment()
client.authenticate("your_username", "your_password")

# Make multiple requests over time
# Token validation and re-authentication happen automatically

payment_data = {
    "amount": 1000,
    "merchant_id": "MERCHANT_123",
    "additional_info": {
        "first_name": "Jean",
        "last_name": "Dupont",
        "mobile": "70123456"
    },
    "hash_secret": "your_secret",
    "link_for_update_status": "https://example.com/webhook",
    "link_back_to_calling_website": "https://example.com/return"
}

# First payment (token valid)
response1 = client.initiate_payment(**payment_data)
print(f"Payment 1: {response1['mappedOrderId']}")

# ... time passes, token expires ...

# Second payment (token expired, auto re-authenticates)
response2 = client.initiate_payment(**payment_data)
print(f"Payment 2: {response2['mappedOrderId']}")

# Check payment status (uses same auto re-auth logic)
status = client.check_payment(response2['mappedOrderId'])
print(f"Status: {status}")

client.close()
```

### Example 2: With Convenience Functions

The automatic re-authentication also works with convenience functions:

```python
from arzeka import authenticate, initiate_payment, check_payment

# Authenticate once
authenticate("your_username", "your_password")

# Make multiple requests
# The shared client handles re-authentication automatically

payment_data = {
    "amount": 2000,
    "merchant_id": "MERCHANT_456",
    "additional_info": {...},
    "hash_secret": "secret",
    "link_for_update_status": "https://...",
    "link_back_to_calling_website": "https://..."
}

# Initiate payment (auto re-auth if token expired)
response = initiate_payment(payment_data)

# Check status (auto re-auth if token expired)
status = check_payment(response['mappedOrderId'])
```

### Example 3: Long-Running Application

Perfect for applications that run for extended periods:

```python
from arzeka import ArzekaPayment
import time

client = ArzekaPayment()
client.authenticate("your_username", "your_password")

# Application runs for hours/days
while True:
    # Process payments as they come in
    # Token validation and re-authentication are automatic

    try:
        response = client.initiate_payment(**payment_data)
        print(f"Payment processed: {response['mappedOrderId']}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(300)  # Wait 5 minutes
```

## Token Expiration Margin

The client considers a token expired **60 seconds before** its actual expiration time. This safety margin prevents requests from failing due to tokens expiring mid-request.

You can customize this margin:

```python
# Check if token is valid with custom margin
is_valid = client.is_token_valid(margin_seconds=300)  # 5 minutes before expiration
```

## Error Handling

### When Credentials Are Not Stored

If you manually set a token without authenticating, the client won't have credentials for re-authentication:

```python
client = ArzekaPayment()
client._token = "some_token"  # Manual token, no credentials stored
client._expires_at = time.time() - 100  # Expired token

try:
    response = client.initiate_payment(**payment_data)
except ArzekaAuthenticationError as e:
    print(f"Error: {e}")
    # Error: Token expired and no credentials stored for automatic re-authentication.
    #        Please call authenticate() again with username and password.
```

**Solution**: Always use the `authenticate()` method to set up authentication.

### When Re-authentication Fails

If automatic re-authentication fails (e.g., wrong credentials, network error), an exception is raised:

```python
try:
    response = client.initiate_payment(**payment_data)
except ArzekaAuthenticationError as e:
    print(f"Re-authentication failed: {e}")
    # Handle error appropriately
```

## Checking Token Status

You can still manually check token status if needed:

```python
# Simple check
if client.is_token_valid():
    print("Token is valid")
else:
    print("Token is expired")

# Detailed information
info = client.get_token_expiry_info()
print(f"Token expires in: {info['expires_in_minutes']:.1f} minutes")
print(f"Is valid: {info['is_valid']}")
print(f"Is expired: {info['is_expired']}")
```

## Security Considerations

### Credential Storage

- Credentials are stored in memory only (not persisted to disk)
- They are stored in private attributes (`_username`, `_password`)
- Credentials are cleared when the client is closed

### Best Practices

1. **Use environment variables** for credentials:
   ```python
   import os
   username = os.getenv('ARZEKA_USERNAME')
   password = os.getenv('ARZEKA_PASSWORD')
   client.authenticate(username, password)
   ```

2. **Close the client** when done:
   ```python
   client.close()  # Clears stored credentials
   ```

3. **Use context manager** for automatic cleanup:
   ```python
   with ArzekaPayment() as client:
       client.authenticate(username, password)
       # ... use client ...
   # Automatically closed and cleaned up
   ```

## Implementation Details

### The `_ensure_valid_token()` Method

This private method is called automatically by `initiate_payment()` and `check_payment()`:

```python
def _ensure_valid_token(self) -> None:
    """Ensure the token is valid, re-authenticating if necessary"""

    # Check if token is valid
    if self.is_token_valid():
        return  # Token is valid, nothing to do

    # Token is invalid, check if we have credentials
    if not self._username or not self._password:
        raise ArzekaAuthenticationError(
            "Token expired and no credentials stored"
        )

    # Re-authenticate
    self.authenticate(self._username, self._password)
```

### Modified Methods

Both `initiate_payment()` and `check_payment()` now call `_ensure_valid_token()` at the start:

```python
def initiate_payment(self, ...):
    # Ensure token is valid before making the request
    self._ensure_valid_token()

    # Rest of the method...

def check_payment(self, ...):
    # Ensure token is valid before making the request
    self._ensure_valid_token()

    # Rest of the method...
```

## Migration Guide

### From Manual Token Management

If you were manually managing tokens:

**Before:**
```python
client = ArzekaPayment()
client.authenticate("user", "pass")

# Before each request, check token
if not client.is_token_valid():
    client.authenticate("user", "pass")

response = client.initiate_payment(...)
```

**After:**
```python
client = ArzekaPayment()
client.authenticate("user", "pass")

# Just make requests, re-auth is automatic
response = client.initiate_payment(...)
```

### No Breaking Changes

This feature is **backward compatible**. Existing code will continue to work without modifications, but you can now remove manual token validation logic.

## Benefits

1. **Simpler Code**: No need to check token validity before each request
2. **Fewer Errors**: Eliminates forgotten token checks
3. **Better UX**: Seamless re-authentication without service interruption
4. **Production Ready**: Handles edge cases and provides clear error messages
5. **Time Saver**: Reduces boilerplate code in your application

## Related Documentation

- [Authentication Guide](AUTHENTICATION.md)
- [Token Validation Guide](TOKEN_VALIDATION.md)
- [Shared Client Usage](shared_client_example.py)
- [Auto Re-authentication Examples](auto_reauth_example.py)

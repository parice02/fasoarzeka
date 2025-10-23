"""
Example demonstrating automatic token re-authentication

This example shows how the ArzekaPayment client automatically
re-authenticates when the token expires, without manual intervention.
"""

import time
from arzeka import ArzekaPayment, authenticate, initiate_payment, check_payment


def example_1_automatic_reauth_with_instance():
    """
    Example 1: Automatic re-authentication with client instance

    The client stores credentials and automatically re-authenticates
    when the token expires before making any payment request.
    """
    print("=== Example 1: Automatic Re-authentication ===\n")

    # Create client and authenticate
    client = ArzekaPayment()
    auth = client.authenticate("your_username", "your_password")
    print(f"✓ Initial authentication successful")
    print(f"  Token expires in: {auth['expires_in']} seconds\n")

    # Make a payment (token is valid)
    payment_data = {
        "amount": 1000,
        "merchant_id": "MERCHANT_123",
        "additional_info": {
            "first_name": "Jean",
            "last_name": "Dupont",
            "mobile": "70123456",
        },
        "hash_secret": "your_secret",
        "link_for_update_status": "https://example.com/webhook",
        "link_back_to_calling_website": "https://example.com/return",
    }

    try:
        response = client.initiate_payment(**payment_data)
        print(f"✓ First payment initiated successfully")
        print(f"  Order ID: {response.get('mappedOrderId')}\n")
    except Exception as e:
        print(f"✗ Payment failed: {e}\n")

    # Simulate token expiration by setting expires_at to past
    print("⏰ Simulating token expiration...")
    client._expires_at = time.time() - 100  # Token expired 100 seconds ago

    # Check token validity
    if not client.is_token_valid():
        print("✓ Token is now expired\n")

    # Make another payment - will automatically re-authenticate
    print("🔄 Attempting payment with expired token...")
    try:
        response = client.initiate_payment(**payment_data)
        print(f"✓ Payment successful after automatic re-authentication")
        print(f"  Order ID: {response.get('mappedOrderId')}")
        print(
            f"  The client automatically re-authenticated before making the request!\n"
        )
    except Exception as e:
        print(f"✗ Payment failed: {e}\n")

    # Close client
    client.close()


def example_2_automatic_reauth_with_convenience_functions():
    """
    Example 2: Automatic re-authentication with convenience functions

    The shared client instance also supports automatic re-authentication.
    """
    print("=== Example 2: Automatic Re-auth with Convenience Functions ===\n")

    # Authenticate using convenience function
    auth = authenticate("your_username", "your_password")
    print(f"✓ Authentication successful")
    print(f"  Token expires in: {auth['expires_in']} seconds\n")

    # Prepare payment data
    payment_data = {
        "amount": 2000,
        "merchant_id": "MERCHANT_456",
        "additional_info": {
            "first_name": "Marie",
            "last_name": "Martin",
            "mobile": "70987654",
        },
        "hash_secret": "your_secret",
        "link_for_update_status": "https://example.com/webhook",
        "link_back_to_calling_website": "https://example.com/return",
    }

    # First payment
    try:
        response = initiate_payment(payment_data)
        print(f"✓ First payment initiated")
        order_id = response.get("mappedOrderId")
        print(f"  Order ID: {order_id}\n")
    except Exception as e:
        print(f"✗ Payment failed: {e}\n")
        return

    # Simulate token expiration
    from arzeka import _shared_client

    if _shared_client:
        print("⏰ Simulating token expiration...")
        _shared_client._expires_at = time.time() - 100

        if not _shared_client.is_token_valid():
            print("✓ Token is now expired\n")

    # Check payment status - will automatically re-authenticate
    print("🔄 Checking payment with expired token...")
    try:
        status = check_payment(order_id)
        print(f"✓ Payment status retrieved after automatic re-authentication")
        print(f"  Status: {status}\n")
    except Exception as e:
        print(f"✗ Status check failed: {e}\n")


def example_3_long_running_application():
    """
    Example 3: Long-running application with automatic re-authentication

    Simulates a long-running application that makes multiple requests
    over time, with automatic re-authentication when needed.
    """
    print("=== Example 3: Long-running Application ===\n")

    client = ArzekaPayment()
    client.authenticate("your_username", "your_password")
    print("✓ Application started and authenticated\n")

    # Simulate multiple requests over time
    payment_data = {
        "amount": 500,
        "merchant_id": "MERCHANT_789",
        "additional_info": {
            "first_name": "Pierre",
            "last_name": "Dubois",
            "mobile": "70555555",
        },
        "hash_secret": "your_secret",
        "link_for_update_status": "https://example.com/webhook",
        "link_back_to_calling_website": "https://example.com/return",
    }

    for i in range(3):
        print(f"--- Request {i + 1} ---")

        # Check token status
        token_info = client.get_token_expiry_info()
        print(f"Token status: {'Valid' if token_info['is_valid'] else 'Expired'}")
        print(f"Time until expiry: {token_info['expires_in_minutes']:.1f} minutes")

        # Make payment - automatic re-auth if needed
        try:
            response = client.initiate_payment(**payment_data)
            print(f"✓ Payment initiated: {response.get('mappedOrderId')}\n")
        except Exception as e:
            print(f"✗ Payment failed: {e}\n")

        # Simulate time passing (force expiration for demo)
        if i == 0:
            print("⏰ Simulating token expiration...")
            client._expires_at = time.time() - 10
            print()

    client.close()
    print("Application stopped")


def example_4_error_handling_no_credentials():
    """
    Example 4: Error handling when no credentials are stored

    Shows what happens when token expires and no credentials
    are available for automatic re-authentication.
    """
    print("=== Example 4: Error Handling - No Stored Credentials ===\n")

    # Create client without authenticating
    client = ArzekaPayment()
    client._token = "fake_token"  # Manually set an expired token
    client._expires_at = time.time() - 100

    print("⚠ Client has expired token but no stored credentials")
    print(f"Token valid: {client.is_token_valid()}\n")

    # Try to make a payment
    payment_data = {
        "amount": 1000,
        "merchant_id": "MERCHANT_123",
        "additional_info": {
            "first_name": "Test",
            "last_name": "User",
            "mobile": "70123456",
        },
        "hash_secret": "secret",
        "link_for_update_status": "https://example.com/webhook",
        "link_back_to_calling_website": "https://example.com/return",
    }

    try:
        response = client.initiate_payment(**payment_data)
        print(f"✓ Payment initiated: {response}")
    except Exception as e:
        print(f"✗ Expected error occurred: {type(e).__name__}")
        print(f"  Message: {str(e)}\n")
        print("💡 Solution: Call authenticate() with username and password first")

    client.close()


def example_5_manual_vs_automatic():
    """
    Example 5: Comparison of manual vs automatic re-authentication

    Shows the difference between manually checking and re-authenticating
    vs letting the client do it automatically.
    """
    print("=== Example 5: Manual vs Automatic Re-authentication ===\n")

    # --- Manual approach (old way) ---
    print("--- Manual Approach ---")
    client = ArzekaPayment()
    client.authenticate("username", "password")

    # Before each request, manually check token
    if not client.is_token_valid():
        print("Token expired, re-authenticating...")
        client.authenticate("username", "password")

    # Then make request
    print("Making request...\n")

    # --- Automatic approach (new way) ---
    print("--- Automatic Approach ---")
    client2 = ArzekaPayment()
    client2.authenticate("username", "password")

    # Just make the request - token validation happens automatically
    print("Making request (auto re-auth if needed)...\n")

    print("✓ Automatic approach is simpler and less error-prone!")

    client.close()
    client2.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Arzeka Payment - Automatic Re-authentication Examples")
    print("=" * 60)
    print()

    # Note: These examples use placeholder credentials
    # Replace with actual credentials to run successfully

    print("⚠️  Note: Replace placeholder credentials with actual values\n")

    # Uncomment to run examples:
    # example_1_automatic_reauth_with_instance()
    # example_2_automatic_reauth_with_convenience_functions()
    # example_3_long_running_application()
    # example_4_error_handling_no_credentials()
    # example_5_manual_vs_automatic()

    print("\n" + "=" * 60)
    print("Key Benefits of Automatic Re-authentication:")
    print("=" * 60)
    print("✓ No need to manually check token validity before each request")
    print("✓ Credentials stored securely within the client instance")
    print("✓ Seamless re-authentication when token expires")
    print("✓ Reduces code complexity and potential errors")
    print("✓ Works with both client instances and convenience functions")

"""
Example usage of the improved Arzeka Payment API client
"""

from arzeka import (
    ArzekaAPIError,
    ArzekaAuthenticationError,
    ArzekaPayment,
    ArzekaPaymentError,
    ArzekaValidationError,
    authenticate,
    check_payment,
    initiate_payment,
)

# Configuration
TOKEN = "your_arzeka_token_here"
BASE_URL = "https://pwg-test.fasoarzeka.com/"  # Test environment
MERCHANT_ID = "your_merchant_id"

# Credentials (for authentication example)
USERNAME = "your_username"
PASSWORD = "your_password"


# Example 0: Authentication to obtain access token
def example_authentication():
    """Example showing how to authenticate and get an access token"""
    try:
        with ArzekaPayment(token="", base_url=BASE_URL) as client:
            # Authenticate to get access token
            auth_response = client.authenticate(username=USERNAME, password=PASSWORD)

            print("Authentication successful!")
            print(f"Access Token: {auth_response['access_token']}")
            print(f"Token Type: {auth_response['token_type']}")
            print(f"Expires in: {auth_response['expires_in']} seconds")

            # The client's token is automatically updated
            # Now you can make payment requests with the authenticated client
            payment_response = client.initiate_payment(
                msisdn="22670123456", amount=1000, merchant_id=MERCHANT_ID
            )

            print(f"\nPayment initiated: {payment_response}")

    except ArzekaAuthenticationError as e:
        print(f"Authentication failed: {e}")
    except ArzekaValidationError as e:
        print(f"Validation error: {e}")
    except ArzekaAPIError as e:
        print(f"API error: {e}")


# Example 0b: Using the convenience function for authentication
def example_authentication_convenience():
    """Example using the authenticate convenience function"""
    try:
        # Get authentication token
        auth = authenticate(USERNAME, PASSWORD, BASE_URL)

        print("Authentication successful!")
        print(f"Token: {auth['access_token'][:20]}...")  # Show first 20 chars
        print(f"Expires in: {auth['expires_in']} seconds")

        # Use the token for subsequent requests
        token = auth["access_token"]

        with ArzekaPayment(token=token, base_url=BASE_URL) as client:
            response = client.initiate_payment(
                msisdn="22670123456", amount=1000, merchant_id=MERCHANT_ID
            )
            print(f"Payment initiated: {response}")

    except ArzekaAuthenticationError as e:
        print(f"Authentication failed: {e}")


# Example 1: Using the class with context manager (recommended)
def example_with_context_manager():
    """Example using context manager for automatic resource cleanup"""
    try:
        with ArzekaPayment(token=TOKEN, base_url=BASE_URL) as client:
            # Initiate payment
            payment_response = client.initiate_payment(
                msisdn="22670123456",  # Without the '+' sign
                amount=1000,
                merchant_id=MERCHANT_ID,
                link_for_update_status="https://yourdomain.com/webhook/payment-status",
                link_back_to_calling_website="https://yourdomain.com/payment/success",
            )

            print("Payment initiated successfully!")
            print(f"Order ID: {payment_response.get('mappedOrderId')}")
            print(f"Response: {payment_response}")

            # Check payment status
            order_id = payment_response.get("mappedOrderId")
            status_response = client.check_payment(mapped_order_id=order_id)

            print(f"\nPayment status: {status_response}")

    except ArzekaValidationError as e:
        print(f"Validation error: {e}")
    except ArzekaAPIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response data: {e.response_data}")
    except ArzekaPaymentError as e:
        print(f"Payment error: {e}")


# Example 2: Using the class instance directly
def example_with_class_instance():
    """Example using class instance directly"""
    client = ArzekaPayment(token=TOKEN, base_url=BASE_URL)

    try:
        # Initiate payment with custom order ID
        payment_response = client.initiate_payment(
            msisdn="22670123456",
            amount=5000,
            merchant_id=MERCHANT_ID,
            mapped_order_id="custom-order-12345",
        )

        print(f"Payment response: {payment_response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Don't forget to close the session
        client.close()


# Example 3: Using convenience functions (backward compatible)
def example_with_convenience_functions():
    """Example using convenience functions"""
    try:
        # Initiate payment
        payment_data = {
            "msisdn": "22670123456",
            "amount": 2500,
            "merchantid": MERCHANT_ID,
            "mappedOrderId": "order-xyz-789",
            "linkForUpdateStatus": "https://yourdomain.com/webhook/payment",
            "linkBackToCallingWebsite": "https://yourdomain.com/success",
        }

        response = initiate_payment(TOKEN, BASE_URL, payment_data)
        print(f"Payment initiated: {response}")

        # Check payment status
        status = check_payment(TOKEN, BASE_URL, "order-xyz-789")
        print(f"Payment status: {status}")

    except Exception as e:
        print(f"Error: {e}")


# Example 4: Error handling
def example_error_handling():
    """Example showing proper error handling"""
    try:
        with ArzekaPayment(token=TOKEN) as client:
            # This will raise a validation error (invalid amount)
            client.initiate_payment(
                msisdn="22670123456",
                amount=-100,  # Negative amount - invalid
                merchant_id=MERCHANT_ID,
            )
    except ArzekaValidationError as e:
        print(f"Validation failed: {e}")

    try:
        with ArzekaPayment(token="invalid_token") as client:
            # This will likely raise an API error
            client.initiate_payment(
                msisdn="22670123456", amount=1000, merchant_id=MERCHANT_ID
            )
    except ArzekaAPIError as e:
        print(f"API request failed with status {e.status_code}: {e}")


if __name__ == "__main__":
    print("Arzeka Payment API Examples\n")
    print("=" * 50)

    # Uncomment the example you want to run
    # example_authentication()
    # example_authentication_convenience()
    # example_with_context_manager()
    # example_with_class_instance()
    # example_with_convenience_functions()
    # example_error_handling()

    print(
        "\nNote: Replace USERNAME, PASSWORD, TOKEN and MERCHANT_ID with your actual credentials"
    )

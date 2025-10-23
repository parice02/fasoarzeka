"""
Utility functions for Arzeka Payment API
"""

import base64
import hashlib
from datetime import datetime


def get_reference() -> str:
    """
    Generate a unique reference ID for payment transactions

    Format: eT{YYMMDD}.{HHMMSS}.{microseconds}
    Example: eT251022.143025.123456

    Returns:
        str: Unique reference ID
    """
    reference = datetime.now().strftime("%y%m%d.%H%M%S.%f")
    return f"eT{reference}"


def format_msisdn(phone_number: str) -> str:
    """
    Format phone number to Arzeka API format (international without '+')

    Args:
        phone_number: Phone number in various formats

    Returns:
        str: Formatted phone number

    Examples:
        >>> format_msisdn("+226 70 12 34 56")
        "22670123456"
        >>> format_msisdn("226-70-12-34-56")
        "22670123456"
    """
    # Remove common separators and the '+' sign
    cleaned = (
        phone_number.replace("+", "")
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
    return cleaned


def validate_phone_number(msisdn: str, country_code: str = "226") -> bool:
    """
    Validate phone number format for Burkina Faso

    Args:
        msisdn: Phone number to validate
        country_code: Country code (default: 226 for Burkina Faso)

    Returns:
        bool: True if valid, False otherwise
    """
    cleaned = format_msisdn(msisdn)

    # Check if it starts with the country code
    if not cleaned.startswith(country_code):
        return False

    # Check length (country code + 8 digits for BF)
    expected_length = len(country_code) + 8
    if len(cleaned) != expected_length:
        return False

    # Check if all characters are digits
    return cleaned.isdigit()


def generate_hash_signature(secret: str, **kwargs) -> str:
    """
    Generate a SHA256 hash signature for the given data using the provided secret.

    Args:
        secret: The secret key used for hashing.
        **kwargs: The data to be hashed.

    Returns:
        str: The generated hash signature.
    """
    # Combine data and secret
    print(kwargs)
    message = f"{kwargs.get("amount")}|{kwargs.get("merchant_id")}|{kwargs.get("mappedOrderId")}|{kwargs.get("linkBackToCallingWebsite")}|{kwargs.get("linkForUpdateStatus")}|{kwargs.get("additionalInfo")}|{secret}"

    print(message)

    # Generate SHA256 hash
    hash_signature = hashlib.sha256(message.encode()).digest()
    return base64.b64encode(hash_signature).decode()

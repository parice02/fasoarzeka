"""
Arzeka Payment API Client
Unofficial API client for Faso Arzeka mobile money payments in Burkina Faso
"""

from .arzeka import (
    ArzekaPayment,
    initiate_payment,
    check_payment,
    authenticate,
    close_shared_client,
    get_shared_client,
)

from .utils import (
    get_reference,
    format_msisdn,
    validate_phone_number,
)

__version__ = "1.0.0"
__author__ = "Mohamed Zeba (m.zeba@mzeba.dev)"
__all__ = [
    # Classes
    "ArzekaPayment",
    # Functions
    "initiate_payment",
    "check_payment",
    "authenticate",
    "close_shared_client",
    "get_shared_client",
    # Utility functions
    "get_reference",
    "format_msisdn",
    "validate_phone_number",
]

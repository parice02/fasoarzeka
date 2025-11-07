"""
Arzeka Payment API Client
Unofficial API client for Faso Arzeka mobile money payments in Burkina Faso
"""

from .arzeka import (
    ArzekaPayment,
    authenticate,
    check_payment,
    close_shared_client,
    get_shared_client,
    initiate_payment,
)
from .utils import (
    format_msisdn,
    get_reference,
    validate_phone_number,
    generate_hash_signature,
)
from .i18n import install_translations

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
    "generate_hash_signature",
    # i18n helper
    "install_translations",
]

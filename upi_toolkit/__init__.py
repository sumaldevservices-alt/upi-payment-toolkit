"""
UPI Payment Toolkit
High-performance Python library for NPCI-compliant UPI URI generation,
dynamic QR codes, deep links, and UTR validation.
"""

from upi_toolkit.uri import UPITransaction, generate_upi_uri, parse_upi_uri
from upi_toolkit.intents import generate_intent_urls, AppIntent
from upi_toolkit.qr import generate_qr_bytes, generate_qr_base64
from upi_toolkit.validator import validate_vpa, validate_utr

__version__ = "1.0.0"
__all__ = [
    "UPITransaction",
    "generate_upi_uri",
    "parse_upi_uri",
    "generate_intent_urls",
    "AppIntent",
    "generate_qr_bytes",
    "generate_qr_base64",
    "validate_vpa",
    "validate_utr",
]

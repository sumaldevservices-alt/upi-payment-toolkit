import re
from typing import Tuple, Optional

# Standard VPA regex according to NPCI specifications:
# username@psp (e.g. user@okhdfcbank, mobile@paytm, name@fam)
VPA_REGEX = re.compile(r"^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z0-9]{2,64}$")

# Standard 12-digit numeric UTR / RRN (Retrieval Reference Number)
UTR_12_REGEX = re.compile(r"^[0-9]{12}$")

# Extended alphanumeric bank reference format (some banks/IMPS use 12-22 chars)
BANK_REF_REGEX = re.compile(r"^[a-zA-Z0-9]{10,24}$")


def validate_vpa(vpa: str) -> Tuple[bool, Optional[str]]:
    """
    Validate UPI Virtual Payment Address (VPA).
    Returns (is_valid, error_message).
    """
    if not vpa or not isinstance(vpa, str):
        return False, "VPA cannot be empty"

    cleaned = vpa.strip()
    if len(cleaned) < 5 or len(cleaned) > 256:
        return False, "VPA length must be between 5 and 256 characters"

    if "@" not in cleaned:
        return False, "VPA must contain '@' separator"

    user_part, handle_part = cleaned.split("@", 1)
    if not user_part:
        return False, "VPA username part cannot be empty"
    if not handle_part:
        return False, "VPA handle (bank/PSP) part cannot be empty"

    if not VPA_REGEX.match(cleaned):
        return False, "VPA contains invalid characters or structure"

    return True, None


def validate_utr(utr: str, strict_12_digit: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate UPI UTR / RRN.
    Strict mode enforces exact 12-digit numeric standard (NPCI standard).
    Non-strict accepts alphanumeric references up to 24 chars.
    """
    if not utr or not isinstance(utr, str):
        return False, "UTR cannot be empty"

    cleaned = utr.strip()
    if strict_12_digit:
        if not UTR_12_REGEX.match(cleaned):
            return False, "UTR must be exactly 12 numeric digits (NPCI standard)"
    else:
        if not BANK_REF_REGEX.match(cleaned):
            return False, "Reference ID contains invalid characters (alphanumeric 10-24 chars required)"

    return True, None

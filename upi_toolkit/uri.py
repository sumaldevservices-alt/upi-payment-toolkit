from dataclasses import dataclass
from typing import Optional, Dict
from urllib.parse import urlencode, parse_qs, urlparse
from decimal import Decimal


@dataclass
class UPITransaction:
    vpa: str
    name: str
    amount: Optional[Decimal] = None
    transaction_ref: Optional[str] = None
    transaction_id: Optional[str] = None
    note: Optional[str] = None
    merchant_code: Optional[str] = None
    currency: str = "INR"
    url: Optional[str] = None
    mode: Optional[str] = None

    def to_uri(self) -> str:
        return generate_upi_uri(
            vpa=self.vpa,
            name=self.name,
            amount=self.amount,
            transaction_ref=self.transaction_ref,
            transaction_id=self.transaction_id,
            note=self.note,
            merchant_code=self.merchant_code,
            currency=self.currency,
            url=self.url,
            mode=self.mode,
        )


def generate_upi_uri(
    vpa: str,
    name: str,
    amount: Optional[Decimal | float | int | str] = None,
    transaction_ref: Optional[str] = None,
    transaction_id: Optional[str] = None,
    note: Optional[str] = None,
    merchant_code: Optional[str] = None,
    currency: str = "INR",
    url: Optional[str] = None,
    mode: Optional[str] = None,
) -> str:
    """Generate an NPCI-compliant UPI payment URI."""
    if not vpa or "@" not in vpa:
        raise ValueError("Invalid VPA format. Must contain '@'")
    if not name or not name.strip():
        raise ValueError("Payee name cannot be empty")

    params: Dict[str, str] = {
        "pa": vpa.strip(),
        "pn": name.strip(),
        "cu": currency.strip().upper(),
    }

    if amount is not None:
        dec_amount = Decimal(str(amount))
        if dec_amount <= 0:
            raise ValueError("Amount must be greater than zero")
        params["am"] = f"{dec_amount:.2f}"

    if transaction_ref:
        params["tr"] = transaction_ref.strip()
    if transaction_id:
        params["tid"] = transaction_id.strip()
    if note:
        params["tn"] = note.strip()
    if merchant_code:
        params["mc"] = merchant_code.strip()
    if url:
        params["url"] = url.strip()
    if mode:
        params["mode"] = mode.strip()

    return f"upi://pay?{urlencode(params)}"


def parse_upi_uri(uri: str) -> UPITransaction:
    """Parse a upi://pay URI into a UPITransaction object."""
    if not uri.startswith("upi://pay"):
        raise ValueError("URI must start with upi://pay")

    parsed = urlparse(uri)
    query = parse_qs(parsed.query)

    vpa = query.get("pa", [None])[0]
    name = query.get("pn", [None])[0]

    if not vpa or not name:
        raise ValueError("UPI URI missing mandatory 'pa' or 'pn' parameters")

    amount_str = query.get("am", [None])[0]
    amount = Decimal(amount_str) if amount_str else None

    return UPITransaction(
        vpa=vpa,
        name=name,
        amount=amount,
        transaction_ref=query.get("tr", [None])[0],
        transaction_id=query.get("tid", [None])[0],
        note=query.get("tn", [None])[0],
        merchant_code=query.get("mc", [None])[0],
        currency=query.get("cu", ["INR"])[0],
        url=query.get("url", [None])[0],
        mode=query.get("mode", [None])[0],
    )

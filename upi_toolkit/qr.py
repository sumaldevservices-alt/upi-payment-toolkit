import io
import base64
from typing import Optional
import qrcode
from qrcode.image.pil import PilImage


def generate_qr_bytes(
    upi_uri: str,
    box_size: int = 10,
    border: int = 2,
    fill_color: str = "black",
    back_color: str = "white",
    format: str = "PNG",
) -> bytes:
    """Generate raw QR code bytes from a UPI URI."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(upi_uri)
    qr.make(fit=True)

    img: PilImage = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    return buffer.getvalue()


def generate_qr_base64(
    upi_uri: str,
    box_size: int = 10,
    border: int = 2,
    fill_color: str = "black",
    back_color: str = "white",
) -> str:
    """Generate a base64 encoded data URI for direct HTML/frontend rendering."""
    raw_bytes = generate_qr_bytes(
        upi_uri=upi_uri,
        box_size=box_size,
        border=border,
        fill_color=fill_color,
        back_color=back_color,
        format="PNG",
    )
    b64_str = base64.b64encode(raw_bytes).decode("ascii")
    return f"data:image/png;base64,{b64_str}"

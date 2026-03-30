from __future__ import annotations

from io import BytesIO

import qrcode
from PIL import Image


def build_qr_image(data: str, box_size: int = 10, border: int = 4) -> Image.Image:
    """Create a QR image for a URL or any other text payload."""
    cleaned_data = data.strip()
    if not cleaned_data:
        raise ValueError("Enter a website or direct link first.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(cleaned_data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    if hasattr(image, "get_image"):
        image = image.get_image()
    return image.convert("RGB")


def image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()

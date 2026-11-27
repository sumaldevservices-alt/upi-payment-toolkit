# UPI Payment Toolkit

A high‑performance Python library and micro‑service for generating NPCI‑compliant UPI payment URIs, deep‑link intents for major UPI apps, QR code images, and validation utilities for VPA and UTR.

Features
- **URI Builder** – generate `upi://pay?...` strings with optional fields (amount, transaction ref, note, etc.)
- **App Intents** – automatically produce deep‑links for PhonePe, Google Pay, Paytm, BHIM, Cred and the standard schema.
- **QR Generation** – return raw PNG bytes or base64 data‑URL for embedding in webpages or PDFs.
- **Validator** – strict VPA format checking and 12‑digit UTR validation (with optional relaxed mode).
- **FastAPI Service** – REST endpoints for on‑the‑fly URI creation, QR images and validation.
- **CLI** – command line tool for quick generation, QR export and validation.
- **Docker** – ready‑to‑run container exposing the API on port 8000.
- **Test Suite** – full pytest coverage (>90%).

---

## Installation
```bash
pip install upi-payment-toolkit
```
Or clone the repo and install the development dependencies:
```bash
git clone https://github.com/sumaldevservices-alt/upi-payment-toolkit.git
cd upi-payment-toolkit
pip install -e .
```

---

## Quick Usage (Python)
```python
from upi_toolkit import generate_upi_uri, generate_intent_urls, generate_qr_base64

uri = generate_upi_uri(vpa="akash-sumal@fam", name="Sumal Dev", amount=149.99)
print(uri)
print(generate_intent_urls(uri)["gpay"])  # Google Pay deep link
print(generate_qr_base64(uri))          # embed in HTML <img src="...">
```

---

## Run the API Server
```bash
uvicorn upi_toolkit.server:app --host 0.0.0.0 --port 8000
```

---

## License
MIT – see LICENSE file.

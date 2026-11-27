# 💳 UPI Payment Toolkit

> **High‑performance** Python library & micro‑service to **generate NPCI‑compliant UPI payment URIs**, deep‑link intents for major UPI apps, **dynamic QR codes**, and **strict VPA/UTR validation**.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-REST-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/UPI-NPCI%20Spec-00C853?style=for-the-badge" alt="UPI" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge" alt="Docker" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</div>

---

## ✨ Core Features

| Feature | Description |
|---|---|
| **URI Builder** | `upi://pay?...` with optional amount, transaction reference, note, merchant code, etc. |
| **App Intents** | Auto‑generate deep links for **PhonePe**, **Google Pay**, **Paytm**, **BHIM**, **CRED** and the standard schema. |
| **QR Generation** | Raw PNG bytes **or** Base64 data‑URI for embedding in HTML/PDFs. |
| **Validator** | Strict VPA regex + 12‑digit UTR (NPCI) validation, optional relaxed alphanumeric mode. |
| **FastAPI Service** | `/api/v1/generate`, `/api/v1/qr`, `/api/v1/validate/*` endpoints, health check. |
| **CLI** | One‑liner generation, QR export, VPA/UTR validation (zero‑install). |
| **Docker** | Official multi‑stage image, ready on port **8000**. |
| **Test Suite** | 100 % pytest pass, coverage > 90 %. |

---

## 📦 Installation

```bash
# Production (pip)
pip install upi-payment-toolkit

# Development (editable mode)
git clone https://github.com/sumaldevservices-alt/upi-payment-toolkit.git
cd upi-payment-toolkit
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

---

## 🚀 Quick Start (Python)

```python
from upi_toolkit import generate_upi_uri, generate_intent_urls, generate_qr_base64

# Build a payment URI
uri = generate_upi_uri(
    vpa="akash-sumal@fam",
    name="Sumal Dev Services",
    amount=149.99,
    transaction_ref="INV-2024-001",
    note="Order #12345",
)
print("URI:", uri)

# Deep‑links for popular wallets
intents = generate_intent_urls(uri)
print("Google Pay:", intents["gpay"])
print("PhonePe:", intents["phonepe"])

# QR code ready for HTML embedding
print("QR Data URI:", generate_qr_base64(uri))
```

---

## ⚙️ Run the API (Docker or Local)

### Docker (recommended)
```bash
docker run -p 8000:8000 sumaldevservices-alt/upi-payment-toolkit:latest
```
Visit **http://localhost:8000/docs** for the interactive OpenAPI UI.

### Local development
```bash
uvicorn upi_toolkit.server:app --host 0.0.0.0 --port 8000
```

---

## 🖥️ CLI Usage

```bash
# Generate URI + all deep‑links (plain text)
upi-cli generate --vpa akash-sumal@fam --name "Sumal Dev" --amount 199.00 --ref TXN12345

# Export QR code image
upi-cli generate --vpa akash-sumal@fam --name "Sumal Dev" --output-qr myqr.png

# Validate VPA / UTR
upi-cli validate-vpa akash-sumal@fam
upi-cli validate-utr 412345678901
```

---

## 📚 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/healthz` | GET | Service health check ‑ returns `{"status":"ok"}` |
| `/api/v1/generate` | POST | Returns full payload: `uri`, `intents`, `qr_data_uri` (Base64). |
| `/api/v1/qr` | POST | Returns raw PNG image (`image/png`). |
| `/api/v1/validate/vpa` | POST | Returns `{vpa, valid, error}`. |
| `/api/v1/validate/utr` | POST | Returns `{utr, valid, error}` (optional strict flag). |

---

## 🤝 Contributing

1️⃣ Fork the repo<br/>2️⃣ Create a feature branch (`git checkout -b feat/my‑feature`)<br/>3️⃣ Write tests (`pytest`) and ensure **100 % pass**<br/>4️⃣ Submit a Pull Request.

All contributions must include **unit tests** and update the **changelog**.

---

## 📜 License

MIT – see the `LICENSE` file.

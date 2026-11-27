from typing import Optional, Dict
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from upi_toolkit.uri import generate_upi_uri
from upi_toolkit.intents import generate_intent_urls
from upi_toolkit.qr import generate_qr_bytes, generate_qr_base64
from upi_toolkit.validator import validate_vpa, validate_utr

app = FastAPI(
    title="UPI Payment Toolkit API",
    version="1.0.0",
    description="High-speed REST API for dynamic NPCI UPI URI generation, QR codes, and UTR validation.",
)


class UPIRequest(BaseModel):
    vpa: str = Field(..., description="Payee VPA / UPI ID", json_schema_extra={"example": "akash-sumal@fam"})
    name: str = Field(..., description="Payee Name", json_schema_extra={"example": "Sumal Dev Services"})
    amount: Optional[float] = Field(None, description="Amount in INR", json_schema_extra={"example": 499.00})
    transaction_ref: Optional[str] = Field(None, description="Reference ID", json_schema_extra={"example": "TXN987654321"})
    note: Optional[str] = Field(None, description="Payment note", json_schema_extra={"example": "Order #1234"})
    merchant_code: Optional[str] = Field(None, description="Optional MCC")


class UPIResponse(BaseModel):
    uri: str
    vpa: str
    name: str
    amount: Optional[float]
    intents: Dict[str, str]
    qr_data_uri: str


class ValidateVPARequest(BaseModel):
    vpa: str = Field(..., description="VPA address", json_schema_extra={"example": "user@okhdfcbank"})


class ValidateUTRRequest(BaseModel):
    utr: str = Field(..., description="12-digit UTR", json_schema_extra={"example": "412345678901"})
    strict: bool = Field(default=True)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "upi-payment-toolkit"}


@app.post("/api/v1/generate", response_model=UPIResponse)
def generate_payment_payload(req: UPIRequest):
    is_valid, err = validate_vpa(req.vpa)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid VPA: {err}")

    try:
        uri = generate_upi_uri(
            vpa=req.vpa,
            name=req.name,
            amount=req.amount,
            transaction_ref=req.transaction_ref,
            note=req.note,
            merchant_code=req.merchant_code,
        )
        intents = generate_intent_urls(uri)
        qr_b64 = generate_qr_base64(uri)

        return UPIResponse(
            uri=uri,
            vpa=req.vpa,
            name=req.name,
            amount=req.amount,
            intents=intents,
            qr_data_uri=qr_b64,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/qr")
def generate_qr_image(req: UPIRequest):
    is_valid, err = validate_vpa(req.vpa)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid VPA: {err}")

    try:
        uri = generate_upi_uri(
            vpa=req.vpa,
            name=req.name,
            amount=req.amount,
            transaction_ref=req.transaction_ref,
            note=req.note,
        )
        png_bytes = generate_qr_bytes(uri)
        return Response(content=png_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/validate/vpa")
def check_vpa(req: ValidateVPARequest):
    is_valid, err = validate_vpa(req.vpa)
    return {"vpa": req.vpa, "valid": is_valid, "error": err}


@app.post("/api/v1/validate/utr")
def check_utr(req: ValidateUTRRequest):
    is_valid, err = validate_utr(req.utr, strict_12_digit=req.strict)
    return {"utr": req.utr, "valid": is_valid, "error": err}

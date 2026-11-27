import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from upi_toolkit.uri import generate_upi_uri, parse_upi_uri, UPITransaction
from upi_toolkit.intents import generate_intent_urls
from upi_toolkit.qr import generate_qr_bytes, generate_qr_base64
from upi_toolkit.validator import validate_vpa, validate_utr
from upi_toolkit.server import app

client = TestClient(app)


def test_generate_and_parse_upi_uri():
    uri = generate_upi_uri(
        vpa="akash-sumal@fam",
        name="Sumal Dev",
        amount=199.50,
        transaction_ref="ORDER999",
        note="Pro License",
    )
    assert uri.startswith("upi://pay?")
    assert "pa=akash-sumal%40fam" in uri
    assert "pn=Sumal+Dev" in uri
    assert "am=199.50" in uri
    assert "tr=ORDER999" in uri
    assert "tn=Pro+License" in uri

    parsed = parse_upi_uri(uri)
    assert parsed.vpa == "akash-sumal@fam"
    assert parsed.name == "Sumal Dev"
    assert parsed.amount == Decimal("199.50")
    assert parsed.transaction_ref == "ORDER999"
    assert parsed.note == "Pro License"


def test_invalid_vpa_in_uri():
    with pytest.raises(ValueError):
        generate_upi_uri(vpa="invalid_without_at", name="Sumal")

    with pytest.raises(ValueError):
        generate_upi_uri(vpa="user@fam", name="")


def test_intent_urls_generation():
    uri = "upi://pay?pa=akash-sumal@fam&pn=Sumal&am=100.00&cu=INR"
    intents = generate_intent_urls(uri)

    assert "standard" in intents
    assert "phonepe" in intents
    assert "gpay" in intents
    assert "paytm" in intents
    assert "bhim" in intents
    assert "cred" in intents

    assert intents["phonepe"].startswith("phonepe://pay?")
    assert intents["gpay"].startswith("tez://upi/pay?")
    assert intents["paytm"].startswith("paytmmp://pay?")


def test_qr_generation():
    uri = "upi://pay?pa=akash-sumal@fam&pn=Sumal&am=500.00&cu=INR"
    qr_bytes = generate_qr_bytes(uri)
    assert len(qr_bytes) > 100
    assert qr_bytes.startswith(b"\x89PNG")

    qr_b64 = generate_qr_base64(uri)
    assert qr_b64.startswith("data:image/png;base64,")


def test_validate_vpa():
    assert validate_vpa("akash-sumal@fam")[0] is True
    assert validate_vpa("user@okhdfcbank")[0] is True
    assert validate_vpa("9876543210@paytm")[0] is True

    # Invalids
    assert validate_vpa("")[0] is False
    assert validate_vpa("no_at_symbol")[0] is False
    assert validate_vpa("@onlyhandle")[0] is False
    assert validate_vpa("user@")[0] is False


def test_validate_utr():
    # Valid 12 digits
    assert validate_utr("412345678901")[0] is True
    assert validate_utr("001122334455")[0] is True

    # Invalid
    assert validate_utr("12345")[0] is False
    assert validate_utr("41234567890A")[0] is False
    assert validate_utr("41234567890123")[0] is False

    # Non-strict
    assert validate_utr("TXN1234567890", strict_12_digit=False)[0] is True


def test_api_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_api_generate():
    payload = {
        "vpa": "akash-sumal@fam",
        "name": "Sumal Dev Services",
        "amount": 299.00,
        "transaction_ref": "REF12345",
        "note": "Subscription",
    }
    resp = client.post("/api/v1/generate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "uri" in data
    assert "intents" in data
    assert "phonepe" in data["intents"]
    assert data["qr_data_uri"].startswith("data:image/png;base64,")


def test_api_qr_image():
    payload = {
        "vpa": "akash-sumal@fam",
        "name": "Sumal",
        "amount": 100.0,
    }
    resp = client.post("/api/v1/qr", json=payload)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert resp.content.startswith(b"\x89PNG")

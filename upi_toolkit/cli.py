import argparse
import sys
from upi_toolkit.uri import generate_upi_uri
from upi_toolkit.intents import generate_intent_urls
from upi_toolkit.qr import generate_qr_bytes
from upi_toolkit.validator import validate_vpa, validate_utr


def main():
    parser = argparse.ArgumentParser(
        description="UPI Payment Toolkit CLI - Generate QR, Intents, and validate VPA/UTR"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate UPI URI and deep links")
    gen_parser.add_argument("--vpa", required=True, help="Payee VPA (e.g., merchant@fam)")
    gen_parser.add_argument("--name", required=True, help="Payee name")
    gen_parser.add_argument("--amount", type=float, help="Amount in INR")
    gen_parser.add_argument("--ref", help="Transaction reference ID")
    gen_parser.add_argument("--note", help="Payment note / remarks")
    gen_parser.add_argument("--output-qr", help="Output PNG file path for QR code")

    # Command: validate-vpa
    vpa_parser = subparsers.add_parser("validate-vpa", help="Validate a VPA / UPI ID")
    vpa_parser.add_argument("vpa", help="VPA address to validate")

    # Command: validate-utr
    utr_parser = subparsers.add_parser("validate-utr", help="Validate a 12-digit UTR/RRN")
    utr_parser.add_argument("utr", help="UTR string to validate")

    args = parser.parse_args()

    if args.command == "generate":
        valid, err = validate_vpa(args.vpa)
        if not valid:
            print(f"[ERROR] Invalid VPA: {err}", file=sys.stderr)
            sys.exit(1)

        uri = generate_upi_uri(
            vpa=args.vpa,
            name=args.name,
            amount=args.amount,
            transaction_ref=args.ref,
            note=args.note,
        )
        print("Generated UPI URI:")
        print(uri)
        print("\nApp Deep Links:")
        for app_name, link in generate_intent_urls(uri).items():
            print(f"  - {app_name.capitalize()}: {link}")

        if args.output_qr:
            qr_bytes = generate_qr_bytes(uri)
            with open(args.output_qr, "wb") as f:
                f.write(qr_bytes)
            print(f"\nQR Code saved to: {args.output_qr}")

    elif args.command == "validate-vpa":
        valid, err = validate_vpa(args.vpa)
        if valid:
            print(f"[VALID] VPA '{args.vpa}' is properly formatted.")
        else:
            print(f"[INVALID] {err}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "validate-utr":
        valid, err = validate_utr(args.utr)
        if valid:
            print(f"[VALID] UTR '{args.utr}' is a valid 12-digit NPCI reference.")
        else:
            print(f"[INVALID] {err}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

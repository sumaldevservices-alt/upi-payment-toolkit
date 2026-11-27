from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlparse, urlunparse


@dataclass
class AppIntent:
    app_name: str
    scheme: str
    deep_link: str


APP_SCHEMES = {
    "standard": "upi://pay",
    "phonepe": "phonepe://pay",
    "gpay": "tez://upi/pay",
    "paytm": "paytmmp://pay",
    "bhim": "bhim://pay",
    "cred": "cred://pay",
}


def generate_intent_urls(upi_uri: str) -> Dict[str, str]:
    """
    Transform a standard upi://pay URI into application-specific deep links.
    Returns a dictionary of app_name -> deep_link_url.
    """
    if not upi_uri.startswith("upi://pay"):
        raise ValueError("URI must start with upi://pay")

    parsed = urlparse(upi_uri)
    query_string = parsed.query

    intents: Dict[str, str] = {}
    for app_name, base_scheme in APP_SCHEMES.items():
        if app_name == "standard":
            intents[app_name] = upi_uri
        else:
            base_parsed = urlparse(base_scheme)
            new_url = urlunparse((
                base_parsed.scheme,
                base_parsed.netloc,
                base_parsed.path,
                "",
                query_string,
                "",
            ))
            intents[app_name] = new_url

    return intents

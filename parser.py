import re
from urllib.parse import urlparse

CATEGORIES = {
    "investment": "Investment Scam",
    "crypto": "Cryptocurrency Scam",
    "romance": "Romance Scam",
    "phishing": "Phishing",
    "impersonation": "Impersonation Scam",
    "giveaway": "Giveaway Scam",
    "recovery": "Recovery Scam",
    "pig butchering": "Pig Butchering Scam",
    "forex": "Forex Scam",
    "job": "Job Scam",
    "shopping": "Shopping Scam",
    "nft": "NFT Scam",
}

def extract_domain(text):
    urls = re.findall(r'https?://[^\s<>"\']+', text)

    if not urls:
        return None

    url = urls[0].rstrip('.,);')
    return urlparse(url).netloc.lower().replace("www.", "")

def extract_amount(text):
    match = re.search(
        r'(?i)(?:\$|USD\s*)?([\d,]+(?:\.\d+)?)\s*(?:USD|USDT|dollars?)?',
        text
    )

    if not match:
        return None

    return float(match.group(1).replace(",", ""))

def extract_currency(text):
    upper = text.upper()

    if "USDT" in upper:
        return "USDT"
    if "USD" in upper or "$" in text or "DOLLAR" in upper:
        return "USD"

    return None

def extract_category(text):
    lower = text.lower()

    for keyword, category in CATEGORIES.items():
        if keyword in lower:
            return category

    return "Uncategorized"

def extract_date(text):
    patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None

def parse_report(text):
    return {
        "domain": extract_domain(text),
        "amount_lost": extract_amount(text),
        "currency": extract_currency(text),
        "report_date": extract_date(text),
        "category": extract_category(text),
        "description": text.strip()
    }

if __name__ == "__main__":
    sample = """
    I lost $5,000 to a crypto investment scam on 2026-09-10.
    The website was https://example-scam.com
    """

    result = parse_report(sample)

    print("Parsed report:")
    for key, value in result.items():
        print(f"{key}: {value}")

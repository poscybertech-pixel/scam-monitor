import os
import sys
import json
import sqlite3
from datetime import datetime
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.chainabuse.com/v0/reports"
DB_FILE = "scam_reports.db"
USAGE_FILE = "chainabuse_usage.json"

API_KEY = os.getenv("CHAINABUSE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MAX_MONTHLY_CALLS = 10


def get_domain(value):
    value = value.strip()

    if not value.startswith(("http://", "https://")):
        value = "https://" + value

    parsed = urlparse(value)
    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain, value


def load_usage():
    month = datetime.now().strftime("%Y-%m")

    if not os.path.exists(USAGE_FILE):
        return {"month": month, "calls": 0}

    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)

        if data.get("month") != month:
            return {"month": month, "calls": 0}

        return data

    except Exception:
        return {"month": month, "calls": 0}


def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_report(domain, report):
    conn = sqlite3.connect(DB_FILE)

    scammer_urls = report.get("scammerUrls") or report.get("scammer_urls") or []
    if isinstance(scammer_urls, list):
        website_url = scammer_urls[0] if scammer_urls else f"https://{domain}"
    else:
        website_url = str(scammer_urls)

    amount = report.get("reportedLoss")

    if isinstance(amount, dict):
        amount_lost = amount.get("amount") or amount.get("value")
        currency = amount.get("currency") or amount.get("asset") or "USD"
    else:
        amount_lost = amount
        currency = report.get("currency") or "USD"

    source_url = (
        "https://www.chainabuse.com/"
        + str(report.get("id", ""))
    )

    conn.execute("""
        INSERT OR IGNORE INTO scam_reports
        (
            domain,
            website_url,
            amount_lost,
            currency,
            report_date,
            category,
            description,
            source,
            source_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        domain,
        website_url,
        amount_lost,
        currency,
        report.get("reportedDate") or report.get("createdAt"),
        report.get("category"),
        report.get("description"),
        "Chainabuse",
        source_url
    ))

    conn.commit()
    conn.close()


def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=20
        )
    except Exception as e:
        print("Telegram error:", e)


def screen_domain(value):
    if not API_KEY:
        print("CHAINABUSE_API_KEY is missing from .env")
        return

    usage = load_usage()

    if usage["calls"] >= MAX_MONTHLY_CALLS:
        print(
            f"Monthly Chainabuse limit reached: "
            f"{usage['calls']}/{MAX_MONTHLY_CALLS}"
        )
        return

    domain, normalized_url = get_domain(value)

    print(f"\nChecking: {domain}")
    print(
        f"Chainabuse calls this month: "
        f"{usage['calls']}/{MAX_MONTHLY_CALLS}"
    )

    try:
        response = requests.get(
            API_URL,
            params={
                "domain": normalized_url,
                "perPage": 50
            },
            auth=(API_KEY, API_KEY),
            timeout=30
        )

        usage["calls"] += 1
        save_usage(usage)

    except requests.RequestException as e:
        print("Network error:", e)
        return

    print("HTTP Status:", response.status_code)

    if not response.ok:
        print("Chainabuse API error:")
        print(response.text)
        return

    try:
        data = response.json()
    except Exception:
        print("Invalid JSON response.")
        return

    reports = data.get("reports", [])
    count = data.get("count", len(reports))

    print(f"Reports found: {count}")

    if not reports:
        print("No Chainabuse reports were returned.")
        return

    saved = 0

    for report in reports:
        save_report(domain, report)
        saved += 1

    message = (
        "🚨 Chainabuse Alert\n\n"
        f"Domain: {domain}\n"
        f"Reports found: {count}\n"
        f"Reports processed: {saved}\n\n"
        f"Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    send_telegram(message)

    print(f"Processed {saved} report(s).")
    print("Telegram alert sent.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python chainabuse_monitor.py example.com")
        sys.exit(1)

    screen_domain(sys.argv[1])

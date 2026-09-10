import sqlite3
from parser import parse_report

DB_FILE = "scam_reports.db"

def save_report(text, source, source_url):
    report = parse_report(text)

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.execute("""
        INSERT OR IGNORE INTO scam_reports
        (domain, website_url, amount_lost, currency, report_date,
         category, description, source, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report["domain"],
        None,
        report["amount_lost"],
        report["currency"],
        report["report_date"],
        report["category"],
        report["description"],
        source,
        source_url
    ))

    conn.commit()

    if cursor.rowcount == 1:
        print("Report saved successfully.")
    else:
        print("Report already exists.")

    conn.close()

if __name__ == "__main__":
    sample_text = """
    I lost $5,000 to a crypto investment scam on 2026-09-10.
    The website was https://example-scam.com
    """

    save_report(
        sample_text,
        "TEST",
        "https://example.com/test-report-2"
    )

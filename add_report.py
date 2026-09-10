import sqlite3

DB_FILE = "scam_reports.db"

def add_report():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        INSERT OR IGNORE INTO scam_reports
        (domain, website_url, amount_lost, currency, report_date,
         category, description, source, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "example-scam.com",
        "https://example-scam.com",
        5000,
        "USD",
        "2026-09-10",
        "Investment Scam",
        "Example test report for the scam monitoring database.",
        "TEST",
        "https://example.com/test-report"
    ))

    conn.commit()
    conn.close()

    print("Test report saved successfully.")

if __name__ == "__main__":
    add_report()

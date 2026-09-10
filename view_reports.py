import sqlite3

conn = sqlite3.connect("scam_reports.db")

rows = conn.execute("""
    SELECT id, domain, amount_lost, currency, report_date,
           category, source, source_url
    FROM scam_reports
    ORDER BY id DESC
""").fetchall()

if not rows:
    print("No reports found.")
else:
    print(f"Found {len(rows)} report(s).\n")

    for row in rows:
        print("-" * 60)
        print(f"ID: {row[0]}")
        print(f"Domain: {row[1]}")
        print(f"Amount lost: {row[2]} {row[3] or ''}")
        print(f"Date: {row[4] or 'Unknown'}")
        print(f"Category: {row[5]}")
        print(f"Source: {row[6]}")
        print(f"Source URL: {row[7]}")

conn.close()

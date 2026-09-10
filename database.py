import sqlite3

DB_FILE = "scam_reports.db"

def create_database():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS scam_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            website_url TEXT,
            amount_lost REAL,
            currency TEXT,
            report_date TEXT,
            category TEXT,
            description TEXT,
            source TEXT,
            source_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source, source_url)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully.")

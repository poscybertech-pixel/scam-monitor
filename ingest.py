from save_report import save_report

def ingest_report(text, source, source_url):
    if not text.strip():
        print("Report text is empty.")
        return

    if not source.strip():
        print("Source is required.")
        return

    if not source_url.strip():
        print("Source URL is required.")
        return

    save_report(
        text=text,
        source=source,
        source_url=source_url
    )

if __name__ == "__main__":
    print("Scam Monitor - Report Ingestion Test")
    print("------------------------------------")

    text = input("Report text: ").strip()
    source = input("Source name: ").strip()
    source_url = input("Source URL: ").strip()

    ingest_report(text, source, source_url)

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CHAINABUSE_API_KEY")

url = "https://api.chainabuse.com/v0/reports"

domain = input("Enter a URL to check: ").strip()

if not domain.startswith(("http://", "https://")):
    domain = "https://" + domain

response = requests.get(
    url,
    params={
        "domain": domain,
        "perPage": 50
    },
    auth=(api_key, api_key),
    timeout=30
)

print("\nHTTP Status:", response.status_code)

if response.ok:
    data = response.json()
    print("API request successful.")
    print("Response received.")
    print(data)
else:
    print("API request failed.")
    print(response.text)

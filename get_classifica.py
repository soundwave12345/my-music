import os
import requests
import json

WRAPAPI_KEY = os.environ.get("WRAPAPI_KEY")

if not WRAPAPI_KEY:
    raise RuntimeError("❌ Environment variable WRAPAPI_KEY not set")

URL = f"https://wrapapi.com/use/soundwave/test/FIMI/0.1.0?wrapAPIKey={WRAPAPI_KEY}"

print("📡 Fetching FIMI chart data...")
response = requests.get(URL)
response.raise_for_status()

data = response.json()

if not data.get("success"):
    raise RuntimeError("⚠️ Failed to fetch chart data")

output_file = "/app/music/classifica_fimi.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Chart saved to {output_file}")

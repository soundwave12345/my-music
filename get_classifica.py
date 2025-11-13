import os
import requests
import json

WRAPAPI_KEY = os.environ.get("WRAPAPI_KEY")

if not WRAPAPI_KEY:
    raise RuntimeError("❌ Environment variable WRAPAPI_KEY not set")

URL = f"https://wrapapi.com/use/soundwave/test/FIMI/0.1.0?wrapAPIKey={WRAPAPI_KEY}"


OUTPUT_FILE = "classifica.txt"

def scarica_classifica():
    print("📡 Scarico la classifica FIMI...")
    r = requests.get(URL)
    r.raise_for_status()

    data = r.json()

    # Verifica struttura JSON
    if not data.get("success") or "data" not in data or "output" not in data["data"]:
        raise ValueError("Formato JSON inatteso.")

    # Estrae i brani
    output = data["data"]["output"]
    if not output or "canzone" not in output[0]:
        raise ValueError("Nessun brano trovato nel JSON.")

    canzoni = output[0]["canzone"]

    # Scrive il file classifica.txt
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for c in canzoni:
            titolo = c["titolo"].strip()
            autore = c["autore"].strip()
            f.write(f"{titolo} - {autore}\n")

    print(f"✅ Classifica salvata in: {OUTPUT_FILE}")
    print(f"📀 Totale brani: {len(canzoni)}")

if __name__ == "__main__":
    scarica_classifica()

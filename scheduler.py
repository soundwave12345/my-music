import schedule
import time
import subprocess

def aggiorna_classifica():
    print("⏰ Avvio aggiornamento classifica FIMI...")
    result = subprocess.run(["python", "get_classifica.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Errore:", result.stderr)

# Esegui subito al primo avvio
aggiorna_classifica()

# Pianifica ogni giorno alle 06:00
schedule.every().day.at("06:00").do(aggiorna_classifica)

print("🕓 Scheduler avviato: aggiornerà la classifica ogni giorno alle 06:00")

while True:
    schedule.run_pending()
    time.sleep(60)

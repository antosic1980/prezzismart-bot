import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = os.environ["TELEGRAM_CHANNEL"]

message = """
🚀 PREZZISMART

Il sistema automatico è online! 🤖

Questo è il primo messaggio pubblicato automaticamente dal nostro bot.

🔥 Presto arriveranno le migliori offerte Amazon.
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHANNEL,
        "text": message,
    },
    timeout=30,
)

response.raise_for_status()

print("Messaggio inviato correttamente!")

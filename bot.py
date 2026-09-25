import os
import json
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = os.environ["TELEGRAM_CHANNEL"]

with open("offers.json", "r", encoding="utf-8") as file:
    offers = json.load(file)


def calculate_discount(old_price, price):
    if old_price <= 0:
        return 0

    return round((old_price - price) / old_price * 100)


def create_message(offer):
    old_price = offer["old_price"]
    price = offer["price"]

    discount = calculate_discount(old_price, price)

    return f"""🔥 OFFERTA PREZZISMART

📦 {offer["name"]}

💰 Prezzo: €{price:.2f}
❌ Prezzo precedente: €{old_price:.2f}
📉 Sconto: -{discount}%

🏷️ Categoria: {offer["category"]}

👉 Vedi l'offerta:
{offer["url"]}

⚠️ Prezzo verificato al momento della pubblicazione.
"""


def send_message(message):
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


for offer in offers:

    discount = calculate_discount(
        offer["old_price"],
        offer["price"]
    )

    # Pubblica solamente offerte con almeno il 30% di sconto
    if discount >= 30:
        message = create_message(offer)
        send_message(message)
        print(f"Pubblicata offerta: {offer['name']}")
    else:
        print(f"Scartata: {offer['name']}")

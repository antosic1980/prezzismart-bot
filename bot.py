import os
import json
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = os.environ["TELEGRAM_CHANNEL"]

OFFERS_FILE = "offers.json"
PUBLISHED_FILE = "published.json"


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


# Legge le offerte
with open(OFFERS_FILE, "r", encoding="utf-8") as file:
    offers = json.load(file)


# Legge le offerte già pubblicate
with open(PUBLISHED_FILE, "r", encoding="utf-8") as file:
    published = json.load(file)


for offer in offers:

    offer_id = offer["id"]

    # Se già pubblicata, la saltiamo
    if offer_id in published:
        print(f"Già pubblicata: {offer['name']}")
        continue

    discount = calculate_discount(
        offer["old_price"],
        offer["price"]
    )

    # Pubblica solo offerte con almeno il 30% di sconto
    if discount >= 30:

        message = create_message(offer)

        send_message(message)

        published.append(offer_id)

        print(f"Pubblicata: {offer['name']}")

    else:
        print(f"Sconto insufficiente: {offer['name']}")


# Salva l'elenco aggiornato
with open(PUBLISHED_FILE, "w", encoding="utf-8") as file:
    json.dump(published, file, indent=2)

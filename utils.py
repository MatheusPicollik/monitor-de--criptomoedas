import requests
from plyer import notification

def get_price(coin, currency):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
        r = requests.get(url)
        data = r.json()
        return data[coin][currency]
    except:
        return None

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )
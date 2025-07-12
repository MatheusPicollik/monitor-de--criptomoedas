import threading
import time
from utils import get_price, notify
from historico import salvar_historico

def monitorar(coin, currency, target_price, label):
    while True:
        price = get_price(coin, currency)
        if price is None:
            label.configure(text=f"{coin}: erro ao buscar preço")
            break

        label.configure(text=f"{coin.capitalize()} atual: {price} {currency.upper()}")
        salvar_historico(coin, price)

        if price >= target_price:
            notify("🚨 Alerta Cripto", f"{coin.capitalize()} atingiu {price} {currency.upper()}!")
            break

        time.sleep(30)

def iniciar_monitoramento(coins_str, currency, target_price, label):
    coins = [c.strip().lower() for c in coins_str.split(",")]
    for coin in coins:
        thread = threading.Thread(target=monitorar, args=(coin, currency, target_price, label))
        thread.daemon = True
        thread.start()
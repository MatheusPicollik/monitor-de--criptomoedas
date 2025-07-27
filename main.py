import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd
import os
from tkinter import messagebox
from monitor import iniciar_monitoramento
from grafico import exibir_graficos
from config_window import ConfigWindow
from utils import get_price

import threading
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO

#app config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🚀 Alerta de Criptomoedas")
app.geometry("460x600")

#configuração padrão
config = {
    "coins": ["bitcoin"],
    "currencies": ["brl"],
    "volume": 50,
    "theme": "Dark"
}

titulo = ctk.CTkLabel(app, text="🔔 Monitor de Criptomoedas", font=ctk.CTkFont(size=20, weight="bold"))
titulo.pack(pady=15)

ctk.CTkLabel(app, text="Preço de alerta").pack()
price_entry = ctk.CTkEntry(app)
price_entry.insert(0, "300000")
price_entry.pack(pady=5)

status_label = ctk.CTkLabel(app, text="Status: aguardando...", text_color="gray")
status_label.pack(pady=15)

#funções principais
def iniciar():
    moedas = config["coins"]
    moedas_base = config["currencies"]
    try:
        preco_alvo = float(price_entry.get())
        status_label.configure(text="⏳ Monitorando...")

        for moeda in moedas:
            for base in moedas_base:
                iniciar_monitoramento(moeda, base, preco_alvo, status_label)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido para o preço.")

def abrir_graficos():
    moedas = config["coins"]
    exibir_graficos(moedas)

def abrir_configuracoes():
    def ao_salvar_configuracoes(dados):
        config.update(dados)
        ctk.set_appearance_mode(dados["theme"])
        status_label.configure(text=f"✔️ Configurações atualizadas")

    ConfigWindow(app, config_callback=ao_salvar_configuracoes)

#botões
ctk.CTkButton(app, text="Iniciar Monitoramento", command=iniciar).pack(pady=5)
ctk.CTkButton(app, text="📊 Ver Gráficos", command=abrir_graficos).pack(pady=5)
ctk.CTkButton(app, text="⚙️ Configurações", command=abrir_configuracoes).pack(pady=10)

#tabela
tabela_frame = ctk.CTkScrollableFrame(app, width=430, height=250)
tabela_frame.pack(pady=10)

labels_tabela = {}
precos_anteriores = {}

def obter_logo_url(moeda):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{moeda.lower()}")
        data = r.json()
        return data["image"]["thumb"]
    except:
        return None

def gerar_sparkline(coin, largura=80, altura=30):
    caminho = f"historico/{coin}.csv"
    if not os.path.exists(caminho):
        return None
    try:
        df = pd.read_csv(caminho)
        if "preco" not in df.columns:
            return None
        #pegar ultimos 30 pontos
        valores = df["preco"].tail(30).values
        if len(valores) < 2:
            return None

        fig, ax = plt.subplots(figsize=(largura/100, altura/100), dpi=100)
        ax.plot(valores, color="#00BFFF", linewidth=1.5)
        ax.axis("off")  #sem eixos
        fig.tight_layout(pad=0)

        #salvar na memoria
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)

        pil_img = Image.open(buf)
        return ImageTk.PhotoImage(pil_img)
    except Exception as e:
        print("Erro sparkline:", e)
        return None

def atualizar_tabela():
    while True:
        if not config["coins"] or not config["currencies"]:
            time.sleep(5)
            continue

        for coin in config["coins"]:
            for fiat in config["currencies"]:
                key = f"{coin}_{fiat}"
                preco = get_price(coin, fiat)
                if preco is None:
                    continue

                preco_anterior = precos_anteriores.get(key)
                cor = "white"
                seta = ""

                if preco_anterior is not None:
                    if preco > preco_anterior:
                        cor = "#00FF00"  #verde
                        seta = " ↑"
                    elif preco < preco_anterior:
                        cor = "#FF4040"  #vermelho
                        seta = " ↓"

                precos_anteriores[key] = preco
                texto = f"{coin.upper()} / {fiat.upper()}: {preco:.2f}{seta}"

                if key not in labels_tabela:
                    linha = ctk.CTkFrame(tabela_frame)
                    linha.pack(fill="x", padx=10, pady=2)

                    #icone da moeda
                    logo_url = obter_logo_url(coin)
                    if logo_url:
                        try:
                            img_data = requests.get(logo_url).content
                            pil_img = Image.open(BytesIO(img_data)).resize((20, 20))
                            img = ImageTk.PhotoImage(pil_img)
                            icon = ctk.CTkLabel(linha, image=img, text="")
                            icon.image = img
                            icon.pack(side="left", padx=5)
                        except:
                            pass

                    lbl = ctk.CTkLabel(linha, text=texto, font=ctk.CTkFont(size=12))
                    lbl.pack(side="left")
                    labels_tabela[key] = lbl
                spark_img = gerar_sparkline(coin)
                if spark_img:
                    spark_label = ctk.CTkLabel(linha, image=spark_img, text="")
                    spark_label.image = spark_img
                    spark_label.pack(side="right", padx=5)

        time.sleep(30)

threading.Thread(target=atualizar_tabela, daemon=True).start()

app.mainloop()
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
import os

plt.style.use("seaborn-v0_8-dark")

def exibir_graficos(coins):
    janela = ctk.CTkToplevel()
    janela.title("📊 Gráfico de Preços")
    janela.geometry("800x500")

    figura, ax = plt.subplots(figsize=(8, 4))
    houve_dados = False

    for coin in coins:
        caminho = f"historico/{coin}.csv"
        if not os.path.exists(caminho):
            continue

        df = pd.read_csv(caminho)
        df["data"] = pd.to_datetime(df["data"])

        ax.plot(df["data"], df["preco"], label=coin.capitalize(), linewidth=2)
        houve_dados = True

    if not houve_dados:
        ctk.CTkLabel(janela, text="Nenhum dado disponível.").pack(pady=20)
        return

    ax.set_title("Histórico de Preços", fontsize=14, weight="bold")
    ax.set_xlabel("Tempo", fontsize=10)
    ax.set_ylabel("Preço", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()

    canvas = FigureCanvasTkAgg(figura, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    toolbar_frame = ctk.CTkFrame(janela)
    toolbar_frame.pack(fill="x")
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
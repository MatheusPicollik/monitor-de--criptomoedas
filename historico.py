import pandas as pd
from datetime import datetime
import os

def salvar_historico(coin, price):
    os.makedirs("historico", exist_ok=True)
    arquivo = f"historico/{coin}.csv"
    tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame({"data": [tempo], "preco": [price]})
    try:
        df.to_csv(arquivo, mode="a", header=not os.path.exists(arquivo), index=False)
    except Exception as e:
        print("Erro ao salvar histórico:", e)
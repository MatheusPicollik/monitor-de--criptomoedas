import customtkinter as ctk

CRYPTO_OPCOES = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano", "bnb", "ripple"]
FIAT_OPCOES = ["brl", "usd", "eur", "gbp", "ars", "jpy"]

class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, parent, config_callback=None):
        super().__init__(parent)
        self.title("⚙️ Configurações")
        self.geometry("450x500")
        self.config_callback = config_callback
        self.crypto_vars = {}
        self.fiat_vars = {}
        self.build_interface()

    def build_interface(self):
        ctk.CTkLabel(self, text="Configurações do Aplicativo", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        #seletor de criptomoedas
        ctk.CTkLabel(self, text="Selecionar Criptomoedas").pack(pady=(5, 0))
        frame_crypto = ctk.CTkScrollableFrame(self, width=400, height=120)
        frame_crypto.pack(pady=5)
        for moeda in CRYPTO_OPCOES:
            var = ctk.BooleanVar(value=moeda == "bitcoin")
            checkbox = ctk.CTkCheckBox(frame_crypto, text=moeda.capitalize(), variable=var)
            checkbox.pack(anchor="w")
            self.crypto_vars[moeda] = var

        #seletor de moedas
        ctk.CTkLabel(self, text="Selecionar Moedas Fiat").pack(pady=(10, 0))
        frame_fiat = ctk.CTkScrollableFrame(self, width=400, height=100)
        frame_fiat.pack(pady=5)
        for moeda in FIAT_OPCOES:
            var = ctk.BooleanVar(value=moeda == "brl")
            checkbox = ctk.CTkCheckBox(frame_fiat, text=moeda.upper(), variable=var)
            checkbox.pack(anchor="w")
            self.fiat_vars[moeda] = var

        #tema
        ctk.CTkLabel(self, text="Tema").pack(pady=(15, 0))
        self.theme_option = ctk.CTkOptionMenu(self, values=["Dark", "Light"], command=ctk.set_appearance_mode)
        self.theme_option.set("Dark")
        self.theme_option.pack()

        #volume
        ctk.CTkLabel(self, text="Volume da notificação").pack(pady=(10, 0))
        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=10)
        self.volume_slider.set(50)
        self.volume_slider.pack()

        #botão salvar
        salvar = ctk.CTkButton(self, text="Salvar Configurações", command=self.salvar_config)
        salvar.pack(pady=20)

    def salvar_config(self):
        moedas_cripto = [moeda for moeda, var in self.crypto_vars.items() if var.get()]
        moedas_fiat = [moeda for moeda, var in self.fiat_vars.items() if var.get()]
        tema = self.theme_option.get()
        volume = int(self.volume_slider.get())

        config_data = {
            "coins": moedas_cripto,
            "currencies": moedas_fiat,
            "theme": tema,
            "volume": volume
        }

        if self.config_callback:
            self.config_callback(config_data)
        self.destroy()
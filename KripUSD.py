import customtkinter as ctk
import requests
from datetime import datetime
from PIL import Image


ctk.set_appearance_mode("dark")

LOGO_PATH = "logo2.jpeg"
SPLASH_TIME = 1000

TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
EXCHANGE_URL = "https://api.binance.com/api/v3/exchangeInfo"

# полные названия монет для красоты Binance их не отдаёт дополняем сами
FULL_NAMES = {
    "BTC": "Bitcoin", "ETH": "Ethereum", "BNB": "BNB", "SOL": "Solana",
    "ADA": "Cardano", "DOT": "Polkadot", "AVAX": "Avalanche",
    "XRP": "XRP", "DOGE": "Dogecoin", "TON": "Toncoin", "LTC": "Litecoin",
    "SHIB": "Shiba Inu", "TRX": "TRON", "LINK": "Chainlink",
    "MATIC": "Polygon", "POL": "Polygon (POL)",
    "UNI": "Uniswap", "ATOM": "Cosmos",
    "XLM": "Stellar", "ETC": "Ethereum Classic", "FIL": "Filecoin",
    "ARB": "Arbitrum", "OP": "Optimism", "NEAR": "NEAR Protocol",
    "APT": "Aptos", "SUI": "Sui", "PEPE": "Pepe",
    "ALGO": "Algorand", "VET": "VeChain", "ICP": "Internet Computer",
    "AAVE": "Aave", "INJ": "Injective", "RNDR": "Render", "FTM": "Fantom",
    "SAND": "The Sandbox", "MANA": "Decentraland", "AXS": "Axie Infinity",
    "GALA": "Gala", "EOS": "EOS", "XMR": "Monero", "BCH": "Bitcoin Cash",
    "DASH": "Dash", "ZEC": "Zcash", "EGLD": "MultiversX",
    "FLOW": "Flow", "HBAR": "Hedera", "TIA": "Celestia", "WLD": "Worldcoin",
}


def get_full_name(base):
    """возвращает полное название монеты, если оно есть в словаре"""
    if base in FULL_NAMES:
        return FULL_NAMES[base]
    return base


def load_all_bases():
    """загрузка списка монет"""
    try:
        r = requests.get(EXCHANGE_URL, timeout=10)
        bases = []
        for s in r.json()["symbols"]:
            if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
                b = s["baseAsset"]
                if b not in bases:
                    bases.append(b)
        return bases
    except Exception:
        return []


def get_coin_info(base):
    """спрашивает у Binance текущий курс монеты и курс 24 часа назад"""
    info = {}
    try:
        r = requests.get(TICKER_URL, params={"symbol": base + "USDT"}, timeout=5)
        t = r.json()
        info["price"] = float(t["lastPrice"])
        info["old_price"] = float(t["openPrice"])
        time = datetime.fromtimestamp(
            int(t["closeTime"]) / 1000)
        info["date_str"] = "Обновлено: " + time.strftime("%d.%m.%Y в %H:%M")
        info["error"] = ""
    except Exception:
        info["error"] = "Не удалось получить курс"
    return info


## ---------- Создаём окно ----------
root = ctk.CTk()
root.title("KripUSD — курсы криптовалют к USD")
root.geometry("420x490")
root.configure(fg_color="#151515")


## ---------- Заставка ----------
def show_splash():
    """создает заставку"""
    splash_frame = ctk.CTkFrame(root, fg_color="#151515", corner_radius=0)
    splash_frame.pack(fill="both", expand=True)

    logo_label = ctk.CTkLabel(splash_frame, text="")
    logo_label.place(relx=0.5, rely=0.5, anchor="center")

    img = Image.open(LOGO_PATH)
    logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
    logo_label.configure(image=logo_image)

    # через 1 секунду убрать заставку и показать интерфейс
    root.after(SPLASH_TIME, show_main)


## ---------- Основной интерфейс ----------
def show_main():
    """убирает заставку"""
    for child in root.winfo_children():
        child.destroy()


## ---------- Запуск ----------
show_splash()  # запуск заставки
root.mainloop()

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





## ---------- Создаём окно ----------
root = ctk.CTk()
root.title("KripUSD — курсы криптовалют к USD")
root.geometry("420x490")
root.configure(fg_color="#151515")


## ---------- Запуск ----------
root.mainloop()

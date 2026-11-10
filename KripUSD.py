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
    main_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="#202020",
                              border_width=2, border_color="#3a3a3a")
    main_frame.pack(pady=15, padx=20, fill="both", expand=True)

    ctk.CTkLabel(main_frame, text="Курс к USD",
                 font=("Helvetica", 24, "bold")).pack(pady=(20, 10))

    # первый ряд: чекбокс + список монет
    row1 = ctk.CTkFrame(main_frame, fg_color="transparent")
    row1.pack(pady=6, padx=15, fill="x")
    global var1, menu1  # без global Python посчитает var1 и menu1 локальными переменными
    var1 = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(row1, text="", variable=var1, width=30,
                    checkbox_width=22, checkbox_height=22,
                    fg_color="#7b1fa2", hover_color="#9c27b0").pack(side="left", padx=(0, 10))
    menu1 = ctk.CTkOptionMenu(row1, values=[""], font=("Arial", 13),
                              fg_color="#2b2b2b", button_color="#7b1fa2",
                              button_hover_color="#9c27b0")
    menu1.set("")
    menu1.pack(side="left", fill="x", expand=True)

    # второй ряд: чекбокс + список монет
    row2 = ctk.CTkFrame(main_frame, fg_color="transparent")
    row2.pack(pady=6, padx=15, fill="x")
    global var2, menu2, status_label
    var2 = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(row2, text="", variable=var2, width=30,
                    checkbox_width=22, checkbox_height=22,
                    fg_color="#7b1fa2", hover_color="#9c27b0").pack(side="left", padx=(0, 10))
    menu2 = ctk.CTkOptionMenu(row2, values=[""], font=("Arial", 13),
                              fg_color="#2b2b2b", button_color="#7b1fa2",
                              button_hover_color="#9c27b0")
    menu2.set("")
    menu2.pack(side="left", fill="x", expand=True)

    # кнопка и строка статуса
    ctk.CTkButton(main_frame, text="Показать курс", corner_radius=10,
                  height=40, fg_color="#7b1fa2", hover_color="#9c27b0",
                  command=open_results_window).pack(pady=18)

    status_label = ctk.CTkLabel(main_frame, text="Загружаем список монет...",
                                font=("Arial", 12), text_color="#a0a0a0")
    status_label.pack(pady=10)

    # скачиваем полный список монет
    bases = load_all_bases()
    if len(bases) == 0:
        status_label.configure(text="Нет соединения с Binance")
        return
    update_menus(bases)


def update_menus(bases):
    """заполнение выпадающих списков монетами"""
    values = [""]
    for b in bases:
        values.append(b + " — " + get_full_name(b))
    menu1.configure(values=values)
    menu2.configure(values=values)
    status_label.configure(text="Доступно монет: " + str(len(bases)))


def open_results_window():
    """обработка результата ввода монет"""
    selected = []  # сюда сложим монеты, которые пользователь отметил
    if var1.get() == True:  # проверяем галочку первого ряда, var1 видна без параметров она глобальная
        option = menu1.get()
        if option == "":  # защита от "нажал галочку и забыл выбрать"
            status_label.configure(text="Выберите монету в выпадающем списке")
            return
        selected.append(option)  # добавляем выбранный пункт целиком, вместе с названием BTC — Bitcoin
    if var2.get() == True:
        option = menu2.get()
        if option == "":
            status_label.configure(text="Выберите монету в выпадающем списке")
            return
        selected.append(option)

    if len(selected) == 0:  # обе галочки пустые: просим отметить хотя бы одну
        status_label.configure(text="Отметьте хотя бы одну монету")
        return

    status_label.configure(text="Загружаем курсы...")

    # новое окно с результатами
    win = ctk.CTkToplevel(root)
    win.title("Результаты — KripUSD")
    win.geometry("440x520")
    win.configure(fg_color="#151515")

    ctk.CTkLabel(win, text="Курсы к USD", font=("Helvetica", 22, "bold"),
                 text_color="#9c27b0").pack(pady=(20, 10))

    # показываем карточку для каждой выбранной монеты
    for option in selected:
        base = option.split(" — ")[0]
        show_coin_info(win, base)

    ctk.CTkButton(win, text="Закрыть", width=120, corner_radius=10,
                  fg_color="#7b1fa2", command=win.destroy).pack(pady=15)

    status_label.configure(text="Обновлено успешно")


def show_coin_info(win, base):
    """вывод результатов в отдельном окне"""
    info = get_coin_info(base)  # запрос к Binance

    block = ctk.CTkFrame(win, corner_radius=15, fg_color="#202020",
                         border_width=1, border_color="#3a3a3a")  #отдельный фрейм-«карточка» с рамкой под каждую монету
    block.pack(pady=8, padx=15, fill="x")

    if info["error"] != "":  # если при запросе случился сбой, вместо курса показываем красное сообщение
        ctk.CTkLabel(block, text=base + ": " + info["error"],
                     font=("Arial", 14), text_color="#f44336").pack(pady=10)
        return

    price = info["price"]
    old_price = info["old_price"]
    # текущий курс и время обновления
    ctk.CTkLabel(block, text=base + ": $" + str(round(price, 2)),
                 font=("Segoe UI", 22, "bold"), text_color="#9c27b0").pack(pady=(10, 2))  # крупная надпись
    ## «BTC: $64753.12»: округляем до 2 знаков и приклеиваем к коду валюты
    ctk.CTkLabel(block, text=info["date_str"],
                 font=("Segoe UI", 13, "italic"), text_color="#b39ddb").pack(pady=(0, 6))  # строка "Обновлено: …",
    ## подготовленная в get_coin_info

    # сравнение с курсом 24ч назад
    diff = price - old_price  # насколько курс изменился за сутки, положительное- вырос, отрицательное- упал
    pct = diff / old_price * 100  # то же самое в процентах, изменение 500 при цене 100000- это 0.5%

    if diff > 0:  # рост- зелёный треугольник вверх
        arrow = "▲"
        color = "#4caf50"
    elif diff < 0:  # падение- красный вниз
        arrow = "▼"
        color = "#f44336"
    else:  # без изменений- серый ромбик
        arrow = "►"
        color = "#a0a0a0"

    text = "24 ч назад ($" + str(round(old_price, 2)) + "):\n"
    text = text + arrow + " $" + str(round(abs(diff), 2)) + " | " + str(round(abs(pct), 2)) + "%"
    ctk.CTkLabel(block, text=text, font=("Arial", 13),
                 text_color=color, justify="center").pack(pady=(0, 10))


## ---------- Запуск ----------
show_splash()  # запуск заставки
root.mainloop()

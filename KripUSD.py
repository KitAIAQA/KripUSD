import customtkinter as ctk


ctk.set_appearance_mode("dark")


## ---------- Создаём окно ----------
root = ctk.CTk()
root.title("KripUSD — курсы криптовалют к USD")
root.geometry("420x490")
root.configure(fg_color="#151515")


## ---------- Запуск ----------
root.mainloop()

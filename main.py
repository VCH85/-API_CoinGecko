from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


url = "https://api.coingecko.com/api/v3/simple/price"

coin_api = {"bitcoin": "Биткойн","ethereum": "Эфириум","ripple": "Рипл","litecoin": "Лайткоин","cardano": "Кардано"}

currency_api = {"usd": "Доллар США (USD)","eur": "Евро (EUR)","rub": "Российский рубль (RUB)",
                "gbp": "Фунт стерлингов (GBP)", "cny": "Китайский юань (CNY)"}

def update_b_label(event):
    code = base_combobox.get()
    name = currency_api[code]
    b_label.config(text=name)


def update_t_label(event):
    code = target_combobox.get()
    name = coin_api[code]
    t_label.config(text=name)
def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()
    if target_code and base_code:
        try:
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={target_code}&vs_currencies={base_code}")
            response.raise_for_status()

            data = response.json()

            if 'error' not in data:
                price = data[target_code][base_code]
                base = coin_api[target_code]
                target = currency_api[base_code]
                mb.showinfo("Курс обмена", f"1 {target} = {price} {base}")
            else:
                mb.showerror("Ошибка", data['error']['message'])
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при получении данных: {e}")
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка", f"Проблема с подключением к API: {e}")
        target_combobox.delete(0, END)
        base_combobox.delete(0, END)


window = Tk()
window.title("Обменник24/7")
window.geometry("400x320")

Label(text="Целевая валюта:").pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(currency_api.keys()))
base_combobox.pack(padx =10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=5)

Label(text="Криптовалюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(coin_api.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=5)
Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=5)

window.mainloop()





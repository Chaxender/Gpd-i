import tkinter as tk
from tkinter import simpledialog
import json
import difflib
import random

# Veritabanını yükleme fonksiyonu
def load_database(filename="database.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# En yakın eşleşmeyi bulma fonksiyonu
def find_closest_match(user_input, database):
    closest_match = difflib.get_close_matches(user_input, database.keys(), n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None


# Botun cevabını alma fonksiyonu
def get_response(user_input, database):
    closest_match = find_closest_match(user_input, database)
    if closest_match:
        responses = database[closest_match]
        return random.choice(responses)
    else:
        return None


# Mesaj gönderme fonksiyonu
def send_message(event=None):
    user_input = entry.get()
    if user_input.strip() == "":
        return

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Gpd-i: " + user_input + "\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

    entry.delete(0, tk.END)

    response = get_response(user_input, database)
    if response:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Gpd-i: " + response + "\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)
    else:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END,
                        "Gpd-i: Maalesef Anlamadım...\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)


# Veritabanını yükle
database = load_database()

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Gpd-i")

chat_log = tk.Text(root, state=tk.DISABLED, width=50, height=20, wrap=tk.WORD)
chat_log.grid(row=0, column=0, columnspan=2)

entry = tk.Entry(root, width=40)
entry.grid(row=1, column=0, padx=10, pady=10)
entry.bind("<Return>", send_message)

send_button = tk.Button(root, text="Gönder", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()

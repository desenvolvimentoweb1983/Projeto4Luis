import requests
from tkinter import *
from tkinter import ttk

def obter_taxas_de_cambio(api_key):
    try:
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        response = requests.get(url)
        response.raise_for_status()  # Isso irá lançar uma exceção se houver um erro na requisição
        data = response.json()
        return data['conversion_rates']
    except requests.exceptions.RequestException as e:
        print("Erro ao obter taxas de câmbio:", e)
        return None

def converter_moeda(valor, moeda_origem, moeda_destino, taxas):
    if moeda_origem not in taxas or moeda_destino not in taxas:
        raise ValueError("Moeda não suportada")

    taxa_origem = taxas[moeda_origem]
    taxa_destino = taxas[moeda_destino]

    valor_em_usd = valor / taxa_origem
    valor_convertido = valor_em_usd * taxa_destino
    return valor_convertido

def converter_e_atualizar():
    valor_origem = float(entry_valor.get())
    moeda_origem = moeda_origem_var.get()
    moeda_destino = moeda_destino_var.get()

    try:
        resultado = converter_moeda(valor_origem, moeda_origem, moeda_destino, taxas_de_cambio)
        resultado_var.set(f"{valor_origem:.2f} {moeda_origem} equivalem a {resultado:.2f} {moeda_destino}")
    except ValueError as e:
        resultado_var.set(f"Erro: {e}")

api_key = 'a370a8b6aa5ff10e1b3e8948'

taxas_de_cambio = obter_taxas_de_cambio(api_key)

root = Tk()
root.title("PROJETO 4 MATCH! CONVERSOR DE MOEDAS")
root.geometry("430x300")
root.configure(bg="#000000")

frame = Frame(root, bg="#00FF00")
frame.pack(padx=10, pady=10)

valor_var = StringVar()
moeda_origem_var = StringVar()
moeda_destino_var = StringVar()
resultado_var = StringVar()

fonte_negrito = ("Helvetica", 12, "bold")

label_valor = Label(frame, text="Valor: ", font=fonte_negrito, bg="#00FF00", fg="black")
entry_valor = Entry(frame, textvariable=valor_var, font=fonte_negrito, bg="black", fg="#00FF00")

label_moeda_origem = Label(frame, text="Escolha uma Moeda: ", font=fonte_negrito, bg="#00FF00", fg="black")
option_moeda_origem = ttk.Combobox(frame, textvariable=moeda_origem_var, values=list(taxas_de_cambio.keys()), font=fonte_negrito, state="readonly")

label_moeda_destino = Label(frame, text="Moeda para conversão: ", font=fonte_negrito, bg="#00FF00", fg="black")
option_moeda_destino = ttk.Combobox(frame, textvariable=moeda_destino_var, values=list(taxas_de_cambio.keys()), font=fonte_negrito, state="readonly")

button_converter = Button(frame, text="$$$ CONVERTER $$$", command=converter_e_atualizar, font=fonte_negrito, fg="black", bg="#FFA500")
label_resultado = Label(frame, textvariable=resultado_var, font=fonte_negrito, bg="#00FF00", fg="black")

label_valor.grid(row=0, column=0, padx=5, pady=5)
entry_valor.grid(row=0, column=1, padx=5, pady=5)
label_moeda_origem.grid(row=1, column=0, padx=5, pady=5)
option_moeda_origem.grid(row=1, column=1, padx=5, pady=5)
label_moeda_destino.grid(row=2, column=0, padx=5, pady=5)
option_moeda_destino.grid(row=2, column=1, padx=5, pady=5)
button_converter.grid(row=3, column=0, columnspan=2, pady=10)
label_resultado.grid(row=4, column=0, columnspan=2)

root.mainloop()
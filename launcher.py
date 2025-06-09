import requests
import zipfile
import io
import os
import tkinter as tk
from tkinter import ttk, messagebox

VERSOES_URL = "https://pastebin.com/raw/gWf8ZxuG"  # JSON com as versões

def baixar_textura(url, destino):
    try:
        resposta = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(resposta.content)) as z:
            z.extractall(destino)
        messagebox.showinfo("Sucesso", "Textura instalada com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar a textura:\n{str(e)}")

def iniciar_download(versoes, versao_selecionada):
    url = versoes.get(versao_selecionada)
    if not url:
        messagebox.showerror("Erro", "Versão inválida.")
        return

    pasta_minecraft = os.path.expanduser("~/.minecraft/resourcepacks")
    os.makedirs(pasta_minecraft, exist_ok=True)
    baixar_textura(url, pasta_minecraft)

def carregar_versoes():
    try:
        dados = requests.get(VERSOES_URL).json()
        return dados["versoes"], dados["atual"]
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter as versões:\n{str(e)}")
        return {}, ""

def iniciar_interface():
    versoes, atual = carregar_versoes()

    root = tk.Tk()
    root.title("Launcher de Textura Minecraft")
    root.geometry("400x200")
    root.resizable(False, False)

    label = ttk.Label(root, text="Selecione a versão da textura:", font=("Arial", 12))
    label.pack(pady=10)

    combo = ttk.Combobox(root, values=list(versoes.keys()), font=("Arial", 10), state="readonly")
    combo.pack(pady=5)
    combo.set(atual)

    botao = ttk.Button(root, text="Instalar Textura", command=lambda: iniciar_download(versoes, combo.get()))
    botao.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()

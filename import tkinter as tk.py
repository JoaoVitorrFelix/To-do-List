import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# Caminho do arquivo
ARQUIVO = "tarefas.json"

# Carregar tarefas do arquivo (se existir)
def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Salvar tarefas no arquivo
def salvar_tarefas():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

# Atualiza a lista de tarefas na interface
def atualizar_lista():
    for widget in frame_lista.winfo_children():
        widget.destroy()

    for idx, tarefa in enumerate(tarefas):
        var_concluida = tk.BooleanVar(value=tarefa["concluida"])
        checkbox = tk.Checkbutton(frame_lista, text=tarefa["texto"], variable=var_concluida,
                                 onvalue=True, offvalue=False, command=lambda idx=idx, var=var_concluida: marcar_concluida(idx, var))
        checkbox.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

        # Marcar como concluída (alterar cor)
        if tarefa["concluida"]:
            checkbox.config(fg="green", font=("Arial", 10, "italic"))

        btn_remover = tk.Button(frame_lista, text="Remover", command=lambda idx=idx: remover_tarefa(idx))
        btn_remover.grid(row=idx, column=1, padx=10)

# Adiciona uma nova tarefa
def adicionar_tarefa():
    texto = entrada.get().strip()
    if texto:
        tarefa = {
            "texto": texto,
            "concluida": False,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tarefas.append(tarefa)
        tarefas.sort(key=lambda x: x["data"], reverse=False)  # Organizar por data
        entrada.delete(0, tk.END)
        salvar_tarefas()
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Digite uma tarefa antes de adicionar.")

# Marca uma tarefa como concluída
def marcar_concluida(idx, var):
    tarefas[idx]["concluida"] = var.get()
    salvar_tarefas()
    atualizar_lista()

# Remove a tarefa selecionada
def remover_tarefa(idx):
    del tarefas[idx]
    salvar_tarefas()
    atualizar_lista()

# Criar a janela principal
janela = tk.Tk()
janela.title("To-do List")
janela.geometry("500x400")
janela.resizable(False, False)

# Entrada de texto
entrada = tk.Entry(janela, font=("Arial", 12), width=30)
entrada.pack(pady=10)

# Botão de adicionar tarefas
btn_add = tk.Button(janela, text="Adicionar tarefa", command=adicionar_tarefa)
btn_add.pack()

# Frame para exibir tarefas
frame_lista = tk.Frame(janela)
frame_lista.pack(pady=10)

# Carregar e exibir tarefas ao iniciar
tarefas = carregar_tarefas()
atualizar_lista()

# Executar a interface
janela.mainloop()

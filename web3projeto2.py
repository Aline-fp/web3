import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# Função para conectar ao banco de dados 
def initialize_db():
    conn = sqlite3.connect('criancas.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='criancas'")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(criancas)")
        columns = cursor.fetchall()
        if any(column[1] == 'idade' for column in columns):
            cursor.execute("ALTER TABLE criancas RENAME TO criancas_old")
            cursor.execute('''
                CREATE TABLE criancas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    data_nascimento TEXT NOT NULL,
                    tipo_sanguineo TEXT NOT NULL,
                    alergias TEXT,
                    intolerancias TEXT,
                    telefone_responsaveis TEXT NOT NULL,
                    deficiencia TEXT,
                    nome_responsavel TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                INSERT INTO criancas (id, nome, cpf, endereco, data_nascimento, tipo_sanguineo, alergias, intolerancias, telefone_responsaveis, deficiencia, nome_responsavel)
                SELECT id, nome, cpf, endereco, data_nascimento, tipo_sanguineo, alergias, intolerancias, telefone_responsaveis, deficiencia, nome_responsavel
                FROM criancas_old
            ''')
            cursor.execute("DROP TABLE criancas_old")
    else:
        cursor.execute('''
            CREATE TABLE criancas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL,
                endereco TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                tipo_sanguineo TEXT NOT NULL,
                alergias TEXT,
                intolerancias TEXT,
                telefone_responsaveis TEXT NOT NULL,
                deficiencia TEXT,
                nome_responsavel TEXT NOT NULL
            )
        ''')

    conn.commit()
    conn.close()

def adicionar_crianca():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    endereco = entry_endereco.get()
    data_nascimento = entry_data_nascimento.get()
    tipo_sanguineo = entry_tipo_sanguineo.get()
    nome_responsavel = entry_nome_responsavel.get()
    telefone_responsaveis = entry_telefone_responsaveis.get()

    alergias = entry_alergias.get() if var_alergias.get() == "Sim" else "Nenhuma"
    intolerancias = entry_intolerancias.get() if var_intolerancias.get() == "Sim" else "Nenhuma"
    deficiencia = entry_deficiencia.get() if var_deficiencia.get() == "Sim" else "Nenhuma"

    if nome and cpf and endereco and data_nascimento and tipo_sanguineo and nome_responsavel and telefone_responsaveis:
        conn = sqlite3.connect('criancas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO criancas (nome, cpf, endereco, data_nascimento, tipo_sanguineo, alergias, intolerancias, telefone_responsaveis, deficiencia, nome_responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, endereco, data_nascimento, tipo_sanguineo, alergias, intolerancias, telefone_responsaveis, deficiencia, nome_responsavel))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Criança cadastrada com sucesso!")
        limpar_campos()
    else:
        messagebox.showwarning("Erro", "Todos os campos obrigatórios devem ser preenchidos.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_tipo_sanguineo.delete(0, tk.END)
    entry_nome_responsavel.delete(0, tk.END)
    entry_telefone_responsaveis.delete(0, tk.END)
    entry_alergias.delete(0, tk.END)
    entry_intolerancias.delete(0, tk.END)
    entry_deficiencia.delete(0, tk.END)
    var_alergias.set("Não")
    var_intolerancias.set("Não")
    var_deficiencia.set("Não")
    toggle_entry_state(entry_alergias, var_alergias)
    toggle_entry_state(entry_intolerancias, var_intolerancias)
    toggle_entry_state(entry_deficiencia, var_deficiencia)

def toggle_entry_state(entry, var):
    if var.get() == "Sim":
        entry.config(state="normal")
    else:
        entry.config(state="disabled")

def visualizar_criancas():
    conn = sqlite3.connect('criancas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM criancas')
    registros = cursor.fetchall()
    conn.close()

    janela_visualizar = tk.Toplevel()
    janela_visualizar.title("Visualizar Crianças")

    colunas = ["ID", "Nome", "CPF", "Endereço", "Data de Nascimento", "Tipo Sanguíneo",
               "Alergias", "Intolerâncias", "Telefone dos Responsáveis", "Deficiência", "Nome do Responsável"]
    for col, coluna in enumerate(colunas):
        ttk.Label(janela_visualizar, text=coluna, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=10, pady=5)

    for row, registro in enumerate(registros, start=1):
        for col, valor in enumerate(registro):
            ttk.Label(janela_visualizar, text=valor).grid(row=row, column=col, padx=10, pady=5)

def pesquisar_crianca():
    nome_pesquisa = entry_pesquisa.get()

    if nome_pesquisa:
        conn = sqlite3.connect('criancas.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM criancas WHERE nome LIKE ?', ('%' + nome_pesquisa + '%',))
        registros = cursor.fetchall()
        conn.close()

        janela_pesquisa = tk.Toplevel()
        janela_pesquisa.title("Resultados da Pesquisa")


        colunas = ["ID", "Nome", "CPF", "Endereço", "Data de Nascimento", "Tipo Sanguíneo",
                   "Alergias", "Intolerâncias", "Telefone dos Responsáveis", "Deficiência", "Nome do Responsável"]
        for col, coluna in enumerate(colunas):
            ttk.Label(janela_pesquisa, text=coluna, font=('Helvetica', 10, 'bold')).grid(row=0, column=col, padx=10, pady=5)

        for row, registro in enumerate(registros, start=1):
            for col, valor in enumerate(registro):
                ttk.Label(janela_pesquisa, text=valor).grid(row=row, column=col, padx=10, pady=5)
    else:
        messagebox.showwarning("Erro", "Por favor, insira um nome para pesquisar.")


#interface gráfica
root = tk.Tk()
root.title("Cadastro de Crianças")
root.geometry("900x600")

ttk.Label(root, text="Informações da Criança", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
ttk.Label(root, text="Dados da Saúde", font=('Helvetica', 12, 'bold')).grid(row=0, column=2, columnspan=2, padx=10, pady=10)
ttk.Label(root, text="Dados do Responsável", font=('Helvetica', 12, 'bold')).grid(row=0, column=4, columnspan=2, padx=10, pady=10)

ttk.Label(root, text="Nome Completo:").grid(row=1, column=0, padx=10, pady=10)
entry_nome = ttk.Entry(root)
entry_nome.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(root, text="CPF:").grid(row=2, column=0, padx=10, pady=10)
entry_cpf = ttk.Entry(root)
entry_cpf.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(root, text="Endereço:").grid(row=3, column=0, padx=10, pady=10)
entry_endereco = ttk.Entry(root)
entry_endereco.grid(row=3, column=1, padx=10, pady=10)

ttk.Label(root, text="Data de Nascimento:").grid(row=4, column=0, padx=10, pady=10)
entry_data_nascimento = ttk.Entry(root)
entry_data_nascimento.grid(row=4, column=1, padx=10, pady=10)

ttk.Label(root, text="Tipo Sanguíneo:").grid(row=5, column=0, padx=10, pady=10)
entry_tipo_sanguineo = ttk.Entry(root)
entry_tipo_sanguineo.grid(row=5, column=1, padx=10, pady=10)

ttk.Label(root, text="Alergias:").grid(row=1, column=2, padx=10, pady=10)
var_alergias = tk.StringVar(value="Não")
alergias_combobox = ttk.Combobox(root, textvariable=var_alergias, values=["Sim", "Não"])
alergias_combobox.grid(row=1, column=3, padx=10, pady=10)
alergias_combobox.bind("<<ComboboxSelected>>", lambda e: toggle_entry_state(entry_alergias, var_alergias))

ttk.Label(root, text="Quais:").grid(row=2, column=2, padx=10, pady=10)
entry_alergias = ttk.Entry(root, state="disabled")
entry_alergias.grid(row=2, column=3, padx=10, pady=10)

ttk.Label(root, text="Intolerâncias:").grid(row=3, column=2, padx=10, pady=10)
var_intolerancias = tk.StringVar(value="Não")
intolerancias_combobox = ttk.Combobox(root, textvariable=var_intolerancias, values=["Sim", "Não"])
intolerancias_combobox.grid(row=3, column=3, padx=10, pady=10)
intolerancias_combobox.bind("<<ComboboxSelected>>", lambda e: toggle_entry_state(entry_intolerancias, var_intolerancias))

ttk.Label(root, text="Quais:").grid(row=4, column=2, padx=10, pady=10)
entry_intolerancias = ttk.Entry(root, state="disabled")
entry_intolerancias.grid(row=4, column=3, padx=10, pady=10)

ttk.Label(root, text="Deficiência:").grid(row=5, column=2, padx=10, pady=10)
var_deficiencia = tk.StringVar(value="Não")
deficiencia_combobox = ttk.Combobox(root, textvariable=var_deficiencia, values=["Sim", "Não"])
deficiencia_combobox.grid(row=5, column=3, padx=10, pady=10)
deficiencia_combobox.bind("<<ComboboxSelected>>", lambda e: toggle_entry_state(entry_deficiencia, var_deficiencia))

ttk.Label(root, text="Quais:").grid(row=6, column=2, padx=10, pady=10)
entry_deficiencia = ttk.Entry(root, state="disabled")
entry_deficiencia.grid(row=6, column=3, padx=10, pady=10)

ttk.Label(root, text="Nome do Responsável:").grid(row=1, column=4, padx=10, pady=10)
entry_nome_responsavel = ttk.Entry(root)
entry_nome_responsavel.grid(row=1, column=5, padx=10, pady=10)

ttk.Label(root, text="Telefone dos Responsáveis:").grid(row=2, column=4, padx=10, pady=10)
entry_telefone_responsaveis = ttk.Entry(root)
entry_telefone_responsaveis.grid(row=2, column=5, padx=10, pady=10)

ttk.Button(root, text="Adicionar Criança", command=adicionar_crianca).grid(row=7, column=0, columnspan=2, padx=10, pady=10)
ttk.Button(root, text="Visualizar Crianças", command=visualizar_criancas).grid(row=7, column=2, columnspan=2, padx=10, pady=10)

ttk.Label(root, text="Pesquisar por Nome:").grid(row=8, column=0, padx=10, pady=10)
entry_pesquisa = ttk.Entry(root)
entry_pesquisa.grid(row=8, column=1, padx=10, pady=10)
ttk.Button(root, text="Pesquisar", command=pesquisar_crianca).grid(row=8, column=2, padx=10, pady=10)

initialize_db()

root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class AutorCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Autores")
        self.janela.geometry("400x300")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="Nome").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nome = tk.Entry(self.janela)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Sobrenome").grid(row=1, column=0, padx=10, pady=5)
        self.entry_sobrenome = tk.Entry(self.janela)
        self.entry_sobrenome.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Data de Nascimento (AAAA-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
        self.entry_data_nascimento = tk.Entry(self.janela)
        self.entry_data_nascimento.grid(row=2, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Autor", command=self.adicionar_autor, width=20)
        self.btn_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Autores", command=self.visualizar_autores, width=20)
        self.btn_visualizar.grid(row=4, column=0, columnspan=2, pady=10)

    def adicionar_autor(self):
        nome = self.entry_nome.get()
        sobrenome = self.entry_sobrenome.get()
        data_nascimento = self.entry_data_nascimento.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO AUTOR (PrimeiroNome, Sobrenome, DataNascimento) VALUES (?, ?, ?)",
                           (nome, sobrenome, data_nascimento))
            connection.commit()
            messagebox.showinfo("Sucesso", "Autor adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_nome.delete(0, tk.END)
        self.entry_sobrenome.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)

    def visualizar_autores(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM AUTOR")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Autores Cadastrados")
            janela_visualizacao.geometry("600x300")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("AutorID", "PrimeiroNome", "Sobrenome", "DataNascimento"), show="headings")
            tree.heading("AutorID", text="ID do Autor")
            tree.heading("PrimeiroNome", text="Primeiro Nome")
            tree.heading("Sobrenome", text="Sobrenome")
            tree.heading("DataNascimento", text="Data de Nascimento")

            # Definir tamanhos das colunas
            tree.column("AutorID", width=50)
            tree.column("PrimeiroNome", width=150)
            tree.column("Sobrenome", width=150)
            tree.column("DataNascimento", width=100)

            # Adicionar dados à tabela
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class ClienteCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Clientes")
        self.janela.geometry("400x500")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="Primeiro Nome").grid(row=0, column=0, padx=10, pady=5)
        self.entry_primeiro_nome = tk.Entry(self.janela)
        self.entry_primeiro_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Sobrenome").grid(row=1, column=0, padx=10, pady=5)
        self.entry_sobrenome = tk.Entry(self.janela)
        self.entry_sobrenome.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Email").grid(row=2, column=0, padx=10, pady=5)
        self.entry_email = tk.Entry(self.janela)
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Telefone").grid(row=3, column=0, padx=10, pady=5)
        self.entry_telefone = tk.Entry(self.janela)
        self.entry_telefone.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Endereço").grid(row=4, column=0, padx=10, pady=5)
        self.entry_endereco = tk.Entry(self.janela)
        self.entry_endereco.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Cliente", command=self.adicionar_cliente, width=20)
        self.btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Clientes", command=self.visualizar_clientes, width=20)
        self.btn_visualizar.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão para visualizar o código-fonte
        self.btn_ver_codigo = tk.Button(self.janela, text="Visualizar Código", command=self.visualizar_codigo, width=20)
        self.btn_ver_codigo.grid(row=7, column=0, columnspan=2, pady=10)

    def adicionar_cliente(self):
        primeiro_nome = self.entry_primeiro_nome.get()
        sobrenome = self.entry_sobrenome.get()
        email = self.entry_email.get()
        telefone = self.entry_telefone.get()
        endereco = self.entry_endereco.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO CLIENTE (PrimeiroNome, Sobrenome, Email, Telefone, Endereco) VALUES (?, ?, ?, ?, ?)",
                           (primeiro_nome, sobrenome, email, telefone, endereco))
            connection.commit()
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_primeiro_nome.delete(0, tk.END)
        self.entry_sobrenome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)

    def visualizar_clientes(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM CLIENTE")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Clientes Cadastrados")
            janela_visualizacao.geometry("600x300")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("ClienteID", "PrimeiroNome", "Sobrenome", "Email", "Telefone", "Endereco"), show="headings")
            tree.heading("ClienteID", text="ID do Cliente")
            tree.heading("PrimeiroNome", text="Primeiro Nome")
            tree.heading("Sobrenome", text="Sobrenome")
            tree.heading("Email", text="Email")
            tree.heading("Telefone", text="Telefone")
            tree.heading("Endereco", text="Endereço")

            # Definir tamanhos das colunas
            tree.column("ClienteID", width=50)
            tree.column("PrimeiroNome", width=100)
            tree.column("Sobrenome", width=100)
            tree.column("Email", width=150)
            tree.column("Telefone", width=100)
            tree.column("Endereco", width=150)

            # Adicionar dados à tabela
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

    def visualizar_codigo(self):
        janela_codigo = tk.Toplevel(self.janela)
        janela_codigo.title("Código Fonte - Cliente CRUD")
        janela_codigo.geometry("700x500")

        # Caixa de texto para exibir o código-fonte
        txt_codigo = tk.Text(janela_codigo, wrap="word")
        txt_codigo.pack(expand=True, fill="both")

        # Carregar e exibir o código-fonte
        try:
            with open(__file__, 'r', encoding='utf-8') as f:
                codigo = f.read()
                txt_codigo.insert(tk.END, codigo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o código-fonte: {e}")


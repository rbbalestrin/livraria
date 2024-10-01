import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class EditoraCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Editoras")
        self.janela.geometry("400x300")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="Nome da Editora").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nome = tk.Entry(self.janela)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Endereço").grid(row=1, column=0, padx=10, pady=5)
        self.entry_endereco = tk.Entry(self.janela)
        self.entry_endereco.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Telefone").grid(row=2, column=0, padx=10, pady=5)
        self.entry_telefone = tk.Entry(self.janela)
        self.entry_telefone.grid(row=2, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Editora", command=self.adicionar_editora, width=20)
        self.btn_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Editoras", command=self.visualizar_editoras, width=20)
        self.btn_visualizar.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_ver_codigo = tk.Button(self.janela, text="Visualizar Código", command=self.visualizar_codigo, width=20)
        self.btn_ver_codigo.grid(row=5, column=0, columnspan=2, pady=10)


    def adicionar_editora(self):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO EDITORA (Nome, Endereco, Telefone) VALUES (?, ?, ?)",
                           (nome, endereco, telefone))
            connection.commit()
            messagebox.showinfo("Sucesso", "Editora adicionada com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_nome.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)

    def visualizar_editoras(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM EDITORA")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Editoras Cadastradas")
            janela_visualizacao.geometry("600x300")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("EditoraID", "Nome", "Endereco", "Telefone"), show="headings")
            tree.heading("EditoraID", text="ID da Editora")
            tree.heading("Nome", text="Nome")
            tree.heading("Endereco", text="Endereço")
            tree.heading("Telefone", text="Telefone")

            # Definir tamanhos das colunas
            tree.column("EditoraID", width=50)
            tree.column("Nome", width=150)
            tree.column("Endereco", width=150)
            tree.column("Telefone", width=100)

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
        janela_codigo.title("Código Fonte - Editoras CRUD")
        janela_codigo.geometry("700x500")

        txt_codigo = tk.Text(janela_codigo, wrap="word")
        txt_codigo.pack(expand=True, fill="both")

        try:
            with open(__file__, 'r', encoding='utf-8') as f:
                codigo = f.read()
                txt_codigo.insert(tk.END, codigo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o código-fonte: {e}")

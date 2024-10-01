import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class LivroCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Livros")
        self.janela.geometry("400x400")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="Título").grid(row=0, column=0, padx=10, pady=5)
        self.entry_titulo = tk.Entry(self.janela)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="ID da Editora").grid(row=1, column=0, padx=10, pady=5)
        self.entry_editora_id = tk.Entry(self.janela)
        self.entry_editora_id.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Data de Publicação (AAAA-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
        self.entry_data_publicacao = tk.Entry(self.janela)
        self.entry_data_publicacao.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Preço").grid(row=3, column=0, padx=10, pady=5)
        self.entry_preco = tk.Entry(self.janela)
        self.entry_preco.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Quantidade em Estoque").grid(row=4, column=0, padx=10, pady=5)
        self.entry_quantidade_estoque = tk.Entry(self.janela)
        self.entry_quantidade_estoque.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Livro", command=self.adicionar_livro, width=20)
        self.btn_adicionar.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Livros", command=self.visualizar_livros, width=20)
        self.btn_visualizar.grid(row=6, column=0, columnspan=2, pady=10)

    def adicionar_livro(self):
        titulo = self.entry_titulo.get()
        editora_id = self.entry_editora_id.get()
        data_publicacao = self.entry_data_publicacao.get()
        preco = self.entry_preco.get()
        quantidade_estoque = self.entry_quantidade_estoque.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO LIVRO (Titulo, EditoraID, DataPublicacao, Preco, QuantidadeEstoque) VALUES (?, ?, ?, ?, ?)",
                           (titulo, editora_id, data_publicacao, preco, quantidade_estoque))
            connection.commit()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_titulo.delete(0, tk.END)
        self.entry_editora_id.delete(0, tk.END)
        self.entry_data_publicacao.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_quantidade_estoque.delete(0, tk.END)

    def visualizar_livros(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM LIVRO")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Livros Cadastrados")
            janela_visualizacao.geometry("800x400")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("LivroID", "Titulo", "EditoraID", "DataPublicacao", "Preco", "QuantidadeEstoque"), show="headings")
            tree.heading("LivroID", text="ID do Livro")
            tree.heading("Titulo", text="Título")
            tree.heading("EditoraID", text="ID da Editora")
            tree.heading("DataPublicacao", text="Data de Publicação")
            tree.heading("Preco", text="Preço")
            tree.heading("QuantidadeEstoque", text="Quantidade em Estoque")

            # Definir tamanhos das colunas
            tree.column("LivroID", width=50)
            tree.column("Titulo", width=150)
            tree.column("EditoraID", width=100)
            tree.column("DataPublicacao", width=100)
            tree.column("Preco", width=100)
            tree.column("QuantidadeEstoque", width=100)

            # Adicionar dados à tabela
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

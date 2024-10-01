import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class ItemPedidoCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Itens do Pedido")
        self.janela.geometry("400x350")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="ID do Pedido").grid(row=0, column=0, padx=10, pady=5)
        self.entry_pedido_id = tk.Entry(self.janela)
        self.entry_pedido_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="ID do Livro").grid(row=1, column=0, padx=10, pady=5)
        self.entry_livro_id = tk.Entry(self.janela)
        self.entry_livro_id.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Quantidade").grid(row=2, column=0, padx=10, pady=5)
        self.entry_quantidade = tk.Entry(self.janela)
        self.entry_quantidade.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Preço Unitário").grid(row=3, column=0, padx=10, pady=5)
        self.entry_preco = tk.Entry(self.janela)
        self.entry_preco.grid(row=3, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Item ao Pedido", command=self.adicionar_item_pedido, width=25)
        self.btn_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Itens do Pedido", command=self.visualizar_itens_pedido, width=25)
        self.btn_visualizar.grid(row=5, column=0, columnspan=2, pady=10)

    def adicionar_item_pedido(self):
        pedido_id = self.entry_pedido_id.get()
        livro_id = self.entry_livro_id.get()
        quantidade = self.entry_quantidade.get()
        preco = self.entry_preco.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO ITEM_PEDIDO (PedidoID, LivroID, Quantidade, PrecoUnitario) VALUES (?, ?, ?, ?)",
                           (pedido_id, livro_id, quantidade, preco))
            connection.commit()
            messagebox.showinfo("Sucesso", "Item do pedido adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_pedido_id.delete(0, tk.END)
        self.entry_livro_id.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)

    def visualizar_itens_pedido(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM ITEM_PEDIDO")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Itens do Pedido Cadastrados")
            janela_visualizacao.geometry("600x350")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("PedidoID", "LivroID", "Quantidade", "PrecoUnitario"), show="headings")
            tree.heading("PedidoID", text="ID do Pedido")
            tree.heading("LivroID", text="ID do Livro")
            tree.heading("Quantidade", text="Quantidade")
            tree.heading("PrecoUnitario", text="Preço Unitário")

            # Definir tamanhos das colunas
            tree.column("PedidoID", width=100)
            tree.column("LivroID", width=100)
            tree.column("Quantidade", width=100)
            tree.column("PrecoUnitario", width=100)

            # Adicionar dados à tabela
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

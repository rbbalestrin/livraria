import tkinter as tk
from tkinter import messagebox, ttk
from utils import get_connection

class PedidoCRUD:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerenciar Pedidos")
        self.janela.geometry("400x300")

        # Labels e Widgets de Entrada
        tk.Label(self.janela, text="ID do Cliente").grid(row=0, column=0, padx=10, pady=5)
        self.entry_cliente_id = tk.Entry(self.janela)
        self.entry_cliente_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.janela, text="Data do Pedido (AAAA-MM-DD)").grid(row=1, column=0, padx=10, pady=5)
        self.entry_data_pedido = tk.Entry(self.janela)
        self.entry_data_pedido.grid(row=1, column=1, padx=10, pady=5)

        # Botões
        self.btn_adicionar = tk.Button(self.janela, text="Adicionar Pedido", command=self.adicionar_pedido, width=20)
        self.btn_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_visualizar = tk.Button(self.janela, text="Visualizar Pedidos", command=self.visualizar_pedidos, width=20)
        self.btn_visualizar.grid(row=3, column=0, columnspan=2, pady=10)

    def adicionar_pedido(self):
        cliente_id = self.entry_cliente_id.get()
        data_pedido = self.entry_data_pedido.get()

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO PEDIDO (ClienteID, DataPedido) VALUES (?, ?)",
                           (cliente_id, data_pedido))
            connection.commit()
            messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

        # Limpar entradas
        self.entry_cliente_id.delete(0, tk.END)
        self.entry_data_pedido.delete(0, tk.END)

    def visualizar_pedidos(self):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM PEDIDO")
            rows = cursor.fetchall()

            # Criar nova janela para mostrar os dados
            janela_visualizacao = tk.Toplevel(self.janela)
            janela_visualizacao.title("Pedidos Cadastrados")
            janela_visualizacao.geometry("600x300")

            # Criar Treeview para mostrar os dados em tabela
            tree = ttk.Treeview(janela_visualizacao, columns=("PedidoID", "ClienteID", "DataPedido", "ValorTotal"), show="headings")
            tree.heading("PedidoID", text="ID do Pedido")
            tree.heading("ClienteID", text="ID do Cliente")
            tree.heading("DataPedido", text="Data do Pedido")
            tree.heading("ValorTotal", text="Valor Total")

            # Definir tamanhos das colunas
            tree.column("PedidoID", width=50)
            tree.column("ClienteID", width=100)
            tree.column("DataPedido", width=100)
            tree.column("ValorTotal", width=100)

            # Adicionar dados à tabela
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            connection.close()

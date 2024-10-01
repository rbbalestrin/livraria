import tkinter as tk
from tkinter import ttk, messagebox
from utils import get_connection

class Relatorios:
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Gerar Relatórios")
        self.janela.geometry("500x400")

        # Botões para cada relatório
        self.btn_pedidos_por_cliente = tk.Button(self.janela, text="Pedidos por Cliente", command=self.relatorio_pedidos_por_cliente, width=30)
        self.btn_pedidos_por_cliente.pack(pady=10)

        self.btn_livros_por_editora = tk.Button(self.janela, text="Livros por Editora", command=self.relatorio_livros_por_editora, width=30)
        self.btn_livros_por_editora.pack(pady=10)

        self.btn_pedidos_por_periodo = tk.Button(self.janela, text="Pedidos por Período", command=self.relatorio_pedidos_por_periodo, width=30)
        self.btn_pedidos_por_periodo.pack(pady=10)

        self.btn_ver_codigo = tk.Button(self.janela, text="Visualizar Código", command=self.visualizar_codigo, width=20)
        self.btn_ver_codigo.grid(row=5, column=0, columnspan=2, pady=10)

    def relatorio_pedidos_por_cliente(self):
        # Entrada do cliente ID
        janela_entrada = tk.Toplevel(self.janela)
        janela_entrada.title("Relatório: Pedidos por Cliente")
        tk.Label(janela_entrada, text="Digite o ID do Cliente:").pack(pady=5)
        entry_cliente_id = tk.Entry(janela_entrada)
        entry_cliente_id.pack(pady=5)

        def gerar_relatorio():
            cliente_id = entry_cliente_id.get()
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("SELECT * FROM PEDIDO WHERE ClienteID = ?", (cliente_id,))
                rows = cursor.fetchall()

                # Criar nova janela para mostrar os dados
                janela_visualizacao = tk.Toplevel(janela_entrada)
                janela_visualizacao.title("Pedidos do Cliente")
                janela_visualizacao.geometry("600x300")

                # Criar Treeview para mostrar os dados em tabela
                tree = ttk.Treeview(janela_visualizacao, columns=("PedidoID", "ClienteID", "DataPedido", "ValorTotal"), show="headings")
                tree.heading("PedidoID", text="ID do Pedido")
                tree.heading("ClienteID", text="ID do Cliente")
                tree.heading("DataPedido", text="Data do Pedido")
                tree.heading("ValorTotal", text="Valor Total")

                # Adicionar dados à tabela
                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill="both", expand=True)

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            finally:
                connection.close()

        tk.Button(janela_entrada, text="Gerar Relatório", command=gerar_relatorio).pack(pady=10)

    def relatorio_livros_por_editora(self):
        # Entrada do Editora ID
        janela_entrada = tk.Toplevel(self.janela)
        janela_entrada.title("Relatório: Livros por Editora")
        tk.Label(janela_entrada, text="Digite o ID da Editora:").pack(pady=5)
        entry_editora_id = tk.Entry(janela_entrada)
        entry_editora_id.pack(pady=5)

        def gerar_relatorio():
            editora_id = entry_editora_id.get()
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("SELECT * FROM LIVRO WHERE EditoraID = ?", (editora_id,))
                rows = cursor.fetchall()

                # Criar nova janela para mostrar os dados
                janela_visualizacao = tk.Toplevel(janela_entrada)
                janela_visualizacao.title("Livros da Editora")
                janela_visualizacao.geometry("600x300")

                # Criar Treeview para mostrar os dados em tabela
                tree = ttk.Treeview(janela_visualizacao, columns=("LivroID", "Titulo", "EditoraID", "DataPublicacao", "Preco", "QuantidadeEstoque"), show="headings")
                tree.heading("LivroID", text="ID do Livro")
                tree.heading("Titulo", text="Título")
                tree.heading("EditoraID", text="ID da Editora")
                tree.heading("DataPublicacao", text="Data de Publicação")
                tree.heading("Preco", text="Preço")
                tree.heading("QuantidadeEstoque", text="Quantidade em Estoque")

                # Adicionar dados à tabela
                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill="both", expand=True)

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            finally:
                connection.close()

        tk.Button(janela_entrada, text="Gerar Relatório", command=gerar_relatorio).pack(pady=10)

    def relatorio_pedidos_por_periodo(self):
        # Entrada de intervalo de datas
        janela_entrada = tk.Toplevel(self.janela)
        janela_entrada.title("Relatório: Pedidos por Período")
        tk.Label(janela_entrada, text="Data Inicial (AAAA-MM-DD):").pack(pady=5)
        entry_data_inicial = tk.Entry(janela_entrada)
        entry_data_inicial.pack(pady=5)
        tk.Label(janela_entrada, text="Data Final (AAAA-MM-DD):").pack(pady=5)
        entry_data_final = tk.Entry(janela_entrada)
        entry_data_final.pack(pady=5)

        def gerar_relatorio():
            data_inicial = entry_data_inicial.get()
            data_final = entry_data_final.get()
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("SELECT * FROM PEDIDO WHERE DataPedido BETWEEN ? AND ?", (data_inicial, data_final))
                rows = cursor.fetchall()

                # Criar nova janela para mostrar os dados
                janela_visualizacao = tk.Toplevel(janela_entrada)
                janela_visualizacao.title("Pedidos por Período")
                janela_visualizacao.geometry("600x300")

                # Criar Treeview para mostrar os dados em tabela
                tree = ttk.Treeview(janela_visualizacao, columns=("PedidoID", "ClienteID", "DataPedido", "ValorTotal"), show="headings")
                tree.heading("PedidoID", text="ID do Pedido")
                tree.heading("ClienteID", text="ID do Cliente")
                tree.heading("DataPedido", text="Data do Pedido")
                tree.heading("ValorTotal", text="Valor Total")

                # Adicionar dados à tabela
                for row in rows:
                    tree.insert("", "end", values=row)

                tree.pack(fill="both", expand=True)

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            finally:
                connection.close()

        tk.Button(janela_entrada, text="Gerar Relatório", command=gerar_relatorio).pack(pady=10)

    def visualizar_codigo(self):
        janela_codigo = tk.Toplevel(self.janela)
        janela_codigo.title("Código Fonte - Relatorios")
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


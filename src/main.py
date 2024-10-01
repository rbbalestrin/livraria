import tkinter as tk
from tkinter import messagebox, ttk
from cliente_crud import ClienteCRUD
from autor_crud import AutorCRUD
from editora_crud import EditoraCRUD
from livro_crud import LivroCRUD
from pedido_crud import PedidoCRUD
from item_pedido_crud import ItemPedidoCRUD
from relatorios import Relatorios
from procedures import calcular_total_vendas_cliente, buscar_livros_por_autor, adicionar_pedido_com_itens

class SistemaLivrariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Livraria")

        # Tamanho da janela
        self.root.geometry("400x600")

        # Botões para cada entidade
        self.btn_gerenciar_clientes = tk.Button(self.root, text="Gerenciar Clientes", command=self.abrir_cliente_crud, width=30, height=2)
        self.btn_gerenciar_clientes.pack(pady=10)

        self.btn_gerenciar_autores = tk.Button(self.root, text="Gerenciar Autores", command=self.abrir_autor_crud, width=30, height=2)
        self.btn_gerenciar_autores.pack(pady=10)

        self.btn_gerenciar_editoras = tk.Button(self.root, text="Gerenciar Editoras", command=self.abrir_editora_crud, width=30, height=2)
        self.btn_gerenciar_editoras.pack(pady=10)

        self.btn_gerenciar_livros = tk.Button(self.root, text="Gerenciar Livros", command=self.abrir_livro_crud, width=30, height=2)
        self.btn_gerenciar_livros.pack(pady=10)

        self.btn_gerenciar_pedidos = tk.Button(self.root, text="Gerenciar Pedidos", command=self.abrir_pedido_crud, width=30, height=2)
        self.btn_gerenciar_pedidos.pack(pady=10)

        self.btn_gerenciar_itens_pedido = tk.Button(self.root, text="Gerenciar Itens do Pedido", command=self.abrir_item_pedido_crud, width=30, height=2)
        self.btn_gerenciar_itens_pedido.pack(pady=10)

        # Botão para relatórios
        self.btn_gerar_relatorios = tk.Button(self.root, text="Gerar Relatórios", command=self.abrir_relatorios, width=30, height=2)
        self.btn_gerar_relatorios.pack(pady=10)

        # Botão para simular Stored Procedures
        self.btn_simular_procedures = tk.Button(self.root, text="Operações Especiais", command=self.operacoes_especiais, width=30, height=2)
        self.btn_simular_procedures.pack(pady=10)

    def abrir_cliente_crud(self):
        ClienteCRUD(self.root)

    def abrir_autor_crud(self):
        AutorCRUD(self.root)

    def abrir_editora_crud(self):
        EditoraCRUD(self.root)

    def abrir_livro_crud(self):
        LivroCRUD(self.root)

    def abrir_pedido_crud(self):
        PedidoCRUD(self.root)

    def abrir_item_pedido_crud(self):
        ItemPedidoCRUD(self.root)

    def abrir_relatorios(self):
        Relatorios(self.root)

    def operacoes_especiais(self):
        janela_operacoes = tk.Toplevel(self.root)
        janela_operacoes.title("Operações Especiais")
        janela_operacoes.geometry("400x300")

        # Calcular total de vendas por cliente
        tk.Label(janela_operacoes, text="ID do Cliente para Total de Vendas:").pack(pady=5)
        entry_cliente_id = tk.Entry(janela_operacoes)
        entry_cliente_id.pack(pady=5)

        def mostrar_total_vendas():
            cliente_id = entry_cliente_id.get()
            total_vendas = calcular_total_vendas_cliente(cliente_id)
            messagebox.showinfo("Total de Vendas", f"Total de Vendas do Cliente {cliente_id}: {total_vendas}")

        btn_calcular_total = tk.Button(janela_operacoes, text="Calcular Total de Vendas", command=mostrar_total_vendas)
        btn_calcular_total.pack(pady=10)

        # Botão para buscar livros por autor
        tk.Label(janela_operacoes, text="Nome do Autor para Buscar Livros:").pack(pady=5)
        entry_autor_nome = tk.Entry(janela_operacoes)
        entry_autor_nome.pack(pady=5)

        def mostrar_livros_autor():
            autor_nome = entry_autor_nome.get()
            livros = buscar_livros_por_autor(autor_nome)
            if livros:
                janela_livros = tk.Toplevel(janela_operacoes)
                janela_livros.title(f"Livros de {autor_nome}")
                janela_livros.geometry("600x300")

                tree = ttk.Treeview(janela_livros, columns=("LivroID", "Titulo", "DataPublicacao", "Preco"), show="headings")
                tree.heading("LivroID", text="ID do Livro")
                tree.heading("Titulo", text="Título")
                tree.heading("DataPublicacao", text="Data de Publicação")
                tree.heading("Preco", text="Preço")

                # Adicionar dados à tabela
                for livro in livros:
                    tree.insert("", "end", values=livro)

                tree.pack(fill="both", expand=True)
            else:
                messagebox.showinfo("Resultado", f"Nenhum livro encontrado para o autor '{autor_nome}'.")

        btn_buscar_livros = tk.Button(janela_operacoes, text="Buscar Livros por Autor", command=mostrar_livros_autor)
        btn_buscar_livros.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaLivrariaApp(root)
    root.mainloop()

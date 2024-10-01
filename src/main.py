import tkinter as tk
from cliente_crud import ClienteCRUD
from autor_crud import AutorCRUD
from editora_crud import EditoraCRUD
from livro_crud import LivroCRUD
from pedido_crud import PedidoCRUD
from item_pedido_crud import ItemPedidoCRUD
from relatorios import Relatorios

class SistemaLivrariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Livraria")

        # Tamanho da janela
        self.root.geometry("400x500")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaLivrariaApp(root)
    root.mainloop()

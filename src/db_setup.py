import sqlite3

def create_tables():
    connection = sqlite3.connect('C:/.code/livraria/database/livraria.db')
    cursor = connection.cursor()

    # CLIENTE table
    cursor.execute('''CREATE TABLE IF NOT EXISTS CLIENTE (
                        ClienteID INTEGER PRIMARY KEY,
                        PrimeiroNome TEXT NOT NULL,
                        Sobrenome TEXT NOT NULL,
                        Email TEXT UNIQUE NOT NULL,
                        Telefone TEXT,
                        Endereco TEXT)''')

    # AUTOR table
    cursor.execute('''CREATE TABLE IF NOT EXISTS AUTOR (
                        AutorID INTEGER PRIMARY KEY,
                        PrimeiroNome TEXT NOT NULL,
                        Sobrenome TEXT NOT NULL,
                        DataNascimento DATE)''')

    # EDITORA table
    cursor.execute('''CREATE TABLE IF NOT EXISTS EDITORA (
                        EditoraID INTEGER PRIMARY KEY,
                        Nome TEXT NOT NULL,
                        Endereco TEXT,
                        Telefone TEXT)''')

    # LIVRO table
    cursor.execute('''CREATE TABLE IF NOT EXISTS LIVRO (
                        LivroID INTEGER PRIMARY KEY,
                        Titulo TEXT NOT NULL,
                        EditoraID INTEGER,
                        DataPublicacao DATE,
                        Preco DECIMAL(10, 2) NOT NULL,
                        QuantidadeEstoque INTEGER NOT NULL,
                        FOREIGN KEY (EditoraID) REFERENCES EDITORA(EditoraID))''')

    # PEDIDO table
    cursor.execute('''CREATE TABLE IF NOT EXISTS PEDIDO (
                        PedidoID INTEGER PRIMARY KEY,
                        ClienteID INTEGER,
                        DataPedido DATE NOT NULL,
                        ValorTotal DECIMAL(10, 2) DEFAULT 0,
                        FOREIGN KEY (ClienteID) REFERENCES CLIENTE(ClienteID))''')

    # ITEM_PEDIDO table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ITEM_PEDIDO (
                        PedidoID INTEGER,
                        LivroID INTEGER,
                        Quantidade INTEGER NOT NULL,
                        PrecoUnitario DECIMAL(10, 2) NOT NULL,
                        PRIMARY KEY (PedidoID, LivroID),
                        FOREIGN KEY (PedidoID) REFERENCES PEDIDO(PedidoID),
                        FOREIGN KEY (LivroID) REFERENCES LIVRO(LivroID))''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()

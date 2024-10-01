import os
import sqlite3

def create_tables():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, '../database')
    db_path = os.path.join(db_dir, 'livraria.db')

    # Criar o diretório se ele não existir
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    connection = sqlite3.connect(db_path)
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

    # Trigger para atualizar ValorTotal ao inserir um item do pedido
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS atualiza_valor_total_apos_inserir_item
        AFTER INSERT ON ITEM_PEDIDO
        FOR EACH ROW
        BEGIN
            UPDATE PEDIDO
            SET ValorTotal = ValorTotal + (NEW.Quantidade * NEW.PrecoUnitario)
            WHERE PedidoID = NEW.PedidoID;
        END;
    ''')

    # Trigger para atualizar ValorTotal ao atualizar um item do pedido
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS atualiza_valor_total_apos_atualizar_item
        AFTER UPDATE ON ITEM_PEDIDO
        FOR EACH ROW
        BEGIN
            UPDATE PEDIDO
            SET ValorTotal = ValorTotal - (OLD.Quantidade * OLD.PrecoUnitario) + (NEW.Quantidade * NEW.PrecoUnitario)
            WHERE PedidoID = NEW.PedidoID;
        END;
    ''')

    # Trigger para atualizar ValorTotal ao deletar um item do pedido
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS atualiza_valor_total_apos_deletar_item
        AFTER DELETE ON ITEM_PEDIDO
        FOR EACH ROW
        BEGIN
            UPDATE PEDIDO
            SET ValorTotal = ValorTotal - (OLD.Quantidade * OLD.PrecoUnitario)
            WHERE PedidoID = OLD.PedidoID;
        END;
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()

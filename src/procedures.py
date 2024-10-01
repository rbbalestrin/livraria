import sqlite3
from utils import get_connection

# Função para calcular o total de vendas de um cliente específico
def calcular_total_vendas_cliente(cliente_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            SELECT SUM(ValorTotal) FROM PEDIDO
            WHERE ClienteID = ?
        ''', (cliente_id,))
        total_vendas = cursor.fetchone()[0]
        return total_vendas if total_vendas is not None else 0
    except sqlite3.Error as e:
        print(f"Erro ao calcular total de vendas: {e}")
        return None
    finally:
        connection.close()

# Função para buscar livros de um autor específico
def buscar_livros_por_autor(autor_nome):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            SELECT l.LivroID, l.Titulo, l.DataPublicacao, l.Preco
            FROM LIVRO l
            JOIN AUTOR a ON a.AutorID = l.LivroID
            WHERE a.PrimeiroNome LIKE ? OR a.Sobrenome LIKE ?
        ''', (f'%{autor_nome}%', f'%{autor_nome}%'))
        livros = cursor.fetchall()
        return livros
    except sqlite3.Error as e:
        print(f"Erro ao buscar livros do autor: {e}")
        return []
    finally:
        connection.close()

# Função para adicionar um novo pedido e itens de uma só vez
def adicionar_pedido_com_itens(cliente_id, data_pedido, itens):
    """
    Itens deve ser uma lista de dicionários com o formato:
    [{'LivroID': int, 'Quantidade': int, 'PrecoUnitario': float}, ...]
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Inserir pedido
        cursor.execute('''
            INSERT INTO PEDIDO (ClienteID, DataPedido, ValorTotal)
            VALUES (?, ?, 0)
        ''', (cliente_id, data_pedido))
        pedido_id = cursor.lastrowid

        # Inserir itens do pedido
        valor_total = 0
        for item in itens:
            livro_id = item['LivroID']
            quantidade = item['Quantidade']
            preco_unitario = item['PrecoUnitario']

            cursor.execute('''
                INSERT INTO ITEM_PEDIDO (PedidoID, LivroID, Quantidade, PrecoUnitario)
                VALUES (?, ?, ?, ?)
            ''', (pedido_id, livro_id, quantidade, preco_unitario))

            valor_total += quantidade * preco_unitario

        # Atualizar o valor total do pedido
        cursor.execute('''
            UPDATE PEDIDO
            SET ValorTotal = ?
            WHERE PedidoID = ?
        ''', (valor_total, pedido_id))

        # Commit das transações
        connection.commit()
        return pedido_id
    except sqlite3.Error as e:
        print(f"Erro ao adicionar pedido com itens: {e}")
        connection.rollback()
        return None
    finally:
        connection.close()

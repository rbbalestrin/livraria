def visualizar_autores(self):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM AUTOR")
        rows = cursor.fetchall()

        # Criar nova janela para mostrar os dados
        janela_visualizacao = tk.Toplevel(self.janela)
        janela_visualizacao.title("Autores Cadastrados")
        janela_visualizacao.geometry("600x300")

        # Criar Treeview para mostrar os dados em tabela
        tree = ttk.Treeview(janela_visualizacao, columns=("AutorID", "PrimeiroNome", "Sobrenome", "DataNascimento"), show="headings")
        tree.heading("AutorID", text="ID do Autor")
        tree.heading("PrimeiroNome", text="Primeiro Nome")
        tree.heading("Sobrenome", text="Sobrenome")
        tree.heading("DataNascimento", text="Data de Nascimento")

        # Definir tamanhos das colunas
        tree.column("AutorID", width=50)
        tree.column("PrimeiroNome", width=150)
        tree.column("Sobrenome", width=150)
        tree.column("DataNascimento", width=100)

        # Adicionar dados à tabela
        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        connection.close()

import os
import sqlite3

def get_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'C:/.code/livraria/database/livraria.db')

    # Ensure that the directory exists
    if not os.path.exists(db_path):
        raise FileNotFoundError("The database file does not exist. Ensure the database is created.")

    return sqlite3.connect(db_path)

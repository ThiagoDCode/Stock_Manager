import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import os

caminho = os.path.dirname(__file__) 
connection = sqlite3.connect(caminho + "/StockDatabase.db")


class Database:
    
    def dml_database(self, query_sql, dados):
        try:
            with connection:
                con = connection.cursor()
                con.execute(query_sql, dados)
        except Error as e:
            messagebox.showerror(f"{e}", message="Não foi possível realizar o registro!")
        else:
            messagebox.showinfo("Successfully", message="Registro realizado com sucesso!")
    
    def dql_database(self, query_sql):
        try:
            with connection:
                con = connection.cursor()
                con.execute(query_sql)
                response = con.fetchall()
        except Error as e:
            messagebox.showerror(f"{e}", message="Não foi possível encontrar o registro!")
        else:
            return response
    
    def dml_delete(self, dados):
        try:
            with connection:
                con = connection.cursor()
                con.execute(f"DELETE FROM estoque WHERE id='{dados}'")
        except Error as e:
            messagebox.showerror(f"{e}", message="Não foi possível realizar o registro!")
        else:
            messagebox.showinfo("Successfully", message="Registro excluído com sucesso!")


def create_table():
    table = """
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT(30),
        grupo TEXT(15),
        medida TEXT,
        lote TEXT,
        estoque INTEGER,
        valor_estoque REAL AS (estoque * revenda),
        estoque_mín INTEGER,
        fornecedor TEXT(15),
        NF TEXT,
        responsável TEXT(15),
        fone1 TEXT,
        fone2 TEXT,
        entradas INTEGER,
        data_entrada TEXT,
        saídas INTEGER,
        data_saída TEXT,
        revenda REAL,
        faturamento REAL AS (saídas * revenda),
        repor INTEGER AS (estoque_mín - estoque),
        custo REAL,
        total_custo REAL AS (repor * custo),
        gestor TEXT(15)
    );
    """

    try:
        with connection:
            con = connection.cursor()
            con.execute(table)
            print("Tabela criada com sucesso!")
    except Error as e:
        print(e)


if __name__ == "__main__":
    create_table()

import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import os

caminho = os.path.dirname(__file__) 
connection = sqlite3.connect(caminho + "/stockDatabase.db")


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
        
    def all_select_db(self):
        pass


def create_table():
    table = """
        CREATE TABLE estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT(50),
            grupo TEXT(30),
            medida TEXT,
            estoque INTEGER,
            est_mín INTEGER,
            fornecedor TEXT(50),
            responsável TEXT(50),
            NF TEXT,
            fone_1 TEXT(14),
            fone_2 TEXT(14)
        );
    """

    try:
        with connection:
            con = connection.cursor()
            con.execute(table)
    except Error as e:
        print(e)


if __name__ == "__main__":
    create_table()

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
    
    def dql_database(self, query_sql, column_names=False):
        try:
            with connection:
                con = connection.cursor()
                con.execute(query_sql)
                response = con.fetchall()
                
                if column_names:
                    lista_columns = []
                    for i in set(response):
                        lista_columns.append(i[0])
                    return lista_columns
        
        except Error as e:
            messagebox.showerror(f"{e}", message="Não foi possível encontrar o registro!")
        else:
            return response
        
    def dml_delete(self, id_target_delete):
        try:
            with connection:
                con = connection.cursor()
                con.execute(f"DELETE FROM estoque WHERE id='{id_target_delete}'")
        except Error as e:
            messagebox.showerror(f"{e}", message="Não foi possível realizar o registro!")
        else:
            messagebox.showinfo("Successfully", message="Registro excluído com sucesso!")


def create_table():
    table = """
    CREATE TABLE IF NOT EXISTS estoque (
        id              INTEGER     PRIMARY KEY AUTOINCREMENT,
        produto         TEXT (30),
        grupo           TEXT (15),
        medida          TEXT,
        lote            TEXT,
        estoque         INTEGER     DEFAULT (0),
        valor_estoque   REAL        AS (estoque * valor_venda),
        estoque_mín     INTEGER     DEFAULT (0),
        status          TEXT        AS (CASE WHEN estoque < (estoque_mín * 50/100) THEN 'CRÍTICO' WHEN estoque <= estoque_mín THEN 'BAIXO' ELSE 'OK' END),
        fornecedor      TEXT (20),
        responsável     TEXT (15),
        entradas        INTEGER     DEFAULT (0),
        data_entrada    TEXT,
        custo_unit      REAL        DEFAULT (0),
        custo_total     REAL        AS (entradas * custo_unit),
        saídas          INTEGER     DEFAULT (0),
        data_saída      TEXT,
        valor_venda     REAL        DEFAULT (0),
        faturamento     REAL        AS (valor_venda * saídas),
        repor           INTEGER     AS (CASE WHEN estoque <= estoque_mín THEN estoque_mín - estoque + (estoque_mín * 100/100) ELSE 0 END),
        custo_repor     REAL        AS (custo_unit * repor),
        barcode         TEXT (20),
        ativo           TEXT
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

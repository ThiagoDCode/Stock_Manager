from tkinter import *
from sqlite3 import Error

from con_database import *


class FunctionsEntrada:
    
    def select_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())

        query_select = """
            SELECT id, data, produto, medida, lote, estoque, fornecedor, nf, status
            FROM estoque
        """

        data_return = Database().dql_database(query_select)

        for dado in data_return:
            self.lista_produtos.insert("", "end", values=dado)

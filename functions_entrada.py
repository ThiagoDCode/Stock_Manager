from tkinter import *
from tkinter import messagebox
from sqlite3 import Error

from con_database import *


class Register(Database):
    
    def save(self):
        self.variables_entries()
        
        if self.código == "" or not self.código.isdigit():
            messagebox.showerror("ID invalid", message="Informe o código do produto a ser atualizado!")
        elif self.qtd_entrada == "" or not self.qtd_entrada.isdigit():
            messagebox.showerror("Invalid Input", message="Informe a quantidade de entrada do produto!")
        else:
            query_update = """
                UPDATE estoque SET
                    medida=?, lote=?, estoque=?, data=?, gestor=? 
                WHERE id=?
            """
            try:
                sum_estoque = int(self.qtd_entrada) + int(self.estoque)
            except:
                sum_estoque = self.qtd_entrada
            lista_dados = [self.medida, self.lote, sum_estoque, self.data, self.gestor, self.código]
            
            self.dml_database(query_update, lista_dados)
            
            self.clear_entries()
            self.select_database()

class FunctionsEntrada(Register):
    
    def variables_entries(self):
        self.código = self.reg_entry.get()
        self.data_reg = self.data_register.get()
        self.produto = self.produto_entry.get()
        self.medida = self.medida_entry.get()
        self.grupo = self.grupo_entry.get()
        self.nf = self.nf_entry.get()
        self.forne = self.fornecedor_entry.get()
        self.lote = self.lote_entry.get()
        self.status = self.status_entry.get()
        self.estoque = self.estoque_entry.get()
        
        self.gestor = self.gestor_entry.get()
        self.data = self.data_entry.get()
        
        self.qtd_entrada = self.quantidade_entry.get()
    
    def clear_entries(self):
        self.reg_entry.delete(0, END)
        self.data_register.delete(0, END)
        self.produto_entry.delete(0, END)
        self.medida_entry.delete(0, END)
        self.grupo_entry.delete(0, END)
        self.nf_entry.delete(0, END)
        self.fornecedor_entry.delete(0, END)
        self.lote_entry.delete(0, END)
        self.status_entry.delete(0, END)
        self.estoque_entry.delete(0, END)
        
        self.quantidade_entry.delete(0, END)
    
    def select_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())

        query_select = """
            SELECT id, data, produto, medida, lote, estoque, fornecedor, nf, grupo, status
            FROM estoque
        """

        data_return = Database().dql_database(query_select)

        if data_return is not None:
            for dado in data_return:
                self.lista_produtos.insert("", "end", values=dado)
            
    def on_DoubleClick(self, event):
        self.clear_entries()
        self.lista_produtos.selection()
        
        for row in self.lista_produtos.selection():
            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = self.lista_produtos.item(row, "values")
            self.reg_entry.insert(END, c1)
            self.data_register.insert(END, c2)
            self.produto_entry.insert(END, c3)
            self.medida_entry.insert(END, c4)
            self.lote_entry.insert(END, c5)
            self.estoque_entry.insert(END, c6)
            self.fornecedor_entry.insert(END, c7)
            self.nf_entry.insert(END, c8)
            self.grupo_entry.insert(END, c9)
            self.status_entry.insert(END, c10)

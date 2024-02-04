from tkinter import *
from tkinter import messagebox

from con_database import *


class Register(Database):
    
    def register_product(self):
        self.variables_entry()

        if self.produto_entry.get() == "":
            messagebox.showinfo(
                "Aviso", message="Insira a descrição do produto!")

        else:
            query_sql = """
                INSERT INTO estoque (produto, medida, grupo, est_mín, fornecedor, responsável, fone_1, fone_2, NF)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """
            lista_dados = [self.produto, self.medida, self.grupo, self.min,
                           self.fornecedor, self.resp, self.fone1, self.fone2, self.nf]

            self.dml_database(query_sql, lista_dados)

            self.clear_entries()
            self.select_database()
    
    def register_product2(self):
        self.variables_entry()

        if self.produto_entry.get() == "":
            messagebox.showinfo(
                "Aviso", message="Insira a descrição do produto!")

        else:
            query_sql = """
                INSERT INTO estoque (produto, medida, grupo, est_mín, fornecedor, responsável, fone_1, fone_2, NF, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            lista_dados = [self.produto, self.medida, self.grupo, self.min,
                           self.fornecedor, self.resp, self.fone1, self.fone2, self.nf, self.data]

            self.dml_database(query_sql, lista_dados)

            self.clear_entries()
            self.select_database()

    def update_product(self):
        self.variables_entry()

        if self.código == "" or not self.código.isdigit():
            messagebox.showerror(
                "ID invalid", message="Informe o código do produto a ser atualizado!")
        else:
            if self.produto == "":
                messagebox.showinfo(
                    "Aviso", message="Insira a descrição do produto!")
            else:
                query_sql = """
                    UPDATE estoque SET
                        produto=?, grupo=?, medida=?, est_mín=?, fornecedor=?, responsável=?, NF=?, fone_1=?, fone_2=?
                    WHERE id=?
                """
                lista_dados = [self.produto, self.grupo, self.medida, self.min, self.fornecedor,
                               self.resp, self.nf, self.fone1, self.fone2, self.código]

                self.dml_database(query_sql, lista_dados)

                self.clear_entries()
                self.select_database()

    def delete_product(self):
        self.variables_entry()

        if self.código == "" or not self.código.isdigit():
            messagebox.showerror(
                "ID invalid", message="Informe o código do produto a ser excluído!")
        else:
            if messagebox.askyesno("Delete", message="Deseja excluir o registro?"):
                self.dml_delete(self.código)

                self.clear_entries()
                self.select_database()

    def search_product(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())

        if self.produto_entry.get() == "":
            self.select_database()
        else:
            self.produto_entry.insert(END, "%")
            produto = self.produto_entry.get()

            data_query = """
                        SELECT id, produto, medida, grupo, fornecedor, estoque, est_mín, NF, responsável, fone_1, fone_2
                        FROM estoque WHERE produto LIKE '%s' ORDER BY produto ASC
                        """ % produto
            data_return = self.dql_database(data_query)

            for dados in data_return:
                self.lista_produtos.insert("", END, values=dados)

        self.clear_entries()


class FunctionsEstoque(Register):
    
    def variables_entry(self):
        self.código = self.code_entry.get()
        self.produto = self.produto_entry.get()
        self.medida = self.medida_entry.get()
        self.grupo = self.grupo_entry.get()
        self.min = self.min_entry.get()
        self.fornecedor = self.fornecedor_entry.get()
        self.resp = self.responsavel_entry.get()
        self.fone1 = self.fone1_entry.get()
        self.fone2 = self.fone2_entry.get()
        self.nf = self.nf_entry.get()
        
        #self.gestor = self.gestor_entry.get()
        #self.data = self.data_register.get()

    def clear_entries(self):
        self.code_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.medida_entry.delete(0, END)
        self.grupo_entry.delete(0, END)
        self.min_entry.delete(0, END)
        self.fornecedor_entry.delete(0, END)
        self.responsavel_entry.delete(0, END)
        self.fone1_entry.delete(0, END)
        self.fone2_entry.delete(0, END)
        self.nf_entry.delete(0, END)
    
    def select_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())
        
        query_select = """
            SELECT id, produto, medida, grupo, fornecedor, estoque, est_mín, NF, responsável, fone_1, fone_2
            FROM estoque
        """

        data_return = Database().dql_database(query_select)

        for dado in data_return:
            self.lista_produtos.insert("", "end", values=dado)
    
    def on_DoubleClick(self, event):
        self.clear_entries()
        self.lista_produtos.selection()
        
        for row in self.lista_produtos.selection():
            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = self.lista_produtos.item(row, "values")
            self.code_entry.insert(END, c1)
            self.produto_entry.insert(END, c2)
            self.medida_entry.insert(END, c3)
            self.grupo_entry.insert(END, c4)
            self.fornecedor_entry.insert(END, c5)
            self.min_entry.insert(END, c7)
            self.nf_entry.insert(END, c8)
            self.responsavel_entry.insert(END, c9)
            self.fone1_entry.insert(END, c10)
            self.fone2_entry.insert(END, c11)

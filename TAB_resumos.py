from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from con_database import *


class FunctionsResumos(Database):
    
    def select_database(self, query_sql, view_target):
        view_target.delete(*view_target.get_children())

        data_return = Database().dql_database(query_sql)
        for dados in data_return:
            view_target.insert("", END, values=dados)

    def filter_repor(self, static=False):
        self.lista_repor.delete(*self.lista_repor.get_children())
        
        query_select = """
                SELECT id, status, produto, grupo, medida, estoque, est_mín, repor, custo, total, fornecedor
                FROM estoque ORDER BY repor DESC
            """
        data_return = Database().dql_database(query_select)
        
        for dados in data_return:
            if dados[7] > 0:
                self.lista_repor.insert("", END, values=dados)
    
    def filter_repor2(self, static=False):
        query_select = """
            SELECT id, status, produto, grupo, medida, estoque, est_mín, repor, custo, total, fornecedor
            FROM estoque ORDER BY repor DESC
        """
        data_return = Database().dql_database(query_select)
        
        if static:
            for dados in data_return:
                if dados[7] > 0:
                    self.total_repor += 1
        else:
            for dados in data_return:
                if dados[7] > 0:
                    self.lista_repor.insert("", END, values=dados)


class TabResumos(FunctionsResumos):
    def __init__(self, root):
        self.root = root
        
        self.widgets_top()
        self.widgets_bottom()
        self.views_todos()
        
    def widgets_top(self):
        ctk.CTkLabel(self.root, text="Análise de Estoque", 
                     font=("Constantia", 25), text_color=("#1C1C1C", "#D3D3D3")).place(x=20, y=10)
        
        self.frame_top = ctk.CTkFrame(self.root, width=985, height=75, border_width=1, border_color="#000")
        self.frame_top.place(x=1, y=50)
        
        todos = f"Todos \n{52} produtos \nR$ {10750.00}"
        
        self.total_repor = 0
        self.filter_repor2(static=True)
        repor = f"Repor \n{self.total_repor} produtos \nR$ {350.00}"
        
        excesso = f"Em excesso \n{42} itens \nR$ {7789.34}"
        novos = f"Novos \n{2} produtos \nR$ {297.10}"
        parados = f"Parados há 90 dias \n{5} produtos \nR$ {398.56}"
        
        ctk.CTkButton(self.frame_top, width=175, text=todos, font=("Cascadia Code", 15), 
                      command=self.views_todos).grid(column=0, row=0)
        ctk.CTkButton(self.frame_top, width=175, text=repor, font=("Cascadia Code", 15), 
                      command=self.view_repor).grid(column=1, row=0, padx=10)
        ctk.CTkButton(self.frame_top, width=175, text=excesso, font=("Cascadia Code", 15),
                      command=self.view_excesso).grid(column=2, row=0)
        ctk.CTkButton(self.frame_top, width=175, text=novos, font=("Cascadia Code", 15),
                      command=self.view_novos).grid(column=3, row=0, padx=10)
        ctk.CTkButton(self.frame_top, width=175, text=parados, font=("Cascadia Code", 15),
                      command=self.view_parados).grid(column=4, row=0)
        
    def widgets_bottom(self):
        self.frame_bottom = ctk.CTkFrame(self.root, width=990, height=425, border_width=1, border_color="#000")
        self.frame_bottom.place(x=0, y=125)
        
        ctk.CTkLabel(self.frame_bottom, text="Produto", font=("Cascadia Code", 13)).place(x=5, y=5)
        self.produto_search = ctk.CTkEntry(self.frame_bottom, width=250, font=("Cascadia Code", 13))
        self.produto_search.place(x=65, y=5)
        
        ctk.CTkLabel(self.frame_bottom, text="Status", font=("Cascadia Code", 13)).place(x=325, y=5)
        self.status_search = ctk.CTkEntry(self.frame_bottom, width=125, font=("Cascadia Code", 13))
        self.status_search.place(x=378, y=5)
        
    def views_todos(self):
        self.lista_todos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'grupo', 'medida', 'estoque', 'valor', 'data', 'status'
        ))
        self.lista_todos.heading("#0", text="")
        self.lista_todos.heading("id", text="Registro")
        self.lista_todos.heading("produto", text="Produto")
        self.lista_todos.heading("grupo", text="Departamento")
        self.lista_todos.heading("medida", text="Medida")
        self.lista_todos.heading("estoque", text="Estoque")
        self.lista_todos.heading("valor", text="Valor Estoque")
        self.lista_todos.heading("data", text="Último Registro")
        self.lista_todos.heading("status", text="Status")
        
        self.lista_todos.column("#0", width=0, stretch=False)
        self.lista_todos.column("id", width=50)
        self.lista_todos.column("produto", width=270)
        self.lista_todos.column("grupo", width=150)
        self.lista_todos.column("medida", width=85)
        self.lista_todos.column("estoque", width=60)
        self.lista_todos.column("valor", width=80)
        self.lista_todos.column("data", width=75)
        self.lista_todos.column("status", width=85)
        
        self.lista_todos.place(y=40, width=970, height=382)
        
        scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_todos.yview)
        self.lista_todos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)
        
        query_select = """
            SELECT id, produto, grupo, medida, estoque, valor, data, status
            FROM estoque
        """
        self.select_database(query_select, self.lista_todos)
        
    def view_repor(self):
        self.lista_repor = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'status', 'produto', 'grupo', 'medida', 'estoque', 'mín', 'repor', 
            'custo', 'total', 'fornecedor'
        ))
        self.lista_repor.heading("#0", text="")
        self.lista_repor.heading("id", text="Registro")
        self.lista_repor.heading("status", text="Status Estoque")
        self.lista_repor.heading("produto", text="Produto")
        self.lista_repor.heading("grupo", text="Departamento")
        self.lista_repor.heading("medida", text="Medida")
        self.lista_repor.heading("estoque", text="Estoque")
        self.lista_repor.heading("mín", text="Est.Mín")
        self.lista_repor.heading("repor", text="Repor")
        self.lista_repor.heading("custo", text="Custo Médio")
        self.lista_repor.heading("total", text="Custo Total")
        self.lista_repor.heading("fornecedor", text="Fornecedor")
        
        self.lista_repor.column("#0", width=0, stretch=False)
        self.lista_repor.column("id", width=50, anchor=CENTER)
        self.lista_repor.column("status", width=90, anchor=CENTER)
        self.lista_repor.column("produto", width=270)
        self.lista_repor.column("grupo", width=150)
        self.lista_repor.column("medida", width=85, anchor=CENTER)
        self.lista_repor.column("estoque", width=60, anchor=CENTER)
        self.lista_repor.column("mín", width=50, anchor=CENTER)
        self.lista_repor.column("repor", width=50, anchor=CENTER)
        self.lista_repor.column("custo", width=80, anchor=CENTER)
        self.lista_repor.column("total", width=80, anchor=CENTER)
        self.lista_repor.column("fornecedor", width=150)
        
        self.lista_repor.place(y=40, width=970, height=362)
        
        scrollbar_y = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_repor.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_bottom, orient="horizontal", command=self.lista_repor.xview)
        self.lista_repor.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=40, width=20, height=382)
        scrollbar_x.place(x=0, y=401, width=970, height=20)

        self.filter_repor()

    def view_excesso(self):
        self.lista_excesso = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'grupo', 'medida', 'estoque', 'mín', 'excesso', 'status'
        ))
        self.lista_excesso.heading("#0", text="")
        self.lista_excesso.heading("id", text="Registro")
        self.lista_excesso.heading("produto", text="Produto")
        self.lista_excesso.heading("grupo", text="Departamento")
        self.lista_excesso.heading("medida", text="Medida")
        self.lista_excesso.heading("estoque", text="Estoque")
        self.lista_excesso.heading("mín", text="Est.Mín")
        self.lista_excesso.heading("excesso", text="Excesso")
        self.lista_excesso.heading("status", text="Status")
        
        self.lista_excesso.column("#0", width=0, stretch=False)
        self.lista_excesso.column("id", width=50)
        self.lista_excesso.column("produto", width=270)
        self.lista_excesso.column("grupo", width=150)
        self.lista_excesso.column("medida", width=85)
        self.lista_excesso.column("estoque", width=60)
        self.lista_excesso.column("mín", width=50)
        self.lista_excesso.column("excesso", width=50)
        self.lista_excesso.column("status", width=85)
        
        self.lista_excesso.place(y=40, width=970, height=382)
        
        scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_excesso.yview)
        self.lista_excesso.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)
        
        query_select = """
            SELECT id, produto, grupo, medida, estoque, est_mín, excesso, status
            FROM estoque
        """
        self.select_database(query_select, self.lista_excesso)

    def view_novos(self):
        self.lista_novos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'data', 'produto', 'grupo', 'medida', 'lote', 'estoque', 'fornecedor', 
            'custo', 'total', 'status'
        ))
        self.lista_novos.heading("#0", text="")
        self.lista_novos.heading("id", text="Registro")
        self.lista_novos.heading("data", text="Data")
        self.lista_novos.heading("produto", text="Produto")
        self.lista_novos.heading("grupo", text="Departamento")
        self.lista_novos.heading("medida", text="Medida")
        self.lista_novos.heading("lote", text="Nº Lote")
        self.lista_novos.heading("estoque", text="Estoque")
        self.lista_novos.heading("fornecedor", text="Fornecedor")
        self.lista_novos.heading("custo", text="Custo Médio")
        self.lista_novos.heading("total", text="Custo Total")
        self.lista_novos.heading("status", text="Status")
        
        self.lista_novos.column("#0", width=0, stretch=False)
        self.lista_novos.column("id", width=50)
        self.lista_novos.column("data", width=85)
        self.lista_novos.column("produto", width=270)
        self.lista_novos.column("grupo", width=150)
        self.lista_novos.column("medida", width=85)
        self.lista_novos.column("lote", width=85)
        self.lista_novos.column("estoque", width=60)
        self.lista_novos.column("fornecedor", width=150)
        self.lista_novos.column("custo", width=80)
        self.lista_novos.column("total", width=80)
        self.lista_novos.column("status", width=90)
        
        self.lista_novos.place(y=40, width=970, height=362)
        
        scrollbar_y = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_novos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_bottom, orient="horizontal", command=self.lista_novos.xview)
        self.lista_novos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=40, width=20, height=382)
        scrollbar_x.place(x=0, y=401, width=970, height=20)
        
        query_select = """
                SELECT id, data, produto, grupo, medida, lote, estoque, fornecedor, custo, total, status
                FROM estoque
            """
        self.select_database(query_select, self.lista_novos)

    def view_parados(self):
        self.lista_parados = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'grupo', 'medida', 'estoque', 'valor', 'data', 'status'
        ))
        self.lista_parados.heading("#0", text="")
        self.lista_parados.heading("id", text="Registro")
        self.lista_parados.heading("produto", text="Produto")
        self.lista_parados.heading("grupo", text="Departamento")
        self.lista_parados.heading("medida", text="Medida")
        self.lista_parados.heading("estoque", text="Estoque")
        self.lista_parados.heading("valor", text="Valor Estoque")
        self.lista_parados.heading("data", text="Última Saída")
        self.lista_parados.heading("status", text="Status")
        
        self.lista_parados.column("#0", width=0, stretch=False)
        self.lista_parados.column("id", width=50)
        self.lista_parados.column("produto", width=270)
        self.lista_parados.column("grupo", width=150)
        self.lista_parados.column("medida", width=85)
        self.lista_parados.column("estoque", width=60)
        self.lista_parados.column("valor", width=80)
        self.lista_parados.column("data", width=75)
        self.lista_parados.column("status", width=85)
        
        self.lista_parados.place(y=40, width=970, height=382)
        
        scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_parados.yview)
        self.lista_parados.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)
        
        query_select = """
            SELECT id, produto, grupo, medida, estoque, valor, data_off, status
            FROM estoque
        """
        self.select_database(query_select, self.lista_parados)


if __name__ == "__main__":
    FunctionsResumos().filter_repor()

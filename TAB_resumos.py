from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from datetime import date

from con_database import *
from functions_base import *


class FunctionsResumos(Database):
    
    def select_database(self, query_sql, view_target):
        view_target.delete(*view_target.get_children())

        data_return = Database().dql_database(query_sql)
        for dados in data_return:
            view_target.insert("", END, values=dados)
    
    def filter_todos(self, resumo=False):
        query_select = """
            SELECT id, produto, grupo, medida, estoque, valor_estoque, data_entrada, status
            FROM estoque
        """
        data_return = Database().dql_database(query_select)

        if resumo:
            self.total_itens = len(data_return)
            for dados in data_return:
                self.valor_itens += dados[5]
        else:
            for dados in data_return:
                self.lista_todos.insert("", END, values=dados)
    
    def filter_repor(self, resumo=False):
        query_select = """
            SELECT id, status, produto, grupo, medida, estoque, estoque_mín, repor, custo, total_custo, fornecedor
            FROM estoque ORDER BY repor DESC
        """
        data_return = Database().dql_database(query_select)
        
        if resumo:
            for dados in data_return:
                if dados[7] > 0:
                    self.total_repor += 1
                    self.valor_repor += dados[9]
        else:
            for dados in data_return:
                if dados[7] > 0:
                    self.lista_repor.insert("", END, values=dados)

    def filter_movimentos(self, resumo=False):
        query_select = """
            SELECT id, produto, medida, estoque, valor_estoque, entradas, saídas, custo, revenda, status, data_entrada, faturamento
            FROM estoque ORDER BY data_entrada DESC
        """
        data_return = Database().dql_database(query_select)

        if resumo:
            for dados in data_return:
                if dados[5] > 0 or dados[6] > 0:
                    self.total_movimentos += 1
                    self.valor_faturamento += dados[11]
        else:
            for dados in data_return:
                if dados[5] > 0 or dados[6] > 0:
                    self.lista_movimentos.insert("", END, values=dados)
    
    def filter_novos(self, resumo=False):
        query_select = """
                SELECT id, data, produto, grupo, medida, lote, entradas, estoque, fornecedor, custo, total_custo, status
                FROM estoque ORDER BY data DESC
            """
        data_return = Database().dql_database(query_select)

        if resumo:
            for dados in data_return:
                pass
        else:
            for dados in data_return:
                ano, mes, dia = int(dados[1][6:]), int(dados[1][3:5]), int(dados[1][:2])
                data = date.today() - date(ano, mes, dia)
                
                if data.days <= 30:
                    self.lista_novos.insert("", END, values=dados)


class TabResumos(FunctionsResumos, Functions):
    def __init__(self, root):
        self.root = root
        
        self.widgets_top()
        self.widgets_bottom()
        self.views_todos()
        
    def widgets_top(self):
        ctk.CTkLabel(self.root, text="Análise de Estoque", 
                     font=("Constantia", 25), text_color=("#1C1C1C", "#D3D3D3")
                     ).place(x=20, y=10)
        
        self.frame_top = ctk.CTkFrame(self.root, width=985, height=75, border_width=1, border_color="#000")
        self.frame_top.place(x=1, y=50)
        
        self.total_itens = 0
        self.valor_itens = 0
        self.filter_todos(resumo=True)
        todos = f"TODOS \n{self.total_itens} produtos \nR$ {self.valor_itens:.2f}"
        
        self.total_repor = 0
        self.valor_repor = 0
        #self.filter_repor(resumo=True)
        repor = f"Repor \n{self.total_repor} produtos \nR$ {self.valor_repor:.2f}"
        
        self.total_movimentos = 0
        self.valor_faturamento = 0
        #self.filter_movimentos(resumo=True)
        excesso = f"Movimentos \n{self.total_movimentos} produtos \nR$ {self.valor_faturamento:.2f}"
        
        
        
        novos = f"Novos \n{2} produtos \nR$ {297.10}"
        parados = f"Parados há 90 dias \n{5} produtos \nR$ {398.56}"
        
        ctk.CTkButton(self.frame_top, width=175, text=todos, font=("Cascadia Code", 15), 
                      command=self.views_todos).grid(column=0, row=0)
        ctk.CTkButton(self.frame_top, width=175, text=repor, font=("Cascadia Code", 15), 
                      command=self.view_repor).grid(column=1, row=0, padx=10)
        ctk.CTkButton(self.frame_top, width=175, text=excesso, font=("Cascadia Code", 15),
                      command=self.view_movimentos).grid(column=2, row=0)
        ctk.CTkButton(self.frame_top, width=175, text=novos, font=("Cascadia Code", 15),
                      command=self.view_novos).grid(column=3, row=0, padx=10)
        ctk.CTkButton(self.frame_top, width=175, text=parados, font=("Cascadia Code", 15),
                      command=self.view_parados).grid(column=4, row=0)
        
        ctk.CTkButton(self.frame_top, image=self.image_button("atualizar.png", (34, 34)), width=50, text="",
                      compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"),
                      command=self.widgets_top).grid(column=5, row=0, padx=10)
        
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
        self.lista_todos.heading("id", text="Cod.")
        self.lista_todos.heading("produto", text="Produto")
        self.lista_todos.heading("grupo", text="Departamento")
        self.lista_todos.heading("medida", text="Medida")
        self.lista_todos.heading("estoque", text="Estoque")
        self.lista_todos.heading("valor", text="Valor do Estoque")
        self.lista_todos.heading("data", text="Últ. Movimento")
        self.lista_todos.heading("status", text="Status")
        
        self.lista_todos.column("#0", width=0, stretch=False)
        self.lista_todos.column("id", width=30, anchor=CENTER)
        self.lista_todos.column("produto", width=270)
        self.lista_todos.column("grupo", width=125)
        self.lista_todos.column("medida", width=85, anchor=CENTER)
        self.lista_todos.column("estoque", width=50, anchor=CENTER)
        self.lista_todos.column("valor", width=80, anchor=CENTER)
        self.lista_todos.column("data", width=75, anchor=CENTER)
        self.lista_todos.column("status", width=70, anchor=CENTER)
        
        self.lista_todos.place(y=40, width=970, height=382)
        
        scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_todos.yview)
        self.lista_todos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)

        self.filter_todos()
        
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

        #self.filter_repor()

    def view_movimentos(self):
        self.lista_movimentos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'medida', 'estoque', 'valor', 'entradas', 'saídas', 'custo',
            'revenda', 'status', 'data', 'faturamento'
        ))
        self.lista_movimentos.heading("#0", text="")
        self.lista_movimentos.heading("id", text="Registro")
        self.lista_movimentos.heading("produto", text="Produto")
        self.lista_movimentos.heading("medida", text="Medida")
        self.lista_movimentos.heading("estoque", text="Estoque")
        self.lista_movimentos.heading("valor", text="Valor do Estoque")
        self.lista_movimentos.heading("entradas", text="Entradas")
        self.lista_movimentos.heading("saídas", text="Saídas")
        self.lista_movimentos.heading("custo", text="Valor de Entrada")
        self.lista_movimentos.heading("revenda", text="Valor de Saída")
        self.lista_movimentos.heading("status", text="Status")
        
        self.lista_movimentos.heading("data", text="")
        self.lista_movimentos.heading("faturamento", text="")
        
        self.lista_movimentos.column("#0", width=0, stretch=False)
        self.lista_movimentos.column("id", width=50)
        self.lista_movimentos.column("produto", width=270)
        self.lista_movimentos.column("medida", width=85)
        self.lista_movimentos.column("estoque", width=50)
        self.lista_movimentos.column("valor", width=90)
        self.lista_movimentos.column("entradas", width=50)
        self.lista_movimentos.column("saídas", width=50)
        self.lista_movimentos.column("custo", width=87)
        self.lista_movimentos.column("revenda", width=75)
        self.lista_movimentos.column("status", width=75)
        
        self.lista_movimentos.column("data", width=0, stretch=False)
        self.lista_movimentos.column("faturamento", width=0, stretch=False)
        
        self.lista_movimentos.place(y=40, width=970, height=382)
        
        scrollbar = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_movimentos.yview)
        self.lista_movimentos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)

        #self.filter_movimentos()

    def view_novos(self):
        self.lista_novos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'data', 'produto', 'grupo', 'medida', 'lote', 'entradas', 'estoque', 'fornecedor',
            'custo', 'total', 'status'
        ))
        self.lista_novos.heading("#0", text="")
        self.lista_novos.heading("id", text="Registro")
        self.lista_novos.heading("data", text="Data")
        self.lista_novos.heading("produto", text="Produto")
        self.lista_novos.heading("grupo", text="Departamento")
        self.lista_novos.heading("medida", text="Medida")
        self.lista_novos.heading("lote", text="Nº Lote")
        self.lista_novos.heading("entradas", text="Entradas")
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
        self.lista_novos.column("entradas", width=55)
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
        
        #self.filter_novos()

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
        #self.select_database(query_select, self.lista_parados)
        
    def total_registries(self):
        self.total_registros = len(self.lista_produtos.get_children())



if __name__ == "__main__":
    pass

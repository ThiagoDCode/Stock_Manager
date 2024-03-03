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
            SELECT 
                id, produto, grupo, medida, lote, estoque, 
                valor_estoque, data_entrada, status, n_barcode
            FROM 
                estoque
        """
        data_return = Database().dql_database(query_select)

        if resumo:
            self.total_itens = len(data_return)
            for dados in data_return:
                self.valor_itens += dados[5]
        else:
            for dados in data_return:
                self.lista_todos.insert("", END, values=dados)
    
    def search_todos(self):
        self.lista_todos.delete(*self.lista_todos.get_children())
        
        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":
                
                sql = """
                    SELECT
                        id, produto, grupo, medida, lote, estoque, 
                        valor_estoque, data_entrada, status, n_barcode
                    FROM
                        estoque
                """
        else:
            if self.busca.get():
                buscar = f"""
                    produto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%' 
                    OR n_barcode LIKE '%{self.busca.get()}%'
                """
            
            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"
            
            elif self.busca_status_listBox.get():
                buscar = f"status LIKE '%{self.busca_status_listBox.get()}%' ORDER BY estoque DESC"
        
            sql = f"""
                SELECT
                    id, produto, grupo, medida, lote, estoque, 
                    valor_estoque, data_entrada, status, n_barcode
                FROM
                    estoque
                WHERE
                    {buscar}
            """
            
        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                self.lista_todos.insert("", END, values=dados)
        
        self.clear_search()

    def filter_repor(self, resumo=False):
        query_select = """
            SELECT 
                id, status, produto, grupo, medida, lote, estoque, 
                estoque_mín, repor, custo, total_custo, fornecedor, n_barcode
            FROM 
                estoque ORDER BY status DESC
        """
        data_return = Database().dql_database(query_select)

        for dados in data_return:
            if dados[6] <= dados[7]:
                if resumo:
                    self.total_repor += 1
                    self.valor_repor += dados[9]
                else:
                    self.lista_repor.insert("", END, values=dados)
    
    def search_repor(self):
        self.lista_repor.delete(*self.lista_repor.get_children())

        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":

            sql = """
                    SELECT
                        id, status, produto, grupo, medida, lote, estoque, 
                        estoque_mín, repor, custo, total_custo, fornecedor, n_barcode
                    FROM
                        estoque ORDER BY status DESC
                """
        else:
            if self.busca.get():
                buscar = f"""
                    produto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%'
                    OR n_barcode LIKE '%{self.busca.get()}%'
                """

            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"

            elif self.busca_status_listBox.get():
                buscar = f"status LIKE '%{self.busca_status_listBox.get()}%' ORDER BY estoque DESC"

            sql = f"""
                SELECT
                    id, status, produto, grupo, medida, lote, estoque,
                    estoque_mín, repor, custo, total_custo, fornecedor, n_barcode
                FROM
                    estoque
                WHERE
                    {buscar}
            """

        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                if dados[6] <= dados[7]:
                    self.lista_repor.insert("", END, values=dados)
        
        self.clear_search()

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
                SELECT id, data_entrada, produto, medida, lote, entradas, custo, custo_total, estoque, status, grupo, fornecedor
                FROM estoque ORDER BY data_entrada DESC
            """
        data_return = Database().dql_database(query_select)

        for dados in data_return:
            if dados[1] == None or dados[1] == "":
                continue
            
            # Busca entradas feitas dentro dos últimos 30 dias
            ano, mes, dia = int(dados[1][6:]), int(dados[1][3:5]), int(dados[1][:2])
            data = date.today() - date(ano, mes, dia)

            if data.days <= 30:
                if resumo:
                    self.total_novos += 1
                    self.valor_novos += dados[7]
                else:
                    self.lista_novos.insert("", END, values=dados)

    def filter_parados(self, resumo=False):
        sql = """
            SELECT 
                id, data_saída, produto, lote, medida, saídas, 
                estoque, valor_estoque, grupo, fornecedor
            FROM 
                estoque ORDER BY data_saída DESC
        """
        data_return = Database().dql_database(sql)

        for dados in data_return:
            if dados[1] == None or dados[1] == "":
                continue
            
            # Busca por saídas feitas a mais de 90 dias
            ano, mes, dia = int(dados[1][6:]), int(dados[1][3:5]), int(dados[1][:2])
            data = date.today() - date(ano, mes, dia)

            if data.days >= 90:
                if resumo:
                    self.total_parados += 1
                    self.valor_parados += dados[7]
                else:
                    self.lista_parados.insert("", END, values=dados)
    
    def clear_search(self):
        self.busca.delete(0, END)
        self.busca.configure(placeholder_text="Buscar Produto, Nº Lote, Código de Barras")
        self.busca_grupo_listBox.set("")
        self.busca_status_listBox.set("")


class TabResumos(FunctionsResumos, FunctionsExtras):
    def __init__(self, root):
        self.root = root

        self.widgets_top()
        # self.widgets_bottom()
        self.views_todos()

    def widgets_top(self):
        ctk.CTkLabel(self.root, text="Análise de Estoque",
                     font=("Constantia", 25), text_color=("#1C1C1C", "#D3D3D3")
                     ).place(x=20, y=10)

        self.frame_top = ctk.CTkFrame(self.root, width=985, height=75)
        self.frame_top.place(x=1, y=50)

        self.total_itens = 0
        self.valor_itens = 0
        self.filter_todos(resumo=True)
        todos = f"TODOS \n{self.total_itens} produtos \nR$ {self.valor_itens:.2f}"

        self.total_repor = 0
        self.valor_repor = 0
        self.filter_repor(resumo=True)
        repor = f"REPOR \n{self.total_repor} produtos \nR$ {self.valor_repor:.2f}"

        self.total_movimentos = 0
        self.valor_faturamento = 0
        # self.filter_movimentos(resumo=True)
        faturamento = f"FATURAMENTO \n{self.total_movimentos} produtos \nR$ {self.valor_faturamento:.2f}"

        self.total_novos = 0
        self.valor_novos = 0
        self.filter_novos(resumo=True)
        novos = f"NOVOS \n{self.total_novos} produtos \nR$ {self.valor_novos:.2f}"

        self.total_parados = 0
        self.valor_parados = 0
        self.filter_parados(resumo=True)
        parados = f"PARADOS \n{self.total_parados} produtos \nR$ {self.valor_parados:.2f}"

        ctk.CTkButton(self.frame_top, text=todos,
                      width=175, 
                      font=("Cascadia Code", 15),
                      fg_color="#000080",
                      command=self.views_todos).grid(column=0, row=0)
        ctk.CTkButton(self.frame_top, text=repor, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#FF4500",
                      command=self.view_repor).grid(column=1, row=0, padx=10)
        ctk.CTkButton(self.frame_top, text=faturamento, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#FFD700",
                      command=self.view_movimentos).grid(column=2, row=0)
        ctk.CTkButton(self.frame_top, text=novos, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#32CD32",
                      command=self.view_novos).grid(column=3, row=0, padx=10)
        ctk.CTkButton(self.frame_top, text=parados, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#D8BFD8",
                      command=self.view_parados).grid(column=4, row=0)

        ctk.CTkButton(self.frame_top, text="",
                      width=50,
                      image=self.image_button("atualizar.png", (34, 34)),  
                      compound=LEFT, anchor=NW, 
                      fg_color="transparent", 
                      hover_color=("#D3D3D3", "#363636"),
                      command=self.widgets_top).grid(column=5, row=0, padx=10)

    def widgets_bottom(self):
        pass
        # self.frame_bottom = ctk.CTkFrame(self.root, width=990, height=425, border_width=1, border_color="#000")
        # self.frame_bottom.place(x=0, y=125)

        # ctk.CTkLabel(self.frame_bottom, text="Produto", font=("Cascadia Code", 13)).place(x=5, y=5)
        # self.produto_search = ctk.CTkEntry(self.frame_bottom, width=250, font=("Cascadia Code", 13))
        # self.produto_search.place(x=65, y=5)

        # ctk.CTkLabel(self.frame_bottom, text="Status", font=("Cascadia Code", 13)).place(x=325, y=5)
        # self.status_search = ctk.CTkEntry(self.frame_bottom, width=125, font=("Cascadia Code", 13))
        # self.status_search.place(x=378, y=5)

    def views_todos(self):
        self.frame_todos = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_todos.place(x=0, y=125)

        ctk.CTkLabel(self.frame_todos, text="Rastreamento de produtos registrados!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_todos, text="Produto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_todos,
                                  width=350,
                                  placeholder_text="Buscar Produto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM estoque", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_todos, 
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Status",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        lista_status = ['OK', 'BAIXO', 'CRÍTICO']
        self.busca_status_listBox = ctk.CTkComboBox(self.frame_todos, 
                                                    width=100,
                                                    values=lista_status,
                                                    font=("Cascadia Code", 13))
        self.busca_status_listBox.set("")
        self.busca_status_listBox.place(x=575, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Data",
                     font=("Cascadia Code", 13)).place(x=685, y=50)
        self.busca_mes = ctk.CTkEntry(self.frame_todos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mês",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=685, y=75)
        ctk.CTkLabel(self.frame_todos, text="/",
                     font=("Cascadia Code", 20, "bold"), text_color="#A9A9A9",
                     ).place(x=735, y=75)
        self.busca_ano = ctk.CTkEntry(self.frame_todos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Ano",
                                      font=("Cascadia Code", 13))
        self.busca_ano.place(x=748, y=75)
        
        ctk.CTkButton(self.frame_todos, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_todos).place(x=820, y=75)

        ctk.CTkButton(self.frame_todos, text="LIMPAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=890, y=75)
        
        """lista_movimentos = ['Recentes', 'Crescente', 'Decrescente']
        self.busca_movimentos_listBox = ctk.CTkComboBox(self.frame_todos, 
                                                        width=150,
                                                        values=lista_movimentos,
                                                        font=("Cascadia Code", 13))
        self.busca_movimentos_listBox.set("Movimentações")
        self.busca_movimentos_listBox.place(x=325, y=45)"""
        # ---------------------------------------------------------------------------------------
        
        self.lista_todos = ttk.Treeview(self.frame_todos, height=3, column=(
            'id', 'produto', 'grupo', 'medida', 'lote', 
            'estoque', 'valor', 'data', 'status', 'barcode'
        ))
        
        self.lista_todos.heading("#0", text="")
        self.lista_todos.heading("id", text="Cód.")
        self.lista_todos.heading("produto", text="Produto")
        self.lista_todos.heading("grupo", text="Departamento")
        self.lista_todos.heading("medida", text="Medida")
        self.lista_todos.heading("lote", text="Nº Lote")
        self.lista_todos.heading("estoque", text="Estoque")
        self.lista_todos.heading("valor", text="Valor Estoque")
        self.lista_todos.heading("data", text="Últ.Registro")
        self.lista_todos.heading("status", text="Status")
        self.lista_todos.heading("barcode", text="Código de Barras")

        self.lista_todos.column("#0", width=0, stretch=False)
        self.lista_todos.column("id", width=30, anchor=CENTER)
        self.lista_todos.column("produto", width=270)
        self.lista_todos.column("grupo", width=125)
        self.lista_todos.column("medida", width=85, anchor=CENTER)
        self.lista_todos.column("lote", width=50, anchor=CENTER)
        self.lista_todos.column("estoque", width=50, anchor=CENTER)
        self.lista_todos.column("valor", width=80, anchor=CENTER)
        self.lista_todos.column("data", width=75, anchor=CENTER)
        self.lista_todos.column("status", width=70, anchor=CENTER)
        self.lista_todos.column("barcode", width=100, anchor=CENTER)

        self.lista_todos.place(y=110, width=970, height=315)

        scrollbar = ttk.Scrollbar(self.frame_todos, 
                                  orient="vertical", 
                                  command=self.lista_todos.yview)
        self.lista_todos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=110, width=20, height=315)

        self.filter_todos()

    def view_repor(self):
        self.frame_repor = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_repor.place(x=0, y=125)

        ctk.CTkLabel(self.frame_repor, text="Recomendações de produtos para reposição de estoque!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_repor, text="Produto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_repor,
                                  width=350,
                                  placeholder_text="Buscar Produto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)
        
        ctk.CTkLabel(self.frame_repor, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM estoque", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_repor, 
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_repor, text="Status",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        lista_status = ['BAIXO', 'CRÍTICO']
        self.busca_status_listBox = ctk.CTkComboBox(self.frame_repor, 
                                                    width=100,
                                                    values=lista_status,
                                                    font=("Cascadia Code", 13))
        self.busca_status_listBox.set("")
        self.busca_status_listBox.place(x=575, y=75)
        
        ctk.CTkButton(self.frame_repor, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_repor).place(x=700, y=75)
        
        ctk.CTkButton(self.frame_repor, text="LIMPAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=770, y=75)
        
        self.lista_repor = ttk.Treeview(self.frame_repor, height=3, column=(
            'id', 'status', 'produto', 'grupo', 'medida', 'lote', 'estoque', 
            'mín', 'repor', 'custo', 'total', 'fornecedor', 'barcode'
        ))
        self.lista_repor.heading("#0", text="")
        self.lista_repor.heading("id", text="Cód.")
        self.lista_repor.heading("status", text="Status")
        self.lista_repor.heading("produto", text="Produto")
        self.lista_repor.heading("grupo", text="Departamento")
        self.lista_repor.heading("medida", text="Medida")
        self.lista_repor.heading("lote", text="Nº Lote")
        self.lista_repor.heading("estoque", text="Estoque")
        self.lista_repor.heading("mín", text="Est.Mín")
        self.lista_repor.heading("repor", text="Repor")
        self.lista_repor.heading("custo", text="Custo Unit.")
        self.lista_repor.heading("total", text="Custo Total")
        self.lista_repor.heading("fornecedor", text="Fornecedor")
        self.lista_repor.heading("barcode", text="Código de Barras")

        self.lista_repor.column("#0", width=0, stretch=False)
        self.lista_repor.column("id", width=35, anchor=CENTER)
        self.lista_repor.column("status", width=70, anchor=CENTER)
        self.lista_repor.column("produto", width=270)
        self.lista_repor.column("grupo", width=125)
        self.lista_repor.column("medida", width=85, anchor=CENTER)
        self.lista_repor.column("lote", width=50, anchor=CENTER)
        self.lista_repor.column("estoque", width=50, anchor=CENTER)
        self.lista_repor.column("mín", width=50, anchor=CENTER)
        self.lista_repor.column("repor", width=50, anchor=CENTER)
        self.lista_repor.column("custo", width=80, anchor=CENTER)
        self.lista_repor.column("total", width=80, anchor=CENTER)
        self.lista_repor.column("fornecedor", width=150)
        self.lista_repor.column("barcode", width=100, anchor=CENTER)

        self.lista_repor.place(y=110, width=970, height=315)

        scrollbar_y = ttk.Scrollbar(self.frame_repor,
                                    orient="vertical",
                                    command=self.lista_repor.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_repor,
                                    orient="horizontal",
                                    command=self.lista_repor.xview)
        self.lista_repor.configure(yscrollcommand=scrollbar_y.set, 
                                   xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=110, width=20, height=315)
        scrollbar_x.place(x=0, y=405, width=970, height=20)

        self.filter_repor()

    def view_movimentos(self):
        self.frame_movimentos = ctk.CTkFrame(self.root,
                                             width=990, height=425,
                                             fg_color="#363636")
        self.frame_movimentos.place(x=0, y=125)

        ctk.CTkLabel(self.frame_movimentos, text="...",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        self.lista_movimentos = ttk.Treeview(self.frame_movimentos, height=3, column=(
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

        scrollbar = ttk.Scrollbar(self.frame_movimentos,
                                  orient="vertical",
                                  command=self.lista_movimentos.yview)
        self.lista_movimentos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=40, width=20, height=382)

        # self.filter_movimentos()

    def view_novos(self):
        self.frame_novos = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_novos.place(x=0, y=125)

        ctk.CTkLabel(self.frame_novos, text="Registros e entradas feitas nos últimos 30 dias!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        self.lista_novos = ttk.Treeview(self.frame_novos, height=3, column=(
            'id', 'data', 'produto', 'medida', 'lote', 'entrada', 'custo',
            'total', 'estoque', 'status', 'grupo', 'fornecedor'
        ))
        self.lista_novos.heading("#0", text="")
        self.lista_novos.heading("id", text="Cód.")
        self.lista_novos.heading("data", text="Últ. Entrada")
        self.lista_novos.heading("produto", text="Produto")
        self.lista_novos.heading("medida", text="Medida")
        self.lista_novos.heading("lote", text="Nº Lote")
        self.lista_novos.heading("entrada", text="Entrada")
        self.lista_novos.heading("custo", text="Custo Unit.")
        self.lista_novos.heading("total", text="Custo Total")
        self.lista_novos.heading("estoque", text="Estoque")
        self.lista_novos.heading("status", text="Status")
        self.lista_novos.heading("grupo", text="Departamento")
        self.lista_novos.heading("fornecedor", text="Fornecedor")

        self.lista_novos.column("#0", width=0, stretch=False)
        self.lista_novos.column("id", width=35, anchor=CENTER)
        self.lista_novos.column("data", width=75, anchor=CENTER)
        self.lista_novos.column("produto", width=270)
        self.lista_novos.column("medida", width=85, anchor=CENTER)
        self.lista_novos.column("lote", width=60, anchor=CENTER)
        self.lista_novos.column("entrada", width=50, anchor=CENTER)
        self.lista_novos.column("custo", width=80, anchor=CENTER)
        self.lista_novos.column("total", width=80, anchor=CENTER)
        self.lista_novos.column("estoque", width=50, anchor=CENTER)
        self.lista_novos.column("status", width=70, anchor=CENTER)
        self.lista_novos.column("grupo", width=125)
        self.lista_novos.column("fornecedor", width=150)

        self.lista_novos.place(y=40, width=970, height=362)

        scrollbar_y = ttk.Scrollbar(self.frame_novos,
                                    orient="vertical",
                                    command=self.lista_novos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_novos,
                                    orient="horizontal",
                                    command=self.lista_novos.xview)
        self.lista_novos.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=40, width=20, height=382)
        scrollbar_x.place(x=0, y=401, width=970, height=20)

        self.filter_novos()

    def view_parados(self):
        self.frame_parados = ctk.CTkFrame(self.root,
                                          width=990, height=425,
                                          fg_color="#363636")
        self.frame_parados.place(x=0, y=125)

        ctk.CTkLabel(self.frame_parados, text="Rastreamento de Lotes sem saída a mais de 90 dias!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        self.lista_parados = ttk.Treeview(self.frame_parados, height=3, column=(
            'id', 'data', 'produto', 'lote', 'medida', 'saída',
            'estoque', 'valor', 'grupo', 'fornecedor'
        ))
        self.lista_parados.heading("#0", text="")
        self.lista_parados.heading("id", text="Cód.")
        self.lista_parados.heading("data", text="Últ. Saída")
        self.lista_parados.heading("produto", text="Produto")
        self.lista_parados.heading("lote", text="Nº Lote")
        self.lista_parados.heading("medida", text="Medida")
        self.lista_parados.heading("saída", text="Saída")
        self.lista_parados.heading("estoque", text="Estoque")
        self.lista_parados.heading("valor", text="Valor Estoque")
        self.lista_parados.heading("grupo", text="Departamento")
        self.lista_parados.heading("fornecedor", text="Fornecedor")

        self.lista_parados.column("#0", width=0, stretch=False)
        self.lista_parados.column("id", width=35, anchor=CENTER)
        self.lista_parados.column("data", width=75, anchor=CENTER)
        self.lista_parados.column("produto", width=270)
        self.lista_parados.column("lote", width=60, anchor=CENTER)
        self.lista_parados.column("medida", width=85, anchor=CENTER)
        self.lista_parados.column("saída", width=50, anchor=CENTER)
        self.lista_parados.column("estoque", width=50, anchor=CENTER)
        self.lista_parados.column("valor", width=80, anchor=CENTER)
        self.lista_parados.column("grupo", width=125)
        self.lista_parados.column("fornecedor", width=150)

        self.lista_parados.place(y=40, width=970, height=382)

        scrollbar_y = ttk.Scrollbar(self.frame_parados,
                                    orient="vertical",
                                    command=self.lista_parados.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_parados,
                                    orient="horizontal",
                                    command=self.lista_parados.xview)
        self.lista_parados.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=40, width=20, height=382)
        scrollbar_x.place(x=0, y=401, width=970, height=20)

        self.filter_parados()

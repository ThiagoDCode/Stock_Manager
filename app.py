from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from functions_estoque import FunctionsEstoque
from functions_entrada import FunctionsEntrada
from functions_base import Functions


class Application:
    def __init__(self):
        self.root = ctk.CTk()

        self.layout_config()
        self.menu_bar()
        self.tabs_application()

        self.root.mainloop()

    def layout_config(self):
        self.root.title("Controle de Estoque")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

    def menu_bar(self):  
        menu_bar = Menu(self.root)
        self.root.configure(menu=menu_bar)
        edite = Menu(menu_bar)
        
        menu_bar.add_cascade(label="Edite", menu=edite)
        edite.add_command(label="Configurações", command=WindowConfig)
    
    def tabs_application(self):
        self.tabs_view = ctk.CTkTabview(self.root, width=1000, height=570, anchor="w", text_color=('#000', '#FFF'))
        self.tabs_view.pack()

        self.tabs_view.add("Resumos")

        self.tabs_view.add("Produtos e Estoque")
        TabEstoque(self.tabs_view.tab("Produtos e Estoque"))

        self.tabs_view.add("Entrada de Produtos")
        TabEntrada(self.tabs_view.tab("Entrada de Produtos"))

        self.tabs_view.set("Entrada de Produtos")


class WindowConfig(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        self.layout_config()
        self.appearance_theme()
        self.confirm_config()
    
    def layout_config(self):
        self.geometry("300x400")
        self.minsize(300, 400)
        self.maxsize(300, 400)
        self.focus()
        self.grab_set()
    
    def appearance_theme(self):
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("system")

        ctk.CTkLabel(self, text="Tema", font=("Cascadia Code", 15, "bold")).place(x=50, y=50)
        ctk.CTkOptionMenu(self, width=90, height=20, values=['System', 'Light', 'Dark'], font=("Cascadia Code", 15), 
                          command=ctk.set_appearance_mode).place(x=50, y=100)
    
    def confirm_config(self):
        ctk.CTkButton(self, width=75, text="APLICAR", font=("Cascadia Code", 15, "bold"),
                      command=None).place(x=100, y=360)
        ctk.CTkButton(self, width=75, text="CANCELAR", font=("Cascadia Code", 15, "bold"),
                      command=self.destroy).place(x=185, y=360)


class TabEstoque(FunctionsEstoque, Functions):
    def __init__(self, root):
        self.root = root

        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()
    
    def buttons_header(self):
        btn_add = ctk.CTkButton(self.root, image=self.image_button("add.png", (34, 34)), text="", width=30,
                                compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"), command=self.register_product)
        btn_add.grid(column=0, row=0, padx=1)

        btn_search = ctk.CTkButton(self.root, image=self.image_button("search.png", (34, 34)), text="", width=30,
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"), command=self.search_product)
        btn_search.grid(column=1, row=0, padx=1)

        btn_update = ctk.CTkButton(self.root, image=self.image_button("update.png", (32, 32)), text="", width=30,
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"), command=self.update_product)
        btn_update.grid(column=2, row=0, padx=1)

        btn_delete = ctk.CTkButton(self.root, image=self.image_button("delete.png", (28, 28)), text="", width=30,
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"), command=self.delete_product)
        btn_delete.grid(column=3, row=0)

    def widgets_top(self):
        self.frame_top = ctk.CTkFrame(self.root, width=990, height=200)
        self.frame_top.place(y=40)

        ctk.CTkLabel(self.frame_top, text="Código", font=("Cascadia Code", 12.5)).place(x=5, y=5)
        self.code_entry = ctk.CTkEntry(self.frame_top, width=45, justify=CENTER, 
                                       font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9", fg_color="transparent")
        self.code_entry.bind("<Key>", lambda e: "break")
        self.code_entry.place(x=5, y=30)

        ctk.CTkLabel(self.frame_top, text="Produto", font=("Cascadia Code", 13)).place(x=55, y=5)
        ctk.CTkLabel(self.frame_top, text="(obrigatório)", font=("Cascadia Code", 10, "italic")).place(x=115, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top, width=350, font=("Cascadia Code", 13), fg_color="transparent")
        self.produto_entry.place(x=55, y=30)

        ctk.CTkLabel(self.frame_top, text="Medida", font=("Cascadia Code", 13)).place(x=410, y=5)
        self.medida_entry = ctk.CTkEntry(self.frame_top, width=75, font=("Cascadia Code", 13), fg_color="transparent")
        self.medida_entry.place(x=410, y=30)

        ctk.CTkLabel(self.frame_top, text="Grupo do Produto", font=("Cascadia Code", 13)).place(x=490, y=5)
        self.grupo_entry = ctk.CTkEntry(self.frame_top, width=150, font=("Cascadia Code", 13), fg_color="transparent")
        self.grupo_entry.place(x=490, y=30)

        ctk.CTkLabel(self.frame_top, text="Estoque Mín.", font=("Cascadia Code", 13)).place(x=650, y=5)
        self.min_entry = ctk.CTkEntry(self.frame_top, width=100, font=("Cascadia Code", 13), fg_color="transparent")
        self.min_entry.place(x=650, y=30)

        ctk.CTkLabel(self.frame_top, text="Fornecedor", font=("Cascadia Code", 13)).place(x=5, y=60)
        self.fornecedor_entry = ctk.CTkEntry(self.frame_top, width=250, font=("Cascadia Code", 13), fg_color="transparent")
        self.fornecedor_entry.place(x=5, y=85)

        ctk.CTkLabel(self.frame_top, text="Responsável", font=("Cascadia Code", 13)).place(x=260, y=60)
        self.responsavel_entry = ctk.CTkEntry(self.frame_top, width=200, font=("Cascadia Code", 13), fg_color="transparent")
        self.responsavel_entry.place(x=260, y=85)

        ctk.CTkLabel(self.frame_top, text="Fone 1", font=("Cascadia Code", 13)).place(x=5, y=115)
        self.fone1_entry = ctk.CTkEntry(self.frame_top, width=140, font=("Cascadia Code", 13), fg_color="transparent")
        self.fone1_entry.place(x=5, y=140)

        ctk.CTkLabel(self.frame_top, text="Fone 2", font=("Cascadia Code", 13)).place(x=150, y=115)
        self.fone2_entry = ctk.CTkEntry(self.frame_top, width=140, font=("Cascadia Code", 13), fg_color="transparent")
        self.fone2_entry.place(x=150, y=140)

        ctk.CTkLabel(self.frame_top, text="Nota Fiscal", font=("Cascadia Code", 13)).place(x=320, y=115)
        self.nf_entry = ctk.CTkEntry(self.frame_top, width=140, font=("Cascadia Code", 13), fg_color="transparent")
        self.nf_entry.place(x=320, y=140)

        ctk.CTkLabel(self.frame_top, text="CÓDIGO DE BARRAS", width=250, height=85, bg_color="#808080").place(x=500, y=85)

        ctk.CTkLabel(self.frame_top, text="IMAGEM", width=220, height=190, bg_color="#808080").place(x=765, y=5)

        ctk.CTkLabel(self.frame_top, text="Duplo CLICK para selecionar um produto!", font=("Cascadia Code", 12, "bold")).place(x=10, y=179)

    def widgets_bottom(self):
        self.frame_bottom = ctk.CTkFrame(self.root, width=990, height=286, border_width=1, border_color="#000")
        self.frame_bottom.place(y=245)

        # TREEVIEW ------------------------------------------------------------------------
        self.lista_produtos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'medida', 'grupo', 'forne', 'estoque', 'mín', 'nf',
            'resp', 'fone1', 'fone2',
        ))
        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("id", text="Código")
        self.lista_produtos.heading("produto", text="Produto")
        self.lista_produtos.heading("medida", text="Medida")
        self.lista_produtos.heading("grupo", text="Grupo do Produto")
        self.lista_produtos.heading("forne", text="Fornecedor")
        self.lista_produtos.heading("estoque", text="Estoque")
        self.lista_produtos.heading("mín", text="Est.Mín.")
        self.lista_produtos.heading("nf", text="NF")

        self.lista_produtos.heading("resp", text="Responsável")
        self.lista_produtos.heading("fone1", text="Fone_1")
        self.lista_produtos.heading("fone2", text="Fone_2")

        self.lista_produtos.column("#0", width=0, stretch=False)
        self.lista_produtos.column("id", width=50)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("medida", width=85)
        self.lista_produtos.column("grupo", width=150)
        self.lista_produtos.column("forne", width=170)
        self.lista_produtos.column("estoque", width=75)
        self.lista_produtos.column("mín", width=50)
        self.lista_produtos.column("nf", width=95)

        self.lista_produtos.column("resp", width=0, stretch=False)
        self.lista_produtos.column("fone1", width=0, stretch=False)
        self.lista_produtos.column("fone2", width=0, stretch=False)

        self.lista_produtos.place(width=970, height=286)
        # ----------------------------------------------------------------------------------

        # SCROLLBAR
        scrollbar_y = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_produtos.yview)
        self.lista_produtos.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.place(x=970, y=0, width=20, height=278)

        # SELECIONA DADOS DA TABELA/TREEVIEW
        self.lista_produtos.bind("<Double-1>", self.on_DoubleClick)
        
        self.select_database()


class TabEntrada(FunctionsEntrada, Functions):
    def __init__(self, root):
        self.root = root
        
        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()
        self.view_bottom()
        
    def buttons_header(self):
        btn_save = ctk.CTkButton(self.root, image=self.image_button("save.png", (40, 40)), text="", width=30,
                                compound=LEFT, anchor=NW, fg_color="transparent", hover_color=("#D3D3D3", "#363636"), 
                                command=self.save)
        btn_save.grid(column=0, row=0, padx=1)
        
    def widgets_top(self):
        self.frame_top = ctk.CTkFrame(self.root, width=990, height=140, border_width=1, border_color="#000")
        self.frame_top.place(y=45)
        
        self.sub_frame_top = ctk.CTkFrame(self.frame_top, width=155, height=130, border_width=1, border_color="#000")
        self.sub_frame_top.place(x=820, y=5)
        
        ctk.CTkLabel(self.frame_top, text="Registro", font=("Cascadia Code", 12.5)).place(x=5, y=5)
        self.reg_entry = ctk.CTkEntry(self.frame_top, width=55, justify=CENTER,
                                       font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9", fg_color="transparent")
        self.reg_entry.bind("<Key>", lambda e: "break")
        self.reg_entry.place(x=5, y=30)
        
        ctk.CTkLabel(self.frame_top, text="Últ. Registro", font=("Cascadia Code", 13)).place(x=70, y=5)
        self.data_register = ctk.CTkEntry(self.frame_top, width=105, justify=CENTER, 
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9", fg_color="transparent")
        self.data_register.bind("<Key>", lambda e: "break")
        self.data_register.place(x=70, y=30)
        
        ctk.CTkLabel(self.frame_top, text="Produto", font=("Cascadia Code", 13)).place(x=185, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top, width=350, font=("Cascadia Code", 13), fg_color="transparent")
        self.produto_entry.place(x=185, y=30)
        
        ctk.CTkLabel(self.frame_top, text="Medida", font=("Cascadia Code", 13)).place(x=545, y=5)
        self.medida_entry = ctk.CTkEntry(self.frame_top, width=100, justify=CENTER, 
                                          font=("Cascadia Code", 13), fg_color="transparent")
        self.medida_entry.place(x=545, y=30)
        
        ctk.CTkLabel(self.frame_top, text="Grupo do Produto", font=("Cascadia Code", 13)).place(x=655, y=5)
        self.grupo_entry = ctk.CTkEntry(self.frame_top, width=150, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.grupo_entry.place(x=655, y=30)
        
        ctk.CTkLabel(self.sub_frame_top, text="Qtd. Entrada", font=("Cascadia Code", 13)).place(x=30, y=1)
        self.quantidade_entry = ctk.CTkEntry(self.sub_frame_top, width=75, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.quantidade_entry.place(x=42, y=24)
        
        ctk.CTkLabel(self.frame_top, text="Nota Fiscal", font=("Cascadia Code", 13)).place(x=5, y=70)
        self.nf_entry = ctk.CTkEntry(self.frame_top, width=150, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.nf_entry.place(x=5, y=95)
        
        ctk.CTkLabel(self.frame_top, text="Fornecedor", font=("Cascadia Code", 13)).place(x=165, y=70)
        self.fornecedor_entry = ctk.CTkEntry(self.frame_top, width=350, font=("Cascadia Code", 13), fg_color="transparent")
        self.fornecedor_entry.place(x=165, y=95)
        
        ctk.CTkLabel(self.frame_top, text="Nº Lote", font=("Cascadia Code", 13)).place(x=525, y=70)
        self.lote_entry = ctk.CTkEntry(self.frame_top, width=100, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.lote_entry.place(x=525, y=95)
        
        ctk.CTkLabel(self.frame_top, text="Status Lote", font=("Cascadia Code", 13)).place(x=635, y=70)
        self.status_entry = ctk.CTkEntry(self.frame_top, width=150, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.status_entry.place(x=635, y=95)
        
        ctk.CTkLabel(self.sub_frame_top, text="Estoque Lote", font=("Cascadia Code", 13)).place(x=30, y=71)
        self.estoque_entry = ctk.CTkEntry(self.sub_frame_top, width=75, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.estoque_entry.place(x=42, y=96)

    def widgets_bottom(self):
        self.frame_bottom = ctk.CTkFrame(self.root, width=990, height=335, border_width=1, border_color="#000")
        self.frame_bottom.place(y=190)
        
        ctk.CTkLabel(self.frame_bottom, text="Rastreamento de Lotes - (duplo CLICK para selecionar um produto)", 
                     font=("Cascadia Code", 12, "bold")).place(x=10, y=1)
        
        ctk.CTkLabel(self.frame_bottom, text="Mês", font=("Cascadia Code", 13)).place(x=5, y=30)
        self.filter_mes = ctk.CTkEntry(self.frame_bottom, width=50, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.filter_mes.place(x=5, y=55)
        
        ctk.CTkLabel(self.frame_bottom, text="Ano", font=("Cascadia Code", 13)).place(x=65, y=30)
        self.filter_ano = ctk.CTkEntry(self.frame_bottom, width=50, justify=CENTER, 
                                       font=("Cascadia Code", 13), fg_color="transparent")
        self.filter_ano.place(x=65, y=55)
        
        ctk.CTkButton(self.frame_bottom, image=self.image_button("clear-filters.png", (20, 20)), compound=RIGHT,
                      width=30, text="LIMPAR", font=("Cascadia Code", 13, "bold"), text_color=("#FFF", "#000"),
                      fg_color=("#363636", "#D3D3D3"), command=None).place(x=125, y=55)
        
    def view_bottom(self):
        # TREEVIEW ------------------------------------------------------------------------
        self.lista_produtos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'data', 'produto', 'medida', 'lote', 'estoque', 'fornecedor', 'nf', 'status',
            'grupo', 
        ))
        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("id", text="Registro")
        self.lista_produtos.heading("data", text="Data")
        self.lista_produtos.heading("produto", text="Produto")
        self.lista_produtos.heading("medida", text="Medida")
        self.lista_produtos.heading("lote", text="Lote")
        self.lista_produtos.heading("estoque", text="Qtd")
        self.lista_produtos.heading("fornecedor", text="Fornecedor")
        self.lista_produtos.heading("nf", text="NF")
        self.lista_produtos.heading("status", text="Status")
        self.lista_produtos.heading("grupo", text="Grupo do Produto")

        self.lista_produtos.column("#0", width=0, stretch=False)
        self.lista_produtos.column("id", width=50)
        self.lista_produtos.column("data", width=100)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("medida", width=85)
        self.lista_produtos.column("lote", width=85)
        self.lista_produtos.column("estoque", width=75)
        self.lista_produtos.column("fornecedor", width=220)
        self.lista_produtos.column("nf", width=95)
        self.lista_produtos.column("status", width=125)
        self.lista_produtos.column("grupo", width=150)

        self.lista_produtos.place(y=88, width=970, height=330)
        # ----------------------------------------------------------------------------------
        
        # SCROLLBAR
        scrollbar_y = ttk.Scrollbar(self.frame_bottom, orient="vertical", command=self.lista_produtos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_bottom, orient="horizontal", command=self.lista_produtos.xview)
        self.lista_produtos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=88, width=20, height=245)
        scrollbar_x.place(x=0, y=315, width=970, height=20)
        
        # SELECIONA DADOS DA TABELA/TREEVIEW
        self.lista_produtos.bind("<Double-1>", self.on_DoubleClick)

        self.select_database()


if __name__ == "__main__":
    Application()

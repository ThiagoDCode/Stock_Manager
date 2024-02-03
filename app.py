from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

from lib_tabEstoque import Register
from lib_functions import Functions


class Application:
    def __init__(self):
        self.root = ctk.CTk()

        self.layout_config()
        self.appearance_theme()
        self.tabs_application()

        self.root.mainloop()

    def layout_config(self):
        self.root.title("Controle de Estoque")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

    def appearance_theme(self):
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("system")

        ctk.CTkLabel(self.root, text="Tema", font=(
            "Cascadia Code", 15)).place(x=860, y=571)
        ctk.CTkOptionMenu(self.root, width=90, height=20, values=['System', 'Light', 'Dark'], font=("Cascadia Code", 15),
                          command=ctk.set_appearance_mode).place(x=900, y=575)

    def tabs_application(self):
        self.tabs_view = ctk.CTkTabview(
            self.root, width=1000, height=570, anchor="w", text_color=('#000', '#FFF'))
        self.tabs_view.pack()

        self.tabs_view.add("Resumos")

        self.tabs_view.add("Produtos e Estoque")
        TabEstoque(self.tabs_view.tab("Produtos e Estoque"))

        self.tabs_view.add("Movimento de Produtos")

        self.tabs_view.set("Produtos e Estoque")


class TabEstoque(Register, Functions):
    def __init__(self, root):
        self.root = root

        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()

    def buttons_header(self):
        btn_add = ctk.CTkButton(self.root, image=self.image_button("add.png", (34, 34)), text="", width=30, 
                                compound=LEFT, anchor=NW, fg_color="transparent", hover_color="#363636", command=self.register_product)
        btn_add.grid(column=0, row=0, padx=1)

        btn_search = ctk.CTkButton(self.root, image=self.image_button("search.png", (34, 34)), text="", width=30, 
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color="#363636", command=self.search_product)
        btn_search.grid(column=1, row=0, padx=1)

        btn_update = ctk.CTkButton(self.root, image=self.image_button("update.png", (32, 32)), text="", width=30, 
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color="#363636", command=self.update_product)
        btn_update.grid(column=2, row=0, padx=1)

        btn_delete = ctk.CTkButton(self.root, image=self.image_button("delete.png", (28, 28)), text="", width=30, 
                                   compound=LEFT, anchor=NW, fg_color="transparent", hover_color="#363636", command=self.delete_product)
        btn_delete.grid(column=3, row=0)

    def widgets_top(self):
        self.frame_top = ctk.CTkFrame(
            self.root, width=990, height=200)
        self.frame_top.place(y=40)

        ctk.CTkLabel(self.frame_top, text="Código", font=(
            "Cascadia Code", 12.5)).place(x=5, y=5)
        self.code_entry = ctk.CTkEntry(
            self.frame_top, width=45, font=("Cascadia Code", 13))
        self.code_entry.place(x=5, y=30)

        ctk.CTkLabel(self.frame_top, text="Produto", font=(
            "Cascadia Code", 13)).place(x=55, y=5)
        ctk.CTkLabel(self.frame_top, text="(obrigatório)", font=(
            "Cascadia Code", 10, "italic")).place(x=115, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top, width=350, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.produto_entry.place(x=55, y=30)

        ctk.CTkLabel(self.frame_top, text="Medida", font=(
            "Cascadia Code", 13)).place(x=410, y=5)
        self.medida_entry = ctk.CTkEntry(self.frame_top, width=75, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.medida_entry.place(x=410, y=30)

        ctk.CTkLabel(self.frame_top, text="Grupo do Produto",
                     font=("Cascadia Code", 13)).place(x=490, y=5)
        self.grupo_entry = ctk.CTkEntry(self.frame_top, width=150, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.grupo_entry.place(x=490, y=30)

        ctk.CTkLabel(self.frame_top, text="Estoque Mín.",
                     font=("Cascadia Code", 13)).place(x=650, y=5)
        self.min_entry = ctk.CTkEntry(self.frame_top, width=100, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.min_entry.place(x=650, y=30)

        ctk.CTkLabel(self.frame_top, text="Fornecedor",
                     font=("Cascadia Code", 13)).place(x=5, y=60)
        self.fornecedor_entry = ctk.CTkEntry(self.frame_top, width=250, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.fornecedor_entry.place(x=5, y=85)

        ctk.CTkLabel(self.frame_top, text="Responsável",
                     font=("Cascadia Code", 13)).place(x=260, y=60)
        self.responsavel_entry = ctk.CTkEntry(self.frame_top, width=200, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.responsavel_entry.place(x=260, y=85)

        ctk.CTkLabel(self.frame_top, text="Fone 1", font=(
            "Cascadia Code", 13)).place(x=5, y=115)
        self.fone1_entry = ctk.CTkEntry(self.frame_top, width=140, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.fone1_entry.place(x=5, y=140)

        ctk.CTkLabel(self.frame_top, text="Fone 2", font=(
            "Cascadia Code", 13)).place(x=150, y=115)
        self.fone2_entry = ctk.CTkEntry(self.frame_top, width=140, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.fone2_entry.place(x=150, y=140)

        ctk.CTkLabel(self.frame_top, text="Nota Fiscal", font=(
            "Cascadia Code", 13)).place(x=320, y=115)
        self.nf_entry = ctk.CTkEntry(self.frame_top, width=140, font=(
            "Cascadia Code", 13), fg_color="transparent")
        self.nf_entry.place(x=320, y=140)

        ctk.CTkLabel(self.frame_top, text="CÓDIGO DE BARRAS", width=250,
                     height=85, bg_color="#808080").place(x=500, y=85)

        ctk.CTkLabel(self.frame_top, text="IMAGEM", width=220,
                     height=190, bg_color="#808080").place(x=765, y=5)
        
        ctk.CTkLabel(self.frame_top, text="Dobro click para selecionar um produto!", 
                     font=("Cascadia Code", 12, "bold")).place(x=10, y=179)

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

        self.lista_produtos.column("#0", width=1)
        self.lista_produtos.column("id", width=50)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("medida", width=85)
        self.lista_produtos.column("grupo", width=150)
        self.lista_produtos.column("forne", width=170)
        self.lista_produtos.column("estoque", width=75)
        self.lista_produtos.column("mín", width=50)
        self.lista_produtos.column("nf", width=95)
        
        self.lista_produtos.column("resp", width=50)
        self.lista_produtos.column("fone1", width=50)
        self.lista_produtos.column("fone2", width=50)

        self.lista_produtos.place(width=970, height=286)
        # ----------------------------------------------------------------------------------
        
        # SCROLLBAR
        scroll_tree = Scrollbar(self.frame_bottom, orient="vertical")
        self.lista_produtos.configure(yscroll=scroll_tree.set)
        scroll_tree.place(x=970, y=0, width=20, height=278)
        
        # SELECIONA DADOS DA TABELA/TREEVIEW
        self.lista_produtos.bind("<Double-1>", self.on_DoubleClick)

        self.select_database()


if __name__ == "__main__":
    Application()

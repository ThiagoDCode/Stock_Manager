from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import awesometkinter as atk

from con_database import *
from functions_base import *


class FunctionsEntradas:
    pass


class TabEntradas(Functions):
    def __init__(self, root):
        self.root = root

        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()
        self.view_bottom()

    def buttons_header(self):
        btn_save = ctk.CTkButton(self.root, image=self.image_button("save.png", (40, 40)),
                                 text="", width=30, compound=LEFT, anchor=NW, fg_color="transparent",
                                 hover_color=("#D3D3D3", "#363636"), command=None)
        btn_save.grid(column=0, row=0)
        atk.tooltip(btn_save, "Salvar Registro")

    def widgets_top(self):
        self.frame_top = ctk.CTkFrame(
            self.root, width=990, height=195, border_width=1, border_color="#000")
        self.frame_top.place(y=45)

        ctk.CTkLabel(self.frame_top, text="Código",
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=5)
        self.cod_entry = ctk.CTkEntry(self.frame_top,
                                      width=55,
                                      justify=CENTER,
                                      font=("Cascadia Code", 13), text_color="#A9A9A9",
                                      fg_color="transparent")
        self.cod_entry.bind("<Key>", lambda e: "break")
        self.cod_entry.place(x=5, y=30)

        ctk.CTkLabel(self.frame_top, text="Últ. Registro",
                     font=("Cascadia Code", 13)
                     ).place(x=70, y=5)
        self.data_register = ctk.CTkEntry(self.frame_top,
                                          width=105,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                          fg_color="transparent")
        self.data_register.bind("<Key>", lambda e: "break")
        self.data_register.place(x=70, y=30)

        ctk.CTkLabel(self.frame_top, text="Produto",
                     font=("Cascadia Code", 13)
                     ).place(x=185, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top,
                                          width=350,
                                          font=("Cascadia Code", 13),
                                          fg_color="transparent")
        self.produto_entry.place(x=185, y=30)

        lista_grupo = ""
        ctk.CTkLabel(self.frame_top, text="Departamento",
                     font=("Cascadia Code", 13)
                     ).place(x=545, y=5)
        self.grupo_listBox = ctk.CTkComboBox(self.frame_top,
                                             width=200,
                                             values=lista_grupo,
                                             font=("Cascadia Code", 13))
        self.grupo_listBox.set("")
        self.grupo_listBox.place(x=545, y=30)

        lista_fornecedor = ""
        ctk.CTkLabel(self.frame_top, text="Fornecedor",
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=70)
        self.fornecedor_listBox = ctk.CTkComboBox(self.frame_top,
                                                  width=200,
                                                  values=lista_fornecedor,
                                                  font=("Cascadia Code", 13))
        self.fornecedor_listBox.set("")
        self.fornecedor_listBox.place(x=5, y=95)

        ctk.CTkLabel(self.frame_top, text="Nota Fiscal",
                     font=("Cascadia Code", 13)
                     ).place(x=215, y=70)
        self.nf_entry = ctk.CTkEntry(self.frame_top,
                                     width=140,
                                     justify=CENTER,
                                     font=("Cascadia Code", 13),
                                     fg_color="transparent")
        self.nf_entry.place(x=215, y=95)

        ctk.CTkLabel(self.frame_top, text="Nº Lote",
                     font=("Cascadia Code", 13)
                     ).place(x=555, y=70)
        self.lote_entry = ctk.CTkEntry(self.frame_top,
                                       width=65,
                                       justify=CENTER,
                                       font=("Cascadia Code", 13),
                                       fg_color="transparent")
        self.lote_entry.place(x=555, y=95)

        lista_medida = ""
        ctk.CTkLabel(self.frame_top, text="Medida",
                     font=("Cascadia Code", 13)
                     ).place(x=630, y=70)
        self.medida_listBox = ctk.CTkComboBox(self.frame_top,
                                              width=115,
                                              values=lista_medida,
                                              font=("Cascadia Code", 13),
                                              justify=CENTER)
        self.medida_listBox.set("")
        self.medida_listBox.place(x=630, y=95)
        
        self.barcode_entry = ctk.CTkEntry(self.frame_top, 
                                          width=220, height=20, 
                                          justify=CENTER, 
                                          placeholder_text="Código de Barras", 
                                          font=("Cascadia Code", 13, "bold"), 
                                          corner_radius=3)
        self.barcode_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.barcode_entry.place(x=5, y=160)
        
        ctk.CTkLabel(self.frame_top, text="VALOR DE ENTRADA",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=515, y=130)
        self.valor_revenda = ctk.CTkEntry(self.frame_top,
                                          width=110,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13),
                                          placeholder_text="R$ custos",
                                          fg_color="transparent")
        self.valor_revenda.place(x=515, y=160)
        
        ctk.CTkLabel(self.frame_top, text="VALOR DE SAÍDA",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=635, y=130)
        self.valor_revenda = ctk.CTkEntry(self.frame_top,
                                          width=110,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13), 
                                          placeholder_text="R$ revenda",
                                          fg_color="transparent")
        self.valor_revenda.place(x=635, y=160)

        # SUB_FRAME ENTRADAS ---------------------------------------------------------------------------------
        self.frame_entradas = atk.Frame3d(self.frame_top)
        self.frame_entradas.place(x=755, y=5, width=230, height=185)

        ctk.CTkLabel(self.frame_entradas, text="Qtd. Entrada",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=10)
        self.qdt_entrada = ctk.CTkEntry(self.frame_entradas,
                                        width=75,
                                        justify=CENTER,
                                        font=("Cascadia Code", 13),
                                        fg_color="#363636", bg_color="#363636")
        self.qdt_entrada.place(x=10, y=35)
        ctk.CTkLabel(self.frame_entradas, text="MEDIDA",
                     font=("Cascadia Code", 13, "italic"), text_color="#A9A9A9",
                     fg_color="#363636", bg_color="#C0C0C0"
                     ).place(x=90, y=35)

        ctk.CTkLabel(self.frame_entradas, text="Estoque Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=65)
        self.estoque_entry = ctk.CTkEntry(self.frame_entradas,
                                          width=75,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13, "bold"),
                                          fg_color="#363636", bg_color="#363636",
                                          corner_radius=3)
        self.estoque_entry.place(x=10, y=90)
        ctk.CTkLabel(self.frame_entradas, text="MEDIDA",
                     font=("Cascadia Code", 13, "italic"), text_color="#A9A9A9",
                     fg_color="#363636", bg_color="#C0C0C0"
                     ).place(x=90, y=90)
        
        ctk.CTkLabel(self.frame_entradas, text="Estoque Mín.",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=120)
        self.estoque_entry = ctk.CTkEntry(self.frame_entradas,
                                          width=75,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13, "bold"),
                                          fg_color="#363636", bg_color="#363636",
                                          corner_radius=3)
        self.estoque_entry.place(x=10, y=145)
        
        ctk.CTkLabel(self.frame_entradas, text="Status Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=126, y=120)
        self.status_entry = ctk.CTkEntry(self.frame_entradas,
                                         width=100,
                                         justify=CENTER, 
                                         font=("Cascadia Code", 13, "bold"),
                                         fg_color="#363636", bg_color="#363636",
                                         corner_radius=2)
        self.status_entry.place(x=120, y=145)
        # -----------------------------------------------------------------------------------------------------
        
    def widgets_bottom(self):
        self.frame_bottom = ctk.CTkFrame(self.root, 
                                         width=990, height=315,
                                         border_width=1, border_color="#000")
        self.frame_bottom.place(y=240)
        
        ctk.CTkLabel(self.frame_bottom, text="Rastreamento de Lotes - (duplo CLICK para selecionar um produto!)",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=10, y=1)
        
    def view_bottom(self):
        self.lista_produtos = ttk.Treeview(self.frame_bottom, 
                                           height=3,
                                           column=(
                                               'id', 'data', 'produto', 'medida', 'lote', 'estoque', 
                                               'fornecedor', 'nf', 'grupo', 'status'
                                           ))
        
        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("id", text="Cód.")
        self.lista_produtos.heading("data", text="Data")
        self.lista_produtos.heading("produto", text="Produto")
        self.lista_produtos.heading("medida", text="Medida")
        self.lista_produtos.heading("lote", text="Nº Lote")
        self.lista_produtos.heading("estoque", text="Estoque")
        self.lista_produtos.heading("fornecedor", text="Fornecedor")
        self.lista_produtos.heading("nf", text="NF")
        self.lista_produtos.heading("grupo", text="Departamento")
        self.lista_produtos.heading("status", text="Status")
        
        self.lista_produtos.column("#0", width=0, stretch=False)
        self.lista_produtos.column("id", width=35)
        self.lista_produtos.column("data", width=75)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("medida", width=85)
        self.lista_produtos.column("lote", width=50)
        self.lista_produtos.column("estoque", width=50)
        self.lista_produtos.column("fornecedor", width=150)
        self.lista_produtos.column("nf", width=85)
        self.lista_produtos.column("grupo", width=125)
        self.lista_produtos.column("status", width=70)
        
        self.lista_produtos.place(y=88, width=970, height=180)
        
        # SCROLLBAR -----------------------------------------------------------------------------------------
        scrollbar_y = ttk.Scrollbar(self.frame_bottom, 
                                    orient="vertical",
                                    command=self.lista_produtos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_bottom,
                                    orient="horizontal",
                                    command=self.lista_produtos.xview)
        self.lista_produtos.configure(yscrollcommand=scrollbar_y.set, 
                                      xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=88, width=20, height=200)
        scrollbar_x.place(x=0, y=268, width=970, height=20)
        # ---------------------------------------------------------------------------------------------------

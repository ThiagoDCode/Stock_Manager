from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import awesometkinter as atk
from tkcalendar import DateEntry

from con_database import *
from functions_base import *


class Functions(Database):
    pass


class TabSaidas(Functions, FunctionsExtras):
    def __init__(self, root):
        self.root = root
        
        self.buttons_header()
        self.widgets_top()
    
    def buttons_header(self):
        self.frame_buttons = ctk.CTkFrame(self.root,
                                          width=990, height=40,
                                          fg_color="#363636")
        self.frame_buttons.place(x=1, y=1)

        btn_save = ctk.CTkButton(self.frame_buttons, text="",
                                 width=30,
                                 corner_radius=3,
                                 image=self.image_button("save.png", (26, 26)),
                                 compound=LEFT, anchor=NW,
                                 fg_color="transparent",
                                 hover_color=("#D3D3D3", "#4F4F4F"),
                                 command=None)
        btn_save.place(x=3, y=3)
        atk.tooltip(btn_save, "Salvar Registro")

        ctk.CTkLabel(self.frame_buttons, text="||",
                     font=("Arial", 30), text_color="#696969",
                     fg_color="transparent").place(x=40)

        btn_clear = ctk.CTkButton(self.frame_buttons, text="",
                                  width=30,
                                  corner_radius=3,
                                  image=self.image_button("clear-entries.png", (26, 26)),
                                  compound=LEFT, anchor=NW,
                                  fg_color="transparent",
                                  hover_color=("#D3D3D3", "#4F4F4F"),
                                  command=None)
        btn_clear.place(x=57, y=3)
        atk.tooltip(btn_clear, "Limpar campos de dados")
        
    def widgets_top(self):
        self.frame_top = ctk.CTkFrame(self.root,
                                      width=990, height=195,
                                      border_width=1, border_color="#000")
        self.frame_top.place(y=45)
        
        ctk.CTkLabel(self.frame_top, text="Código",
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=5)
        self.cod_entry = ctk.CTkEntry(self.frame_top,
                                      width=55,
                                      justify=CENTER,
                                      font=("Cascadia Code", 13), text_color="#A9A9A9",
                                      fg_color="transparent")
        self.cod_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.cod_entry.place(x=5, y=30)

        ctk.CTkLabel(self.frame_top, text="Últ. Entrada",
                     font=("Cascadia Code", 13)
                     ).place(x=70, y=5)
        self.data_entry = ctk.CTkEntry(self.frame_top,
                                       width=105,
                                       justify=CENTER,
                                       font=("Cascadia Code", 13), text_color="#A9A9A9",
                                       fg_color="transparent")
        self.data_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.data_entry.place(x=70, y=30)

        ctk.CTkLabel(self.frame_top, text="Produto",
                     font=("Cascadia Code", 13)
                     ).place(x=185, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top,
                                          width=350,
                                          font=("Cascadia Code", 13), text_color="#A9A9A9",
                                          fg_color="transparent")
        self.produto_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.produto_entry.place(x=185, y=30)

        lista_grupo = self.dql_database(
            "SELECT grupo FROM estoque", column_names=True)
        ctk.CTkLabel(self.frame_top, text="Departamento",
                     font=("Cascadia Code", 13)
                     ).place(x=545, y=5)
        self.grupo_listBox = ctk.CTkComboBox(self.frame_top,
                                             width=200,
                                             values=lista_grupo,
                                             font=("Cascadia Code", 13), text_color="#A9A9A9")
        self.grupo_listBox.set("")
        self.grupo_listBox.bind("<Key>", lambda e: self.entry_off(e))
        self.grupo_listBox.place(x=545, y=30)

        lista_fornecedor = self.dql_database(
            "SELECT fornecedor FROM estoque", column_names=True)
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

        lista_medida = self.dql_database(
            "SELECT medida FROM estoque", column_names=True)
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
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                          corner_radius=3)
        self.barcode_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.barcode_entry.place(x=5, y=160)

        ctk.CTkLabel(self.frame_top, text="VALOR DE ENTRADA",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=350, y=130)
        self.custo_entry = ctk.CTkEntry(self.frame_top,
                                        width=110,
                                        justify=CENTER,
                                        font=("Cascadia Code", 13),
                                        placeholder_text="R$ custos",
                                        fg_color="transparent")
        self.custo_entry.place(x=350, y=160)

        ctk.CTkLabel(self.frame_top, text="VALOR DE SAÍDA",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=500, y=130)
        self.revenda_entry = ctk.CTkEntry(self.frame_top,
                                          width=110,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13),
                                          placeholder_text="R$ revenda",
                                          fg_color="transparent")
        self.revenda_entry.place(x=500, y=160)

        ctk.CTkLabel(self.frame_top, text="Valor do Estoque",
                     font=("Cascadia Code", 13)
                     ).place(x=620, y=130)
        self.valor_entry = ctk.CTkEntry(self.frame_top,
                                        width=110,
                                        justify=CENTER,
                                        font=("Cascadia Code", 13), text_color="#A9A9A9",
                                        placeholder_text="R$ total",
                                        fg_color="transparent")
        self.valor_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.valor_entry.place(x=620, y=160)

        # SUB_FRAME ENTRADAS ---------------------------------------------------------------------------------
        self.frame_entradas = atk.Frame3d(self.frame_top)
        self.frame_entradas.place(x=755, y=5, width=230, height=185)

        ctk.CTkLabel(self.frame_entradas, text="Qtd. Entrada",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=10)
        self.qtd_entrada = ctk.CTkEntry(self.frame_entradas,
                                        width=75,
                                        justify=CENTER,
                                        font=("Cascadia Code", 13),
                                        fg_color="#363636", bg_color="#363636")
        self.qtd_entrada.place(x=10, y=35)

        ctk.CTkLabel(self.frame_entradas, text="Estoque Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=65)
        self.estoque_entry = ctk.CTkEntry(self.frame_entradas,
                                          width=75,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                          fg_color="#363636", bg_color="#363636",
                                          corner_radius=3)
        self.estoque_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.estoque_entry.place(x=10, y=90)
        self.lb_medida = ctk.CTkLabel(self.frame_entradas, text="MEDIDA",
                                      font=("Cascadia Code", 13, "italic"), text_color="#A9A9A9",
                                      fg_color="#363636", bg_color="#C0C0C0"
                                      )
        self.lb_medida.place(x=90, y=90)

        self.lb_ativo = ctk.CTkLabel(self.frame_entradas, text="",
                                     width=105, height=28,
                                     font=("Cascadia Code", 13, "bold"),
                                     text_color="#ADFF2F",
                                     fg_color="#363636", bg_color="#363636")
        self.lb_ativo.place(x=120, y=65)

        ctk.CTkLabel(self.frame_entradas, text="Estoque Mín.",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=120)
        self.min_entry = ctk.CTkEntry(self.frame_entradas,
                                      width=75,
                                      justify=CENTER,
                                      font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                      fg_color="#363636", bg_color="#363636",
                                      corner_radius=3)
        self.min_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.min_entry.place(x=10, y=145)

        ctk.CTkLabel(self.frame_entradas, text="Status Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=126, y=120)
        self.status_entry = ctk.CTkEntry(self.frame_entradas,
                                         width=100,
                                         justify=CENTER,
                                         font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                         fg_color="#363636", bg_color="#363636",
                                         corner_radius=2)
        self.status_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.status_entry.place(x=120, y=145)
        # -----------------------------------------------------------------------------------------------------

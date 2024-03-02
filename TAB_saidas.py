from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import awesometkinter as atk
from tkcalendar import DateEntry

from con_database import *
from functions_base import *


class Functions(Database):
    def variables_entries(self):
        self.code = self.cod_entry.get()
        self.data = self.data_entry.get()
        self.produto = self.produto_entry.get()
        self.grupo = self.grupo_listBox.get()
        self.fornecedor = self.fornecedor_listBox.get()
        self.nf = self.nf_entry.get()
        self.lote = self.lote_entry.get()
        self.barcode = self.barcode_entry.get()
        self.revenda = self.revenda_entry.get()
        self.saída = self.qtd_saída.get()
        self.estoque = self.estoque_entry.get()
        self.min = self.min_entry.get()
        self.status = self.status_entry.get()
    
    def clear_entries(self):
        self.cod_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.grupo_listBox.set("")
        self.fornecedor_listBox.set("")
        self.nf_entry.delete(0, END)
        self.lote_entry.delete(0, END)
        self.barcode_entry.delete(0, END)
        self.revenda_entry.delete(0, END)
        self.qtd_saída.delete(0, END)
        self.estoque_entry.delete(0, END)
        self.min_entry.delete(0, END)
        self.status_entry.delete(0, END)
    
    def on_doubleClick(self, event):
        self.clear_entries()
        
        for row in self.lista_produtos.selection():
            c1, c2, c3, c4, c5, c6, c7, c8, \
                c9, c10, c11, c12, c13, c14, c15 = \
                    self.lista_produtos.item(row, "values")
            
            self.cod_entry.insert(END, c1)
            self.produto_entry.insert(END, c2)
            self.nf_entry.insert(END, c3)
            self.lote_entry.insert(END, c4)
            self.estoque_entry.insert(END, c6)
            self.min_entry.insert(END, c7)
            self.fornecedor_listBox.set(c9)
            self.grupo_listBox.set(c10)
            self.status_entry.insert(END, c11)
            self.data_entry.insert(END, c12)
            self.barcode_entry.insert(END, c13)
            self.revenda_entry.insert(END, c14)
            
            self.últimas_saídas = c15
    
    def select_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())
        
        sql = """
            SELECT
                id, produto, nf, lote, medida, estoque, estoque_mín, valor_estoque, 
                fornecedor, grupo, status, data_saída, n_barcode, revenda, saídas
            FROM
                estoque
        """
        data_return = Database().dql_database(sql)
        
        if data_return is not None:
            for dados in data_return:
                self.lista_produtos.insert("", "end", values=dados)
        
        self.total_registros()
    
    def save_register(self):
        self.variables_entries()
        
        if self.code == "":
            messagebox.showerror(
                "ID invalid", message="Selecione o produto para saída!"
            )
        elif self.saída == "" or not self.saída.isdigit():
            messagebox.showerror(
                "Invalid input", message="Informe a quantidade de saída!"
            )
        
        else:
            if self.radio_button_var.get() == 0:
                messagebox.showerror(
                    "Invalid input", message="Selecione o tipo de saída: \n  Faturamento \n  Consumo Interno"
                )
            else:
                self.estoque = int(self.estoque) - int(self.saída)
                
                sql = """
                    UPDATE estoque SET
                        estoque=?, saídas=?, data_saída=?
                    WHERE
                        id=?
                """
                dados = [self.estoque, self.saída, self.data_saída.get(), 
                        self.code]
                self.dml_database(sql, dados)
            
            self.clear_entries()
            self.select_database()


class TabSaidas(Functions, FunctionsExtras):
    def __init__(self, root):
        self.root = root
        
        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()
        self.view_bottom()
    
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
                                 command=self.save_register)
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
                                  command=self.clear_entries)
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

        ctk.CTkLabel(self.frame_top, text="Últ. Saída",
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

        lista_grupo = self.dql_database("SELECT grupo FROM estoque", column_names=True)
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

        lista_fornecedor = self.dql_database("SELECT fornecedor FROM estoque", column_names=True)
        ctk.CTkLabel(self.frame_top, text="Fornecedor",
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=70)
        self.fornecedor_listBox = ctk.CTkComboBox(self.frame_top,
                                                  width=200,
                                                  values=lista_fornecedor,
                                                  font=("Cascadia Code", 13), text_color="#A9A9A9")
        self.fornecedor_listBox.set("")
        self.fornecedor_listBox.bind("<Key>", lambda e: self.entry_off(e))
        self.fornecedor_listBox.place(x=5, y=95)

        ctk.CTkLabel(self.frame_top, text="Nota Fiscal",
                     font=("Cascadia Code", 13)
                     ).place(x=215, y=70)
        self.nf_entry = ctk.CTkEntry(self.frame_top,
                                     width=140,
                                     justify=CENTER,
                                     font=("Cascadia Code", 13), text_color="#A9A9A9",
                                     fg_color="transparent")
        self.nf_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.nf_entry.place(x=215, y=95)

        ctk.CTkLabel(self.frame_top, text="Nº Lote", 
                     font=("Cascadia Code", 13)
                     ).place(x=365, y=70)
        self.lote_entry = ctk.CTkEntry(self.frame_top,
                                       width=65,
                                       justify=CENTER,
                                       font=("Cascadia Code", 13), text_color="#A9A9A9",
                                       fg_color="transparent")
        self.lote_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.lote_entry.place(x=365, y=95)

        self.barcode_entry = ctk.CTkEntry(self.frame_top,
                                          width=220, height=20,
                                          justify=CENTER,
                                          placeholder_text="Código de Barras",
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                          corner_radius=3)
        self.barcode_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.barcode_entry.place(x=5, y=160)
        
        self.radio_button_var = IntVar(value=0)
        r_button_faturamento = ctk.CTkRadioButton(self.frame_top, text="Faturamento",
                                                  font=("Cascadia Code", 13, "bold"), 
                                                  radiobutton_width=20, radiobutton_height=20,
                                                  variable=self.radio_button_var, 
                                                  value=1)
        r_button_faturamento.place(x=525, y=70)
        r_button_consumo = ctk.CTkRadioButton(self.frame_top, text="Consumo Interno",
                                              font=("Cascadia Code", 13, "bold"),
                                              radiobutton_width=20, radiobutton_height=20,
                                              variable=self.radio_button_var,
                                              value=2)
        r_button_consumo.place(x=525, y=100)

        ctk.CTkLabel(self.frame_top, text="VALOR DE SAÍDA",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=550, y=130)
        self.revenda_entry = ctk.CTkEntry(self.frame_top,
                                          width=110,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13), text_color="#A9A9A9",
                                          placeholder_text="R$ revenda",
                                          fg_color="transparent")
        self.revenda_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.revenda_entry.place(x=550, y=160)

        # SUB_FRAME ENTRADAS ---------------------------------------------------------------------------------
        self.frame_saídas = atk.Frame3d(self.frame_top)
        self.frame_saídas.place(x=755, y=5, width=230, height=185)

        ctk.CTkLabel(self.frame_saídas, text="Qtd. Saída",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=10)
        self.qtd_saída = ctk.CTkEntry(self.frame_saídas,
                                        width=75,
                                        justify=CENTER,
                                        font=("Cascadia Code", 13),
                                        fg_color="#363636", bg_color="#363636")
        self.qtd_saída.place(x=10, y=35)

        ctk.CTkLabel(self.frame_saídas, text="Estoque Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=65)
        self.estoque_entry = ctk.CTkEntry(self.frame_saídas,
                                          width=75,
                                          justify=CENTER,
                                          font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                          fg_color="#363636", bg_color="#363636",
                                          corner_radius=3)
        self.estoque_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.estoque_entry.place(x=10, y=90)
        self.lb_medida = ctk.CTkLabel(self.frame_saídas, text="MEDIDA",
                                      font=("Cascadia Code", 13, "italic"), text_color="#A9A9A9",
                                      fg_color="#363636", bg_color="#C0C0C0"
                                      )
        self.lb_medida.place(x=90, y=90)

        self.lb_ativo = ctk.CTkLabel(self.frame_saídas, text="",
                                     width=105, height=28,
                                     font=("Cascadia Code", 13, "bold"),
                                     text_color="#ADFF2F",
                                     fg_color="#363636", bg_color="#363636")
        self.lb_ativo.place(x=120, y=65)

        ctk.CTkLabel(self.frame_saídas, text="Estoque Mín.",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=10, y=120)
        self.min_entry = ctk.CTkEntry(self.frame_saídas,
                                      width=75,
                                      justify=CENTER,
                                      font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                      fg_color="#363636", bg_color="#363636",
                                      corner_radius=3)
        self.min_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.min_entry.place(x=10, y=145)

        ctk.CTkLabel(self.frame_saídas, text="Status Lote",
                     font=("Cascadia Code", 13),
                     fg_color="#363636", bg_color="#363636"
                     ).place(x=126, y=120)
        self.status_entry = ctk.CTkEntry(self.frame_saídas,
                                         width=100,
                                         justify=CENTER,
                                         font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9",
                                         fg_color="#363636", bg_color="#363636",
                                         corner_radius=2)
        self.status_entry.bind("<Key>", lambda e: self.entry_off(e))
        self.status_entry.place(x=120, y=145)
        # -----------------------------------------------------------------------------------------------------
    
    def widgets_bottom(self):
        self.frame_bottom = ctk.CTkFrame(self.root,
                                         width=990, height=315,
                                         fg_color="#363636")
        self.frame_bottom.place(y=240)

        ctk.CTkLabel(self.frame_bottom, text="Rastreamento de Lotes - (duplo CLICK para selecionar um produto!)",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=10, y=1)

        self.busca = ctk.CTkEntry(self.frame_bottom,
                                  width=350,
                                  placeholder_text="Buscar por Produto, Nº Lote ou Nota Fiscal",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=10, y=50)

        self.busca_mes = ctk.CTkEntry(self.frame_bottom,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mês",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=380, y=50)
        ctk.CTkLabel(self.frame_bottom, text="/",
                     font=("Cascadia Code", 20, "bold")
                     ).place(x=435, y=50)
        self.busca_ano = ctk.CTkEntry(self.frame_bottom,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Ano",
                                      font=("Cascadia Code", 13))
        self.busca_ano.place(x=450, y=50)
        
        # BUSCA POR DEPARTAMENTO OU FORNECEDOR

        ctk.CTkButton(self.frame_bottom, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=None).place(x=640, y=50)

        ctk.CTkButton(self.frame_bottom, text="LIMPAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=None).place(x=710, y=50)

        ctk.CTkLabel(self.frame_bottom, text="Data",
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=15, y=286)
        self.data_saída = DateEntry(self.frame_bottom)
        self.data_saída.place(x=60, y=290)
    
    def view_bottom(self):
        self.lista_produtos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'produto', 'nf', 'lote', 'medida', 'estoque', 
            'mínimo', 'valor', 'fornecedor', 'grupo', 'status',
            'data_saída', 'barcode', 'revenda', 'saídas'
        ))

        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("id", text="Cód.")
        self.lista_produtos.heading("produto", text="Produto")
        self.lista_produtos.heading("nf", text="NF")
        self.lista_produtos.heading("lote", text="Nº Lote")
        self.lista_produtos.heading("medida", text="Medida")
        self.lista_produtos.heading("estoque", text="Estoque")
        self.lista_produtos.heading("mínimo", text="Qtd.Mín")
        self.lista_produtos.heading("valor", text="Valor Estoque")
        self.lista_produtos.heading("fornecedor", text="Fornecedor")
        self.lista_produtos.heading("grupo", text="Departamento")
        self.lista_produtos.heading("status", text="Status")
        
        self.lista_produtos.heading("data_saída", text="")
        self.lista_produtos.heading("barcode", text="")
        self.lista_produtos.heading("revenda", text="")
        self.lista_produtos.heading("saídas", text="")

        self.lista_produtos.column("#0", width=0, stretch=False)
        self.lista_produtos.column("id", width=35, anchor=CENTER)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("nf", width=85, anchor=CENTER)
        self.lista_produtos.column("lote", width=50, anchor=CENTER)
        self.lista_produtos.column("medida", width=85, anchor=CENTER)
        self.lista_produtos.column("estoque", width=55, anchor=CENTER)
        self.lista_produtos.column("mínimo", width=55, anchor=CENTER)
        self.lista_produtos.column("valor", width=80, anchor=CENTER)
        self.lista_produtos.column("fornecedor", width=150)
        self.lista_produtos.column("grupo", width=125)
        self.lista_produtos.column("status", width=70, anchor=CENTER)
        
        self.lista_produtos.column("data_saída", width=0, stretch=False)
        self.lista_produtos.column("barcode", width=0, stretch=False)
        self.lista_produtos.column("revenda", width=0, stretch=False)
        self.lista_produtos.column("saídas", width=0, stretch=False)
        
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
        
        self.lista_produtos.bind("<Double-1>", self.on_doubleClick)
        
        self.select_database()
        
    def total_registros(self):
        total_registros = len(self.lista_produtos.get_children())
        ctk.CTkLabel(self.frame_bottom, text=f"Total de Registros: {total_registros}",
                     width=200,
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=750, y=288)

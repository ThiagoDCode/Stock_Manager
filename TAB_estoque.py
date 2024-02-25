from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk
import awesometkinter as atk
from tkcalendar import DateEntry
import os

from con_database import *
from functions_base import *


class FunctionsEstoque(Database):
    
    def add_barcode(self):
        if self.produto_entry.get() == "":
            messagebox.showinfo("Description", message="Por favor insira a descrição do produto!")
        else:
            self.num_barcode.delete(0, END)
            
            numbers = self.generate_barCode(self.lote_entry.get())
            if numbers:
                self.num_barcode.insert(END, numbers)
    
    def variables_entries(self):
        self.código = self.cod_entry.get()
        self.produto = self.produto_entry.get()
        self.grupo = self.grupo_listBox.get()
        self.medida = self.medida_listBox.get()
        self.fornecedor = self.fornecedor_listBox.get()
        self.resp = self.resp_entry.get()
        self.fone = self.fone_entry.get()
        self.nf = self.nf_entry.get()
        self.lote = self.lote_entry.get()
        self.estoque = self.estoque_entry.get()
        self.min = self.min_entry.get()
        self.custo = self.custo_entry.get()
        self.revenda = self.revenda_entry.get()

        self.data = self.data_registro.get()
        self.barcode = self.num_barcode.get()
        
        self.ativo = self.ativo_checkbox.get()
        
    def clear_entries(self):
        self.cod_entry.configure(state=NORMAL)
        self.cod_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.grupo_listBox.set("")
        self.medida_listBox.set("")
        self.fornecedor_listBox.set("")
        self.resp_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.nf_entry.delete(0, END)
        self.lote_entry.delete(0, END)
        self.estoque_entry.delete(0, END)
        self.min_entry.delete(0, END)
        self.custo_entry.delete(0, END)
        self.revenda_entry.delete(0, END)
        
        self.num_barcode.delete(0, END)
        self.img_barcode.configure(image=None)
    
    def select_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())

        query_select = """
            SELECT 
                id, data_entrada, produto, medida, grupo, fornecedor, lote, estoque, estoque_mín, nf, 
                status, responsável, fone, custo, revenda, n_barcode, ativo
            FROM estoque
        """

        data_return = Database().dql_database(query_select)

        if data_return is not None:
            for dado in data_return:
                self.lista_produtos.insert("", "end", values=dado)
        
        self.total_registries()
            
    def on_doubleClick(self, event):
        self.clear_entries()
        self.lista_produtos.selection()
        
        for row in self.lista_produtos.selection():
            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17 = self.lista_produtos.item(row, "values")
            self.cod_entry.insert(END, c1)
            self.cod_entry.configure(state=DISABLED)
            self.produto_entry.insert(END, c3)
            self.medida_listBox.set(c4)
            self.grupo_listBox.set(c5)
            self.fornecedor_listBox.set(c6)
            self.lote_entry.insert(END, c7)
            self.estoque_entry.insert(END, c8)
            self.min_entry.insert(END, c9)
            self.nf_entry.insert(END, c10)
            self.resp_entry.insert(END, c12)
            self.fone_entry.insert(END, c13)
            self.custo_entry.insert(END, c14)
            self.revenda_entry.insert(END, c15)
            
            self.num_barcode.insert(END, c16)
            if self.num_barcode.get() != "":
                try:
                    self.img_barcode.configure(image=self.image_barcode(f"{self.lote_entry.get()}.png", (222, 125)))
                except:
                    messagebox.showinfo("Not found", message="A imagem do código de barras não foi encontrado!")
                    
            self.check_var.set(c17)
    
    def register_product(self):
        self.variables_entries()

        if self.produto_entry.get() == "":
            messagebox.showinfo("Aviso", message="Insira a descrição do produto!")

        else:
            query_sql = """
                INSERT INTO estoque (
                    produto, grupo, medida, fornecedor, responsável, fone, nf, 
                    lote, estoque, estoque_mín, custo, revenda, data_entrada, n_barcode, ativo
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            
            if self.estoque == "": self.estoque = 0
            lista_dados = [self.produto, self.grupo, self.medida, self.fornecedor, 
                           self.resp, self.fone, self.nf, self.lote, self.estoque, 
                           self.min, self.custo, self.revenda, self.data, self.barcode, self.ativo]

            self.dml_database(query_sql, lista_dados)

            self.widgets_top()
            self.select_database()
    
    def update_product(self):
        self.variables_entries()

        if self.código == "" or not self.código.isdigit():
            messagebox.showerror("ID invalid", message="Selecione o produto a ser atualizado!")
        else:
            if self.produto == "":
                messagebox.showinfo("Aviso", message="Insira a descrição do produto!")
            else:
                query_sql = """
                    UPDATE estoque SET
                        produto=?, grupo=?, medida=?, lote=?, fornecedor=?, responsável=?, fone=?,
                        nf=?, estoque=?, estoque_mín=?, custo=?, revenda=?, data_entrada=?, n_barcode=?, ativo=?
                    WHERE id=?
                """
                lista_dados = [self.produto, self.grupo, self.medida, self.lote, self.fornecedor, 
                               self.resp, self.fone, self.nf, self.estoque, self.min, 
                               self.custo, self.revenda, self.data, self.barcode, self.ativo,
                               self.código]

                if messagebox.askyesno("Update", message="Atualizar Registro?"):
                    self.dml_database(query_sql, lista_dados)

                self.widgets_top()
                self.select_database()
    
    def delete_product(self):
        self.variables_entries()

        if self.código == "" or not self.código.isdigit():
            messagebox.showerror("ID invalid", message="Selecione o produto a ser excluído!")
        else:
            if messagebox.askyesno("Delete", message=f"Excluir o registro: {self.cod_entry.get()}?"):
                self.dml_delete(self.código)
                self.img_barcode.configure(image=None)
                try:
                    os.remove(f"./Stock_Manager/barCodes/{self.lote_entry.get()}.png")
                except:
                    pass

                self.widgets_top()
                self.select_database()

    def search_database(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())

        if self.produto_entry.get() == "" \
            and self.grupo_listBox.get() == "" \
                and self.lote_entry.get() == "" \
                    and self.fornecedor_listBox.get() == "" \
                        and self.nf_entry.get() == "":
            
            self.select_database()
        else:
            if self.produto_entry.get():
                self.produto_entry.insert(END, "%")
                target = "produto"
                busca = self.produto_entry.get()
                
            elif self.grupo_listBox.get():
                self.grupo_listBox.set(self.grupo_listBox.get() + "%")
                target = "grupo"
                busca = self.grupo_listBox.get()
                
            elif self.lote_entry.get():
                self.lote_entry.insert(END, "%")
                target = "lote"
                busca = self.lote_entry.get()
                
            elif self.fornecedor_listBox.get():
                self.fornecedor_listBox.set(self.fornecedor_listBox.get() + "%")
                target = "fornecedor"
                busca = self.fornecedor_listBox.get()
                
            elif self.nf_entry.get():
                self.nf_entry.insert(END, "%")
                target = "nf"
                busca = self.nf_entry.get()

            data_query = f"""
                        SELECT
                            id, data_entrada, produto, medida, grupo, fornecedor, lote, estoque, estoque_mín, 
                            nf, status, responsável, fone, custo, revenda, n_barcode
                        FROM 
                            estoque WHERE {target} LIKE '%{busca}%' ORDER BY produto ASC
                        """
            data_return = self.dql_database(data_query)

            for dados in data_return:
                self.lista_produtos.insert("", END, values=dados)
            
            self.total_registries()
        
        self.clear_entries()


class TabEstoque(FunctionsEstoque, Functions):
    def __init__(self, root):
        self.root = root
        
        self.buttons_header()
        self.widgets_top()
        self.widgets_bottom()
    
    def buttons_header(self):
        btn_add = ctk.CTkButton(self.root, text="",
                                image=self.image_button("add.png", (34, 34)), 
                                width=30,
                                compound=LEFT, anchor=NW, 
                                fg_color="transparent", 
                                hover_color=("#D3D3D3", "#363636"), 
                                command=self.register_product)
        btn_add.grid(column=0, row=0, padx=1)
        atk.tooltip(btn_add, "Cadastrar Produto")

        btn_search = ctk.CTkButton(self.root, text="",
                                   image=self.image_button("search.png", (34, 34)), 
                                   width=30, 
                                   compound=LEFT, anchor=NW, 
                                   fg_color="transparent", 
                                   hover_color=("#D3D3D3", "#363636"), 
                                   command=self.search_database)
        btn_search.grid(column=1, row=0, padx=1)
        atk.tooltip(btn_search, "Buscar Registro \n (Busca por: produto/departamento/fornecedor/lote/NF)")

        btn_update = ctk.CTkButton(self.root, text="",
                                   image=self.image_button("update.png", (32, 32)), 
                                   width=30,  
                                   compound=LEFT, anchor=NW, 
                                   fg_color="transparent", 
                                   hover_color=("#D3D3D3", "#363636"), 
                                   command=self.update_product)
        btn_update.grid(column=2, row=0, padx=1)
        atk.tooltip(btn_update, "Atualizar Registro")

        btn_delete = ctk.CTkButton(self.root, text="",
                                   image=self.image_button("delete.png", (28, 28)), 
                                   width=30,  
                                   compound=LEFT, anchor=NW, 
                                   fg_color="transparent", 
                                   hover_color=("#D3D3D3", "#363636"), 
                                   command=self.delete_product)
        btn_delete.grid(column=3, row=0)
        atk.tooltip(btn_delete, "Excluir Registro")
        
        ctk.CTkButton(self.root, text="|", 
                      width=30, 
                      font=("Arial", 25), 
                      fg_color="transparent"
                      ).grid(column=4, row=0)
        
        btn_clear = ctk.CTkButton(self.root, text="",
                                  image=self.image_button("clear-entries.png", (30, 30)), 
                                  width=30, 
                                  compound=LEFT, anchor=NW, 
                                  fg_color="transparent", 
                                  hover_color=("#D3D3D3", "#363636"),
                                  command=self.clear_entries)
        btn_clear.grid(column=5, row=0)
        atk.tooltip(btn_clear, "Limpar campos de dados")

    def widgets_top(self):  
        self.frame_top = ctk.CTkFrame(self.root, width=990, height=200)
        self.frame_top.place(y=40)

        ctk.CTkLabel(self.frame_top, text="Código", 
                     font=("Cascadia Code", 12.5)
                     ).place(x=5, y=5)
        self.cod_entry = ctk.CTkEntry(self.frame_top, 
                                      width=45, 
                                      justify=CENTER, 
                                      font=("Cascadia Code", 13, "bold"), text_color="#A9A9A9", 
                                      fg_color="transparent")
        self.cod_entry.place(x=5, y=30)

        ctk.CTkLabel(self.frame_top, text="Descrição do Produto", 
                     font=("Cascadia Code", 13)
                     ).place(x=55, y=5)
        ctk.CTkLabel(self.frame_top, text="(obrigatório)", 
                     font=("Cascadia Code", 10, "italic"), text_color="#FF4500"
                     ).place(x=220, y=5)
        self.produto_entry = ctk.CTkEntry(self.frame_top, 
                                          width=350, 
                                          font=("Cascadia Code", 13), 
                                          fg_color="transparent")
        self.produto_entry.place(x=55, y=30)

        lista = self.dql_database("SELECT grupo FROM estoque", column_names=True)
        ctk.CTkLabel(self.frame_top, text="Departamento", 
                     font=("Cascadia Code", 13)
                     ).place(x=410, y=5)
        self.grupo_listBox = ctk.CTkComboBox(self.frame_top, 
                                             width=200, 
                                             values=lista, 
                                             font=("Cascadia Code", 13))
        self.grupo_listBox.set("")
        self.grupo_listBox.place(x=410, y=30)
        
        lista = self.dql_database("SELECT medida FROM estoque", column_names=True)
        ctk.CTkLabel(self.frame_top, text="Medida", 
                     font=("Cascadia Code", 13)
                     ).place(x=610, y=5)
        self.medida_listBox = ctk.CTkComboBox(self.frame_top, 
                                              width=115, 
                                              values=lista, 
                                              font=("Cascadia Code", 13), 
                                              justify=CENTER)
        self.medida_listBox.set("")
        self.medida_listBox.place(x=615, y=30)

        lista = self.dql_database("SELECT fornecedor FROM estoque", column_names=True)
        ctk.CTkLabel(self.frame_top, text="Fornecedor", 
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=60)
        self.fornecedor_listBox = ctk.CTkComboBox(self.frame_top, 
                                                  width=200, 
                                                  values=lista, 
                                                  font=("Cascadia Code", 13))
        self.fornecedor_listBox.set("")
        self.fornecedor_listBox.place(x=5, y=85)
        
        ctk.CTkLabel(self.frame_top, text="Nº Lote", 
                     font=("Cascadia Code", 13)
                     ).place(x=295, y=60)
        self.lote_entry = ctk.CTkEntry(self.frame_top, 
                                       width=65, 
                                       justify=CENTER,
                                       font=("Cascadia Code", 13), 
                                       fg_color="transparent")
        self.lote_entry.place(x=295, y=85)
        
        self.check_var = ctk.StringVar(value="on")
        self.ativo_checkbox = ctk.CTkCheckBox(self.frame_top, text="LOTE ATIVO", 
                                         checkbox_width=20, checkbox_height=20,
                                         font=("Cascadia Code", 12, "bold"),
                                         corner_radius=15,
                                         command=None, 
                                         variable=self.check_var, 
                                         onvalue="on", offvalue="off")
        self.ativo_checkbox.place(x=365, y=85)
        
        ctk.CTkLabel(self.frame_top, text="Responsável",
                     font=("Cascadia Code", 13)
                     ).place(x=5, y=115)
        self.resp_entry = ctk.CTkEntry(self.frame_top,
                                       width=150,
                                       font=("Cascadia Code", 13),
                                       fg_color="transparent")
        self.resp_entry.place(x=5, y=140)

        ctk.CTkLabel(self.frame_top, text="Fone", 
                     font=("Cascadia Code", 13)
                     ).place(x=165, y=115)
        self.fone_entry = ctk.CTkEntry(self.frame_top, 
                                       width=140, 
                                       font=("Cascadia Code", 13), 
                                       fg_color="transparent")
        self.fone_entry.place(x=165, y=140)

        ctk.CTkLabel(self.frame_top, text="Nota Fiscal", 
                     font=("Cascadia Code", 13)
                     ).place(x=320, y=115)
        self.nf_entry = ctk.CTkEntry(self.frame_top, 
                                     width=140, 
                                     justify=CENTER,
                                     font=("Cascadia Code", 13), fg_color="transparent")
        self.nf_entry.place(x=320, y=140)
        
        # SUB-FRAME ESTOQUE -------------------------------------------------------------------------------------------
        self.sub_frame = atk.Frame3d(self.frame_top, width=285, height=130)
        self.sub_frame.place(x=475, y=65)
        
        ctk.CTkLabel(self.sub_frame, text="Qtd.Entrada", 
                     font=("Cascadia Code", 13), 
                     fg_color="#363636"
                     ).place(x=15, y=5)
        self.estoque_entry = ctk.CTkEntry(self.sub_frame, 
                                          width=100, 
                                          justify=CENTER,
                                          font=("Cascadia Code", 13),  
                                          fg_color="#363636", bg_color="#363636")
        self.estoque_entry.place(x=15, y=30)
        
        ctk.CTkLabel(self.sub_frame, text="Estoque Mín.", 
                     font=("Cascadia Code", 13), 
                     fg_color="#363636"
                     ).place(x=165, y=5)
        self.min_entry = ctk.CTkEntry(self.sub_frame, 
                                      width=100, 
                                      justify=CENTER,
                                      font=("Cascadia Code", 13), 
                                      fg_color="#363636", bg_color="#363636")
        self.min_entry.place(x=165, y=30)
        
        ctk.CTkLabel(self.sub_frame, text="VALOR DE ENTRADA",
                     font=("Cascadia Code", 12, "bold"), 
                     fg_color="#363636"
                     ).place(x=15, y=60)
        self.custo_entry = ctk.CTkEntry(self.sub_frame,
                                        width=100, 
                                        justify=CENTER,
                                        placeholder_text="R$ custos",
                                        font=("Cascadia Code", 13), 
                                        fg_color="#363636", bg_color="#363636")
        self.custo_entry.place(x=15, y=85)
        
        ctk.CTkLabel(self.sub_frame, text="VALOR DE SAÍDA", 
                     font=("Cascadia Code", 12, "bold"), 
                     fg_color="#363636").place(x=165, y=60)
        self.revenda_entry = ctk.CTkEntry(self.sub_frame, 
                                          width=100, 
                                          justify=CENTER,
                                          placeholder_text="R$ revenda",
                                          font=("Cascadia Code", 13), 
                                          fg_color="#363636", bg_color="#363636")
        self.revenda_entry.place(x=165, y=85)
        #--------------------------------------------------------------------------------------------------------------
        
        ctk.CTkLabel(self.frame_top, text="Duplo CLICK para selecionar um produto!",
                     font=("Cascadia Code", 12, "bold")
                     ).place(x=10, y=179)
        
        # CÓDIGO DE BARRAS --------------------------------------------------------------------------------------------
        self.num_barcode = ctk.CTkEntry(self.frame_top, 
                                        width=220, height=20, 
                                        justify=CENTER, 
                                        placeholder_text="Código de Barras", 
                                        font=("Cascadia Code", 13, "bold"), 
                                        corner_radius=3)
        self.num_barcode.bind("<Key>", lambda e: self.entry_off(e))
        self.num_barcode.place(x=765, y=160)
        
        self.img_barcode = ctk.CTkLabel(self.frame_top, text="", 
                                        width=222, height=125)
        self.img_barcode.place(x=765, y=30)

        btn_generate_code = ctk.CTkButton(self.frame_top, text="",
                                          width=20,
                                          image=self.image_button("add_barcode.png", (27, 27)), 
                                          compound=LEFT, anchor=NW,
                                          fg_color="transparent", 
                                          hover_color=("#D3D3D3", "#363636"), 
                                          command=self.add_barcode)
        btn_generate_code.place(x=943, y=119)
        atk.tooltip(btn_generate_code, "Gerar Código de Barras")

    def widgets_bottom(self): 
        self.frame_bottom = ctk.CTkFrame(self.root, 
                                         width=990, height=308,
                                         fg_color="#363636")
        self.frame_bottom.place(y=245)

        ctk.CTkLabel(self.frame_bottom, text="Data", 
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=15, y=275)
        self.data_registro = DateEntry(self.frame_bottom)
        self.data_registro.place(x=60, y=280)

        # TREEVIEW ------------------------------------------------------------------------
        self.lista_produtos = ttk.Treeview(self.frame_bottom, height=3, column=(
            'id', 'data_entrada', 'produto', 'medida', 'grupo', 'fornecedor', 'lote', 
            'estoque', 'estoque_mín', 'nf', 'status', 'responsável', 'fone', 'custo', 
            'revenda', 'barcode', 'ativo'
        ))
        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("id", text="Cód.")
        self.lista_produtos.heading("data_entrada", text="Últ.Registro")
        self.lista_produtos.heading("produto", text="Produto")
        self.lista_produtos.heading("medida", text="Medida")
        self.lista_produtos.heading("grupo", text="Departamento")
        self.lista_produtos.heading("fornecedor", text="Fornecedor")
        self.lista_produtos.heading("lote", text="Nº Lote")
        self.lista_produtos.heading("estoque", text="Estoque")
        self.lista_produtos.heading("estoque_mín", text="Etq.Mín.")
        self.lista_produtos.heading("nf", text="NF")
        self.lista_produtos.heading("status", text="Status")

        self.lista_produtos.heading("responsável", text="")
        self.lista_produtos.heading("fone", text="")
        self.lista_produtos.heading("custo", text="")
        self.lista_produtos.heading("revenda", text="")
        self.lista_produtos.heading("barcode", text="")
        self.lista_produtos.heading("ativo", text="")

        self.lista_produtos.column("#0", width=0, stretch=False)
        self.lista_produtos.column("id", width=35, anchor=CENTER)
        self.lista_produtos.column("data_entrada", width=75, anchor=CENTER)
        self.lista_produtos.column("produto", width=270)
        self.lista_produtos.column("medida", width=85, anchor=CENTER)
        self.lista_produtos.column("grupo", width=125)
        self.lista_produtos.column("fornecedor", width=150)
        self.lista_produtos.column("lote", width=50, anchor=CENTER)
        self.lista_produtos.column("estoque", width=50, anchor=CENTER)
        self.lista_produtos.column("estoque_mín", width=50, anchor=CENTER)
        self.lista_produtos.column("nf", width=85, anchor=CENTER)
        self.lista_produtos.column("status", width=70, anchor=CENTER)

        self.lista_produtos.column("responsável", width=0, stretch=False)
        self.lista_produtos.column("fone", width=0, stretch=False)
        self.lista_produtos.column("custo", width=0, stretch=False)
        self.lista_produtos.column("revenda", width=0, stretch=False)
        self.lista_produtos.column("barcode", width=0, stretch=False)
        self.lista_produtos.column("ativo", width=0, stretch=False)

        self.lista_produtos.place(width=970, height=255)
        # ----------------------------------------------------------------------------------

        scrollbar_y = ttk.Scrollbar(self.frame_bottom, 
                                    orient="vertical", 
                                    command=self.lista_produtos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_bottom, 
                                    orient="horizontal", 
                                    command=self.lista_produtos.xview)
        self.lista_produtos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=0, width=20, height=255)
        scrollbar_x.place(x=0, y=254, width=990, height=20)

        self.lista_produtos.bind("<Double-1>", self.on_doubleClick)
        
        self.select_database()
    
    def total_registries(self):
        total_registros = len(self.lista_produtos.get_children())
        ctk.CTkLabel(self.frame_bottom, 
                     width=200, 
                     text=f"Total de Registros: {total_registros}", 
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=750, y=279)

from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
from sqlite3 import Error

from con_database import *


class Register:
    
    def variables(self):
        self.produto = self.produto_entry.get()
        self.medida = self.medida_entry.get()
        self.grupo = self.grupo_entry.get()
        self.min = self.min_entry.get()
        self.fornecedor = self.fornecedor_entry.get()
        self.resp = self.responsavel_entry.get()
        self.fone1 = self.fone1_entry.get()
        self.fone2 = self.fone2_entry.get()
        self.nf = self.nf_entry.get()
    
    
    def clear_entries(self):
        self.produto_entry.delete(0, END)
        self.medida_entry.delete(0, END)
        self.grupo_entry.delete(0, END)
        self.min_entry.delete(0, END)
        self.fornecedor_entry.delete(0, END)
        self.responsavel_entry.delete(0, END)
        self.fone1_entry.delete(0, END)
        self.fone2_entry.delete(0, END)
        self.nf_entry.delete(0, END)
    
    
    def register_product(self):
        self.variables()
        
        if self.produto_entry.get() == "":
            messagebox.showinfo("Aviso", message="Insira a descrição do produto!")
        
        else:
            try:
                query_sql = """
                    INSERT INTO estoque (produto, medida, grupo, est_mín, fornecedor, responsável, fone_1, fone_2, NF)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """
                lista_dados = [self.produto, self.medida, self.grupo, self.min, self.fornecedor, self.resp, self.fone1, self.fone2, self.nf]
                
                dml_database(query_sql, lista_dados)
            
            except Error as e:
                messagebox.showerror(f"{e}", message="Não foi possível realizar o registro!")
            else:
                self.clear_entries()


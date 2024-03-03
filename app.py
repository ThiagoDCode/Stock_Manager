from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from TAB_resumos import TabResumos
from TAB_estoque import TabEstoque
from TAB_entradas import TabEntradas
from TAB_saidas import TabSaidas
from con_database import *


class Application:
    def __init__(self):
        self.root = ctk.CTk()

        self.layout_config()
        #self.menu_bar()
        self.tabs_application()

        self.root.mainloop()

    def layout_config(self):
        self.root.title("Controle de Estoque")
        self.root.geometry("1000x630")
        self.root.resizable(False, False)

    def menu_bar(self):  
        menu_bar = Menu(self.root)
        self.root.configure(menu=menu_bar)
        edite = Menu(menu_bar)
        
        menu_bar.add_cascade(label="Edite", menu=edite)
        edite.add_command(label="Configurações", command=WindowConfig)
    
    def tabs_application(self):
        self.tabs_view = ctk.CTkTabview(self.root, 
                                        width=1000, height=600, 
                                        anchor="w", 
                                        text_color=('#000', '#FFF'))
        self.tabs_view.pack()

        self.tabs_view.add("Resumos")
        TabResumos(self.tabs_view.tab("Resumos"))

        self.tabs_view.add("Produtos e Estoque")
        TabEstoque(self.tabs_view.tab("Produtos e Estoque"))

        self.tabs_view.add("Entradas")
        TabEntradas(self.tabs_view.tab("Entradas"))
        
        self.tabs_view.add("Saídas")
        TabSaidas(self.tabs_view.tab("Saídas"))

        self.tabs_view.set("Saídas",)


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

        ctk.CTkLabel(self, text="Tema", 
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=50, y=50)
        ctk.CTkOptionMenu(self, width=90, height=20, 
                          values=['System', 'Light', 'Dark'], 
                          font=("Cascadia Code", 15), 
                          command=ctk.set_appearance_mode
                          ).place(x=50, y=100)
    
    def confirm_config(self):
        ctk.CTkButton(self, text="APLICAR",
                      width=75, 
                      font=("Cascadia Code", 15, "bold"),
                      command=None
                      ).place(x=100, y=360)
        ctk.CTkButton(self, text="CANCELAR",
                      width=75, 
                      font=("Cascadia Code", 15, "bold"),
                      command=self.destroy
                      ).place(x=185, y=360)


if __name__ == "__main__":
    create_table()
    Application()

from tkinter import *
from tkinter import ttk
import customtkinter as ctk


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
        
        ctk.CTkLabel(self.root, text="Tema", font=("Cascadia Code", 15)).place(x=860, y=571)
        ctk.CTkOptionMenu(self.root, width=90, height=20, values=['System', 'Light', 'Dark'], font=("Cascadia Code", 15),
                        command=ctk.set_appearance_mode).place(x=900, y=575)
    
    
    def tabs_application(self):
        self.tabs_view = ctk.CTkTabview(self.root, width=1000, height=570, anchor="w", text_color=('#000', '#FFF'))
        self.tabs_view.pack()
        
        self.tabs_view.add("Resumos")
        
        self.tabs_view.add("Produtos e Estoque")
        
        self.tabs_view.add("Movimento de Produtos")
        
        self.tabs_view.set("Produtos e Estoque")


if __name__ == "__main__":
    Application()

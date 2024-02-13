from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from barcode import EAN13
from barcode.writer import ImageWriter
from random import randint


class Functions:

    def image_button(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/image/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/image/" + nameImage),
                           size=(scale))
        return img
    
    def image_barcode(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/barCodes/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/barCodes/" + nameImage),
                           size=(scale))
        return img

    def generate_barCode(self, id_product):
        if id_product == "":
            messagebox.showinfo("Please select", message="Por favor, informe o lote do produto!")
        else:
            if messagebox.askyesno("Generate Barcode", message=f"Gerar o código de barras para o lote: {id_product}"):
                try:
                    numbers = ""
                    for i in range(12):
                        numbers += str(randint(1, 9))
                    
                    code = EAN13(numbers, writer=ImageWriter())
                    code.save(f"./Stock_Manager/barCodes/{id_product}")
                    
                    messagebox.showinfo("Success", message="Código de barras gerado com sucesso!")
                    
                    return numbers
                except FileNotFoundError:
                    messagebox.showerror("Invalid", message="Lote inválido!")
                    
    def entry_off(self, event):
        if (event.state==12 and event.keysym== "c"):
            return
        else:
            return "break"

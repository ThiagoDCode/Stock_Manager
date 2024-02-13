from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from barcode import EAN13
from barcode.writer import ImageWriter
from random import randint


class Functions:

    def image_button(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/image/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/image/" + nameImage),
                           size=(scale))
        return img
    
    def code_image(nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/barCodes/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/barCodes/" + nameImage),
                           size=(scale))
        return img

    def generate_barCode(self, id_product):
        if id_product == "":
            messagebox.showinfo("Please select", message="Por favor, informe o lote do produto!")
        else:
            if messagebox.askyesno("Generate Barcode", message=f"Gerar o código de barras para o lote: {id_product}"):
                numbers = ""
                for i in range(12):
                    numbers += str(randint(1, 9))
                
                code = EAN13(numbers, writer=ImageWriter())
                code.save(f"./Stock_Manager/barCodes/{id_product}")
                
                messagebox.showinfo("Success", message="Código de barras gerado com sucesso!")
                
                return numbers


if __name__ == "__main__":
    
    app = Tk()
    app.geometry("300x300")
    
    def imprimir():
        print(code)
    
    code = ctk.CTkButton(app, text="code", command=lambda: Functions().generate_barCode(565)).pack()
    ctk.CTkButton(app, text="imprimir", command=imprimir).pack()
    
    app.mainloop()

    
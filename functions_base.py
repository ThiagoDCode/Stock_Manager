import customtkinter as ctk
from PIL import Image
from tkcalendar import DateEntry


class Functions:

    def image_button(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/image/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/image/" + nameImage),
                           size=(scale))

        return img

    def management(self, root):
        ctk.CTkLabel(root, text="Gestor", font=("Cascadia Code", 15, "bold")).place(x=10, y=570)
        self.gestor_entry = ctk.CTkEntry(self.root, width=225, font=("Cascadia Code", 15))
        self.gestor_entry.place(x=70, y=570)
        
        ctk.CTkLabel(root, text="Data", font=("Cascadia Code", 15, "bold"), anchor="nw").place(x=310, y=575)
        self.data_register = DateEntry(self.root)
        self.data_register.place(x=352, y=575)

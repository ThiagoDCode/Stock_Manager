import customtkinter as ctk
from PIL import Image


class Functions:

    def image_button(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/image/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/image/" + nameImage),
                           size=(scale))

        return img

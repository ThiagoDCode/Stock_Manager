import customtkinter as ctk
from PIL import Image

from con_database import *


class Functions(Database):
    
    def select_database2(self, query_sql):
        self.lista_produtos.delete(*self.lista_produtos.get_children())
        
        data_return = Database().dql_database(query_sql)
        
        for dado in data_return:
            self.lista_produtos.insert("", "end", values=dado)

    def image_button(self, nameImage, scale=tuple):
        img = ctk.CTkImage(light_image=Image.open("./Stock_Manager/image/" + nameImage),
                           dark_image=Image.open("./Stock_Manager/image/" + nameImage),
                           size=(scale))

        return img

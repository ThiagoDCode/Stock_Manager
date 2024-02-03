from PIL import Image, ImageTk


class Functions:
    
    def image_button(self, nameImage, scale=tuple):
        img = Image.open("./Stock_Manager/image/" + nameImage)
        img = img.resize(scale)
        img = ImageTk.PhotoImage(img)
        
        return img

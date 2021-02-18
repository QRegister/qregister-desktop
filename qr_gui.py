from tkinter import *

import pyqrcode
from PIL import ImageTk

window = Tk()
window.title("Test")
window.geometry("600x600")


def generate():
    qr = pyqrcode.create("test")
    photo = BitmapImage(data=qr.xbm(scale=16))
    qr_image.config(image=photo)
    qr_image.photo = photo


button = Button(window, text="Show", command=generate)
button.grid(row=0, column=0, padx=3, pady=3)

qr_image = Label(window)
qr_image.grid(row=4, column=1, padx=3, pady=3)
window.mainloop()

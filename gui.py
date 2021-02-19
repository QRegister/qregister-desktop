from tkinter import *

import pyqrcode

window = Tk()
window.attributes('-fullscreen', True)
window.title("Test")
#window.geometry("600x600")
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)


def close():
    window.destroy()


def generate():
    qr = pyqrcode.create("test")
    photo = BitmapImage(data=qr.xbm(scale=12))
    qr_image.config(image=photo)
    qr_image.photo = photo


button = Button(window, text="Show", width=4, height=4, command=generate)
button.grid(row=0, column=0, padx=3, pady=3)

button = Button(window, text="Exit", width=4, height=4, command=close)
button.grid(row=0, column=4, padx=3, pady=3)

qr_image = Label(window)
qr_image.grid(row=1, column=3, padx=0, pady=0)
window.mainloop()

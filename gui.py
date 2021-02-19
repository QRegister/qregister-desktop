import pyqrcode
import tkinter as tk

from firebase_setup import send_data, firebase_init
from read_inventory import generate_receipt

db = firebase_init()

window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("Test")
# window.geometry("600x600")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)


def close():
    window.destroy()


def generate():
    doc = 'receipt-2'

    product_list, total_price = generate_receipt()

    send_firebase(document_name=doc, product_list=product_list, total_price=total_price)

    price_text.config(state=tk.NORMAL)
    price_text.replace('1.0', tk.END, f"Total: ${total_price}", "tag-center")
    price_text.config(state=tk.DISABLED)

    qr = pyqrcode.create(doc)
    photo = tk.BitmapImage(data=qr.xbm(scale=12))
    qr_image.config(image=photo)
    qr_image.photo = photo


def send_firebase(document_name: str, product_list: list, total_price: float):
    send_data(
        db=db,
        collection_name='market',
        document_name=document_name,
        cashier_name='Deniz',
        market_name='ŞOK ODTÜ',
        market_address='ODTÜ',
        total_price=total_price,
        product_list=product_list
    )


button_generate = tk.Button(window, text="Show", width=6, height=4, command=generate)
button_generate.grid(row=0, column=0, padx=5, pady=5)

button_exit = tk.Button(window, text="Exit", width=6, height=4, command=close)
button_exit.grid(row=0, column=4, padx=5, pady=5)

price_text = tk.Text(window, width=20, height=1, font=("Helvetica", 25))
price_text.tag_configure('tag-center', justify='center')
price_text.insert(tk.END, "Please scan QR", "tag-center")
price_text.config(state=tk.DISABLED)
price_text.grid(row=0, column=3, padx=3, pady=3)

qr_image = tk.Label(window)
qr_image.grid(row=1, column=3, padx=0, pady=0)

window.mainloop()

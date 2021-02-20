import pyqrcode
import tkinter as tk
import uuid
from firebase_setup import send_data, firebase_init, get_data
from helpers import generate_sample_receipt, generate_hash, convert_receipt_to_firebase

db = firebase_init()

window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("QReceipt")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)

brand_id = 'GwukmSESE5rrvQpEXa39'
store_id = 'YAUQCOP3vm6yDhtMON6k'


def close():
    window.destroy()


def activate_generate_button():
    button_generate['state'] = 'normal'


def generate_receipt():
    receipt_id = str(uuid.uuid4())[:18]

    receipt = generate_sample_receipt()
    qr_hash = generate_hash(receipt=receipt)
    qr_hash += receipt_id + '&'
    product_list, total_price, total_tax = convert_receipt_to_firebase(receipt=receipt)

    send_firebase(
        product_list=product_list,
        total_price=total_price,
        total_tax=total_tax,
        receipt_id=receipt_id
    )

    price_text.config(state=tk.NORMAL)
    price_text.replace('1.0', tk.END, f"Total: ${total_price}", "tag-center")
    price_text.config(state=tk.DISABLED)

    qr = pyqrcode.create(qr_hash)
    photo = tk.BitmapImage(data=qr.xbm(scale=11))
    qr_image.config(image=photo)
    qr_image.photo = photo

    button_generate['state'] = 'disabled'
    window.after(2000, activate_generate_button)


def send_firebase(product_list: list, total_price: float, total_tax: float, receipt_id: str):
    send_data(
        db=db,
        brand_id=brand_id,
        cashier_name='Deniz',
        product_list=product_list,
        receipt_id=receipt_id,
        store_id=store_id,
        total_price=total_price,
        total_tax=total_tax,
    )


# Tkinter GUI

button_generate = tk.Button(window, text="Show", width=6, height=4, command=generate_receipt)
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

import pyqrcode
import tkinter as tk
import uuid
from firebase_setup import send_data, firebase_init, get_data
from read_inventory import generate_receipt

db = firebase_init()

window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("QReceipt")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)


def close():
    window.destroy()


def generate():
    market_id = 'FSBN4CPaa4Jtntwc19dB'
    receipt_id = str(uuid.uuid4())[:18]

    product_list, total_price, total_tax = generate_receipt()
    send_firebase(
        product_list=product_list,
        total_price=total_price,
        total_tax=total_tax,
        market_id=market_id,
        receipt_id=receipt_id
    )

    print(total_price)

    price_text.config(state=tk.NORMAL)
    price_text.replace('1.0', tk.END, f"Total: ${total_price}", "tag-center")
    price_text.config(state=tk.DISABLED)

    qr = pyqrcode.create(receipt_id)
    photo = tk.BitmapImage(data=qr.xbm(scale=11))
    qr_image.config(image=photo)
    qr_image.photo = photo


def send_firebase(product_list: list, total_price: float, total_tax: float, market_id: str, receipt_id: str):
    market_name, market_address = get_data(db=db, market_id=market_id)

    send_data(
        db=db,
        market_id=market_id,
        receipt_id=receipt_id,
        cashier_name='Deniz',
        market_name=market_name,
        market_address=market_address,
        total_price=total_price,
        total_tax=total_tax,
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

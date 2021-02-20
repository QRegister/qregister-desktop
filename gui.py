import pyqrcode
import tkinter as tk
import uuid
from firebase_setup import send_data, firebase_init, get_data
from helpers import generate_sample_receipt, generate_hash, convert_receipt_to_firebase

# Firebase initialization
db = firebase_init()

# Tkinter initialization
window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("QReceipt")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)

# Brand id
brand_id = 'GwukmSESE5rrvQpEXa39'

# Store id
store_id = 'YAUQCOP3vm6yDhtMON6k'


def close():
    """
    Exit from app
    :return:
    """
    window.destroy()


def activate_generate_button():
    """
    Activate "Generate" button
    :return:
    """
    button_generate['state'] = 'normal'


def generate_qr() -> None:
    """
    Generate QR

    :return: None
    """

    # Random receipt id
    receipt_id = str(uuid.uuid4())[:18]

    # Generate sample receipt
    receipt = generate_sample_receipt()

    # Hash receipt data
    qr_secret = generate_hash(receipt=receipt)

    # Add receipt id to the hashed data
    qr_secret += receipt_id + '&'

    # Convert receipt data to list and calculate total price & total tax
    product_list, total_price, total_tax = convert_receipt_to_firebase(receipt=receipt)

    # Send all data to Firebase
    send_firebase(
        product_list=product_list,
        total_price=total_price,
        total_tax=total_tax,
        receipt_id=receipt_id,
        qr_secret=qr_secret,
    )

    # Update price text
    price_text.config(state=tk.NORMAL)
    price_text.replace('1.0', tk.END, f"Total: ${total_price}", "tag-center")
    price_text.config(state=tk.DISABLED)

    # QR generation
    qr = pyqrcode.create(qr_secret)
    photo = tk.BitmapImage(data=qr.xbm(scale=9))
    qr_image.config(image=photo)
    qr_image.photo = photo

    # Deactivate generation button for 2 seconds
    button_generate['state'] = 'disabled'
    window.after(2000, activate_generate_button)


def send_firebase(
        product_list: list,
        total_price: float,
        total_tax: float,
        receipt_id: str,
        qr_secret: str
) -> None:
    """
    Sending data to firebase

    :param product_list:
    :param total_price: Total price of the receipt
    :param total_tax: Total tax of the receipt
    :param receipt_id: Receipt id
    :param qr_secret: QR secret
    :return: None
    """

    send_data(
        db=db,
        brand_id=brand_id,
        cashier_name='Deniz',
        product_list=product_list,
        qr_secret=qr_secret,
        receipt_id=receipt_id,
        store_id=store_id,
        total_price=total_price,
        total_tax=total_tax,
    )


# Tkinter GUI

# Generate button
button_generate = tk.Button(window, text="Show", width=6, height=4, command=generate_qr)
button_generate.grid(row=0, column=0, padx=5, pady=5)

# Exit button
button_exit = tk.Button(window, text="Exit", width=6, height=4, command=close)
button_exit.grid(row=0, column=4, padx=5, pady=5)

# Price text
price_text = tk.Text(window, width=20, height=1, font=("Helvetica", 25))
price_text.tag_configure('tag-center', justify='center')
price_text.insert(tk.END, "Please scan QR", "tag-center")
price_text.config(state=tk.DISABLED)
price_text.grid(row=0, column=3, padx=3, pady=3)

# QR code
qr_image = tk.Label(window)
qr_image.grid(row=1, column=3, padx=0, pady=0)

window.mainloop()

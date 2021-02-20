import os
import random
import calendar
import time
import pyqrcode
import tkinter as tk
import uuid

from PIL import Image, ImageTk

from firebase_setup import send_data, firebase_init, get_data
from helpers import generate_sample_receipt, generate_hash, convert_receipt_to_firebase, convert_stores_to_list

# Firebase initialization
db = firebase_init()

# Tkinter initialization
window = tk.Tk()
window.attributes('-fullscreen', True)
window.title("QReceipt")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)


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

    cashier_name = 'Deniz'

    # Retrieve all stores
    all_stores = convert_stores_to_list()

    # Store id
    store = random.choice(all_stores)

    store_id = store['id']
    store_slag = store['slag']
    store_item_code = store['item-code']
    store_location_id = store['location-id']

    # Random receipt id
    receipt_id = str(uuid.uuid4())[:18]

    # Generate sample receipt
    receipt = generate_sample_receipt()

    # Add timestamp
    qr_secret = str(calendar.timegm(time.gmtime()))

    # Add store item code
    qr_secret += '-' + str(store_item_code)

    # Add cashier name
    qr_secret += '-' + cashier_name

    # Add products
    qr_secret += '-' + generate_hash(receipt=receipt)

    # Convert receipt data to list and calculate total price & total tax
    product_list, total_price, total_tax = convert_receipt_to_firebase(receipt=receipt)

    # Send all data to Firebase
    # send_firebase(
    #     cashier_name=cashier_name,
    #     product_list=product_list,
    #     qr_secret=qr_secret,
    #     receipt_id=receipt_id,
    #     store_id=store_id,
    #     store_location_id=store_location_id,
    #     total_price=total_price,
    #     total_tax=total_tax,
    # )

    # Update price text
    price_text.config(state=tk.NORMAL)
    price_text.replace('1.0', tk.END, f"Total: ${total_price}", "tag-center")
    price_text.config(state=tk.DISABLED)

    # QR generation
    qr = pyqrcode.create(qr_secret)
    photo = tk.BitmapImage(data=qr.xbm(scale=8))
    qr_image.config(image=photo)
    qr_image.photo = photo

    # Store logo
    root = os.getcwd()
    path = root + '/logos/' + store_slag + '.png'

    img = Image.open(path)
    img = img.resize((150, 150), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img)
    store_logo.config(image=photo)
    store_logo.image = photo

    # Deactivate generation button for 2 seconds
    button_generate['state'] = 'disabled'
    window.after(2000, activate_generate_button)


def send_firebase(
        cashier_name: str,
        product_list: list,
        qr_secret: str,
        receipt_id: str,
        store_id: str,
        store_location_id: str,
        total_price: float,
        total_tax: float,
) -> None:
    """
    Sending data to firebase

    :param cashier_name: Cashier name
    :param product_list:
    :param qr_secret: QR secret
    :param receipt_id: Receipt id
    :param store_id: Store id
    :param store_location_id: Store location id
    :param total_price: Total price of the receipt
    :param total_tax: Total tax of the receipt
    :return: None
    """

    send_data(
        db=db,
        cashier_name=cashier_name,
        product_list=product_list,
        qr_secret=qr_secret,
        receipt_id=receipt_id,
        store_id=store_id,
        store_location_id=store_location_id,
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

# Store logo
store_logo = tk.Label(window)
store_logo.place(x=50, y=150)

window.mainloop()

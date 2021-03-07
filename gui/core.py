import random
import time
import uuid
import pyqrcode
from kivy.app import App
from kivy.uix.widget import Widget
from firebase.setup import firebase_init, send_data, send_firebase
from helpers.core import convert_stores_to_list, currency_symbol, generate_sample_receipt, generate_hash, \
    convert_receipt_to_firebase

db = firebase_init()


class QRegisterLayout(Widget):
    def say_hello(self):
        self.ids.img_shop.source = "data/logos/a101.png"

    def generate_qr(self) -> None:
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
        store_slug = store['slug']
        store_item_code = store['item-code']
        store_location_id = store['location-id']
        store_currency = store['currency']

        # Getting correct currency symbol
        currency = currency_symbol(store_currency)

        # Random receipt id
        receipt_id = str(uuid.uuid4())[:18]

        # Generate sample receipt
        receipt = generate_sample_receipt()

        # Add timestamp
        qr_secret = str(int(time.time() * 1000))

        # Add store item code
        qr_secret += '#' + str(store_item_code)

        # Add cashier name
        qr_secret += '#' + cashier_name

        # Add receipt id
        qr_secret += '#' + receipt_id

        # Add products
        qr_secret += '#' + generate_hash(receipt=receipt)

        # Convert receipt data to list and calculate total price & total tax
        product_list, total_price, total_tax = convert_receipt_to_firebase(receipt=receipt)

        # Send all data to Firebase

        # Update price text

        self.ids.txt_price.text = f"Total: {currency}{total_price}"
        print(qr_secret)

        # QR generation
        qr = pyqrcode.create(qr_secret)
        qr.png('data/qr/qr_test.png', scale=10)
        self.ids.img_qr.source = 'data/qr/qr_test.png'
        self.ids.img_qr.reload()

        # Update Shop image
        self.ids.img_shop.source = 'data/logos/' + store_slug + '.png'

    pass


class QRegisterApp(App):
    def build(self):
        return QRegisterLayout()


def run():
    db = firebase_init()
    root = QRegisterApp()
    root.run()

import random
import os
import time
import uuid
import pyqrcode
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from firebase.setup import firebase_init, send_data, send_firebase, update
from core.helpers import convert_stores_to_list, currency_symbol, generate_sample_receipt, generate_hash, \
    convert_receipt_to_firebase, fill_inventory

db = firebase_init()


class QRegisterLayout(Widget):

    def change_source(self, dt) -> None:
        """
        Change source of show button to normal

        :param dt: not used
        :return: None
        """
        self.ids.img_show.source = 'data/ui/btn_show.png'

        # Run generate_qr()
        Clock.schedule_once(self.generate_qr, 0.3)

    def disable_button(self, name) -> None:
        """
        Disable given button

        :param name: button id name
        :return: None
        """
        if name == 'show':
            self.ids.img_show.source = 'data/ui/btn_show_clicked.png'
            self.ids.btn_show.disabled = True

            Clock.schedule_once(self.change_source, 0.5)

        if name == 'exit':
            self.ids.img_exit.source = 'data/ui/btn_exit_clicked.png'
            self.ids.btn_exit.disabled = True

            Clock.schedule_once(self.exit_from_app, 0.3)

    def enable_button(self, dt) -> None:
        """
        Activate show button

        :param dt: not used
        :return: None
        """

        self.ids.btn_show.disabled = False

    @staticmethod
    def exit_from_app(dt) -> None:
        """
        Exit from app

        :param dt: not used
        :return:
        """
        os.remove('data/qr/qr_test.png')
        App.get_running_app().stop()

    def generate_qr(self, dt) -> None:
        """
        Generate QR

        :param dt: not used
        :return: None
        """

        # Random cashier
        cashier_name = random.choice(['Deniz', 'Murat', 'Alkim', 'Humeyra'])

        # Retrieve all stores
        all_stores = convert_stores_to_list()

        # Store id
        store = random.choice(all_stores)

        store_id = store['id']
        store_slug = store['slug']
        store_code = store['store-code']
        store_location_id = store['location-id']
        store_currency = store['currency']

        # Getting correct currency symbol
        currency = currency_symbol(store_currency)

        # Random receipt id
        receipt_id = str(uuid.uuid4())[:18]

        # Generate sample receipt
        receipt = generate_sample_receipt()
        if not receipt:
            receipt = generate_sample_receipt()
        # Add timestamp
        qr_secret = str(int(time.time() * 1000))

        # Add store item code
        qr_secret += '#' + str(store_code)

        # Add cashier name
        qr_secret += '#' + cashier_name

        # Add receipt id
        qr_secret += '#' + receipt_id

        # Add products
        qr_secret += '#' + generate_hash(receipt=receipt)

        # Convert receipt data to list and calculate total price & total tax
        product_list, total_price, total_tax = convert_receipt_to_firebase(receipt=receipt)

        # Firebase init
        db = firebase_init()

        # Send all data to Firebase
        send_firebase(
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

        # Update price text
        self.ids.txt_price.text = f"Total: {currency} {total_price}"
        print(qr_secret)

        # QR generation
        qr = pyqrcode.create(qr_secret)
        qr.png('data/qr/qr_test.png', scale=10)
        self.ids.img_qr.source = 'data/qr/qr_test.png'
        self.ids.img_qr.reload()

        # Update Shop image
        self.ids.img_shop.source = 'data/logos/' + store_slug + '.png'

        # Enable button after 2 seconds
        Clock.schedule_once(self.enable_button, 2)

    pass


class QRegisterApp(App):
    def build(self):
        return QRegisterLayout()


class QRegisterRaspberryApp(App):
    def build(self):
        return QRegisterLayout()


def run(update_store: bool, is_raspberry_pi: bool, is_full_screen: bool, inventory: bool, not_execute: bool) -> None:
    """
    Running QRegister App

    :param update_store: Update Store data on Firebase
    :param is_raspberry_pi: Is app running on Raspberry Pi?
    :param is_full_screen: Is it full screen?
    :param inventory: Fill inventory
    :param not_execute: Do not run the app
    :return: None
    """
    Window.fullscreen = is_full_screen

    if update_store:
        update(db=db, stores=convert_stores_to_list())
    if inventory:
        fill_inventory()
    if is_raspberry_pi:
        root = QRegisterRaspberryApp()
    else:
        root = QRegisterApp()

    if not not_execute:
        root.run()

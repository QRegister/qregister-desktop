import datetime

import firebase_admin

from firebase_admin import firestore
from firebase_admin import credentials


def firebase_init():
    """
    Firebase Initialization

    :return: Firestore Client
    """
    try:
        firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


def get_data(db, brand_id: str, store_id: str) -> (str, str, str):
    """
    Getting store data from Firestore

    :param db:
    :param brand_id:
    :param store_id:
    :return:
    """
    brand_ref = db.collection('stores').document(brand_id)
    brand_detail = brand_ref.get().to_dict()
    brand = brand_detail['name']

    store_ref = brand_ref.collection('store-locations').document(store_id)
    store_detail = store_ref.get().to_dict()

    store_name = store_detail['name']
    store_address = store_detail['address']

    return brand, store_name, store_address


def send_data(
        db,
        brand_id: str,
        cashier_name: str,
        product_list: list,
        qr_secret: str,
        receipt_id: str,
        store_id: str,
        total_price: float,
        total_tax: float,
):
    """
    Sending data to Firestore

    :param db: Firestore client
    :param brand_id: Unique brand id
    :param cashier_name: Cashier Name
    :param product_list: Product list
    :param qr_secret: Hashed QR code
    :param receipt_id: Unique receipt id
    :param store_id: Unique brand id
    :param total_price: Total price of the receipt
    :param total_tax: Total tax of the receipt
    :return:
    """

    brand, store_name, store_address = get_data(db=db, brand_id=brand_id, store_id=store_id)

    # Store Reference
    store_ref = db.collection('stores').document(brand_id).collection('store-locations').document(store_id)

    # Receipt reference
    receipt_ref = store_ref.collection('receipts').document(receipt_id)

    data = {
        'brand': brand,
        'cashier-name': cashier_name,
        'date': datetime.datetime.now(),
        'store-location': store_name,
        'store-address': store_address,
        'products': product_list,
        'qr-secret': qr_secret,
        'total-price': total_price,
        'total-tax': total_tax,
    }
    print(data)
    receipt_ref.set(data)

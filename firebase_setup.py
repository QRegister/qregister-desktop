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


def get_data(db, store_id: str, store_location_id: str) -> (str, str, str):
    """
    Getting store data from Firestore

    :param db:
    :param store_location_id:
    :param store_id:
    :return:
    """
    store_ref = db.collection('stores').document(store_id)
    store_detail = store_ref.get().to_dict()

    store_name = store_detail['name']
    store_slug = store_detail['verbose']

    store_location_ref = store_ref.collection('store-locations').document(store_location_id)
    store_location_detail = store_location_ref.get().to_dict()

    store_location = store_location_detail['name']
    store_location_address = store_location_detail['address']

    return store_name, store_slug, store_location, store_location_address


def send_data(
        db,
        store_id: str,
        cashier_name: str,
        product_list: list,
        qr_secret: str,
        receipt_id: str,
        store_location_id: str,
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

    store_name, store_slug, store_location, store_location_address = get_data(db=db, store_id=store_id,
                                                                              store_location_id=store_location_id)

    # Store Reference
    store_ref = db.collection('stores').document(store_id).collection('store-locations').document(store_location_id)

    # Receipt reference
    receipt_ref = store_ref.collection('receipts').document(receipt_id)

    data = {
        'cashier-name': cashier_name,
        'date': datetime.datetime.now(),
        'store-location-address': store_location_address,
        'store-location': store_location,
        'store-name': store_name,
        'store-slug': store_slug,
        'products': product_list,
        'qr-secret': qr_secret,
        'total-price': total_price,
        'total-tax': total_tax,
    }
    print(data)

    receipt_ref.set(data)

    receipt_ref = db.collection('receipts').document(receipt_id)
    receipt_ref.set(data)

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


def update_stores(db, stores: list):
    """
    Updating all stores

    :param db: Firestore Client
    :param stores: All stores
    :return:
    """
    for store in stores:
        send_store(db, store)
    print("Stores updated")


def send_store(db, store: dict):
    """
    Sending store data to Firestore

    :param db: Firestore Client
    :param store: Store dict
    :return:
    """
    print(store['id'])
    store_ref = db.collection('stores').document(store['id'])

    store_ref.set({
        'name': store['name'],
        'slug': store['slug'],
    })

    store_location_ref = store_ref.collection('store-locations').document(store['location-id'])

    store_location_ref.set({
        'name': store['location'],
        'address': store['address'],
        'currency': store['currency'],
    })


def get_data(db, store_id: str, store_location_id: str) -> dict:
    """
    Getting store data from Firestore

    :param db: Firestore Client
    :param store_location_id: Store location id
    :param store_id: Store id
    :return: Store dict
    """
    store = {}

    store_ref = db.collection('stores').document(store_id)
    store_detail = store_ref.get().to_dict()

    store['name'] = store_detail['name']
    store['slug'] = store_detail['slug']

    store_location_ref = store_ref.collection('store-locations').document(store_location_id)
    store_location_detail = store_location_ref.get().to_dict()

    store['location'] = store_location_detail['name']
    store['address'] = store_location_detail['address']
    store['currency'] = store_location_detail['currency']

    return store


def send_data(db,
              cashier_name: str,
              product_list: list,
              qr_secret: str,
              receipt_id: str,
              store_id: str,
              store_location_id: str,
              total_price: float,
              total_tax: float,
              ):
    """
    Sending data to Firestore

    :param db: Firestore client
    :param cashier_name: Cashier Name
    :param product_list: Product list
    :param qr_secret: Hashed QR code
    :param receipt_id: Unique receipt id
    :param store_id: Unique brand id
    :param store_location_id: Unique store location id
    :param total_price: Total price of the receipt
    :param total_tax: Total tax of the receipt
    :return:
    """

    # Getting store details from Firebase
    store = get_data(db=db, store_id=store_id, store_location_id=store_location_id)

    # Store Reference
    store_ref = db.collection('stores').document(store_id).collection('store-locations').document(store_location_id)

    # Receipt reference
    receipt_ref = store_ref.collection('receipts').document(receipt_id)

    data = {
        'cashier-name': cashier_name,
        'currency': store['currency'],
        'date': datetime.datetime.now(),
        'store-location-address': store['address'],
        'store-location': store['location'],
        'store-name': store['name'],
        'store-slug': store['slug'],
        'products': product_list,
        'qr-secret': qr_secret,
        'total-price': total_price,
        'total-tax': total_tax,
    }
    print(data)

    receipt_ref.set(data)

    receipt_ref = db.collection('receipts').document(receipt_id)
    receipt_ref.set(data)

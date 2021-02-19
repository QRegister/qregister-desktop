import datetime

import firebase_admin

from firebase_admin import firestore
from firebase_admin import credentials


def firebase_init():
    try:
        app = firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def send_data(
        db,
        collection_name: str,
        document_name: str,
        cashier_name: str,
        market_name: str,
        market_address: str,
        total_price: float,
        product_list: list,
):
    ref = db.collection(collection_name).document(document_name)

    data = {
        'date': datetime.datetime.now(),
        'cashier-name': cashier_name,
        'market': market_name,
        'market-address': market_address,
        'total-price': total_price,
        'products': product_list,
    }

    ref.set(data)

# db = firebase_cred()
# send_data(db=db, collection_name='test', document_name='receipt-2')

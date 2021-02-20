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


def get_data(db, market_id):
    ref = db.collection('markets').document(market_id)

    market_detail = ref.get().to_dict()

    market_name = market_detail['name']
    market_address = market_detail['address']

    return market_name, market_address


def send_data(
        db,
        receipt_id: str,
        market_id: str,
        cashier_name: str,
        market_name: str,
        market_address: str,
        total_price: float,
        product_list: list,
):
    ref = db.collection('markets').document(market_id).collection('receipts').document(receipt_id)

    data = {
        'date': datetime.datetime.now(),
        'cashier-name': cashier_name,
        'market': market_name,
        'market-address': market_address,
        'total-price': total_price,
        'products': product_list,
    }
    print(data)
    ref.set(data)

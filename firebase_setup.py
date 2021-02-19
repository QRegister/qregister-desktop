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


def send_data(db, collection_name: str, document_name: str):
    ref = db.collection(collection_name).document(document_name)

    ref.set({
        'date': datetime.datetime.now(),
        'cashier-name': 'Ahmet',
        'qr-secret': 'lorem',
        'products': {
            'product-01': {
                'price': 10,
                'name': 'Örnek Ürün 1',
                'count': 1
            },
            'product-02': {
                'price': 15,
                'name': 'Örnek Ürün 2',
                'count': 2
            },
            'product-03': {
                'price': 25,
                'name': 'Örnek Ürün 2',
                'count': 2
            },
        },
    })


#db = firebase_cred()
#send_data(db=db, collection_name='test', document_name='receipt-2')

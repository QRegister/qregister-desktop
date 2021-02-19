import datetime

import firebase_admin

from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection('test')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

doc_ref = db.collection('test').document('receipt-1')

doc_ref.set({
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
    },
})

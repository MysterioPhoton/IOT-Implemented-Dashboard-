import firebase_admin
from firebase_admin import credentials, firestore

# cred = credentials.Certificate("esp32-addtofs/key.json")
cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client(app=None)

def addToFirestore(temperature, time, doc_name=None):
    coll_ref = store.collection("temperature")

    if doc_name:
        coll_ref.document(doc_name).set({
            "value": temperature,
            "createdAt": time
        })
    else:
        coll_ref.add({
            "value": temperature,
            "createdAt": time
        })

def getFromFirestore():
    collections_ref = store.collection("temperature")
    docrefs = collections_ref.get()
    data = []
    for docref in docrefs:
        doc = docref.to_dict()
        data.append({
            'id': docref.id,
            'value': doc['value'],
            'createdAt': doc['createdAt']
        })
    return data

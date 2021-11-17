#  Copyright (c)  Ong Wi Yi .

import firebase_admin
from firebase_admin import credentials, firestore


def setup_firebase():
    cred = credentials.Certificate("igclientmgmt-firebase-adminsdk-2omdp-c34bf66a95.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
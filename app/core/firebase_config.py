import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    if not firebase_admin._apps:
        firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
        if firebase_credentials:
            cert_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
        else:
            try:
                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print("Aviso: Firebase não foi inicializado corretamente. Configure FIREBASE_CREDENTIALS.")

def get_db():
    try:
        return firestore.client()
    except ValueError:
        init_firebase()
        return firestore.client()

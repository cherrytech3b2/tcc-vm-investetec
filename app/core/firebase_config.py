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
                raise RuntimeError(f"Erro ao inicializar Firebase: Configure a variável FIREBASE_CREDENTIALS ou crie o arquivo serviceAccountKey.json. Detalhes: {str(e)}")

def get_db():
    try:
        firebase_admin.get_app()
    except ValueError:
        init_firebase()
    return firestore.client()

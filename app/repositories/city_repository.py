import firebase_admin
from firebase_admin import firestore
from app.models.city import city

class CityRepository:
    def get_all_cities(self) -> list[City]:
        db = firestore.client()
        
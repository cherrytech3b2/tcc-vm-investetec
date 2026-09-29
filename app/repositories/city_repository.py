import firebase_admin
from firebase_admin import firestore
from app.models.city import city

class CityRepository:
    def get_all_cities(self) -> list[City]:
        db = firestore.client()
        docs = db.collection('cities').stream()
        cities = []
        for doc in docs:
            data = doc.to_dist()
            cities.append(City(id=doc.id,
                                state=data.get('state'),
                                country=data.get('country'),
                                country_i nitials=data.get('country_initials'),
                                timezone=data.get('timezone'),
                                health_cust=data.get('health_cust'),
                                airport=data.get('airport')))
return cities 

def get_city(self, city_id: str) -> city:
    db = firestore.client()
    doc = db.collection('cities').document(city_id).get()
    if doc.exists:
        data = doc.to_dict()
        return City(id=doc.id,
                    state=data.get('state'),
                    country=data.get('country'),
                    country_initials=data.get('country_initials'),
                    timezone=data.get('timexone'),
                    health_cust=data.get('health_cust'),
                    airport= data.get('airport'))
return None

def add_city(self, city: City) -> str:
    db = firestore.client()
    doc = db.collection('cities').add({
        'state': city.state,
        'country': city.country,
        'country_initials': city.country_initials,
        'timezone': city.timezone,
        'health_cust': city.health_cust,
        'airport': city.airport,
    })
    return doc.id

    def update_city(self, city_id: str, city: City) -> bool:
        db = firestore.client()
        db.collection('cities').document(city_id).update({
        'state': city.state,
        'country': city.country,
        'country_initials': city.country_initials,
        'timezone': city.timezone,
        'health_cust': city.health_cust,
        'airport': city.airport,
        })

    return True
    


        
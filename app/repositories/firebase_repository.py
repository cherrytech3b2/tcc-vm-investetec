from app.core.firebase_config import get_db

class UserRepository:
    def __init__(self):
        self.collection = get_db().collection('users')

    def get_by_email(self, email: str, perfil: str):
        doc = self.collection.document(f"{perfil}_{email}").get()
        if doc.exists:
            return doc.to_dict()
        return None

    def save(self, user_dict: dict):
        email = user_dict.get("email")
        perfil = user_dict.get("perfil")
        doc_ref = self.collection.document(f"{perfil}_{email}")
        doc_ref.set(user_dict, merge=True)

class ProjectRepository:
    def __init__(self):
        self.collection = get_db().collection('projects')

    def get_all_available(self):
        docs = self.collection.where("status", "==", "Disponível").stream()
        return [doc.to_dict() for doc in docs]

    def get_by_owner(self, owner_email: str):
        docs = self.collection.where("owner_email", "==", owner_email).stream()
        return [doc.to_dict() for doc in docs]

    def get_by_id(self, project_id: str):
        doc = self.collection.document(project_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def save(self, project_dict: dict):
        doc_ref = self.collection.document(project_dict['id'])
        doc_ref.set(project_dict, merge=True)
        return project_dict

    def delete(self, project_id: str):
        self.collection.document(project_id).delete()

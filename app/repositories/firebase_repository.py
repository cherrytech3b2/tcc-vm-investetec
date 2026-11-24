from datetime import datetime, timezone
from app.core.firebase_config import get_db
from app.core.uploads import gerar_thumbnail_imagem, sincronizar_midias_projeto


def _agora_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class UserRepository:
    def __init__(self):
        self.collection = get_db().collection("users")

    def get_by_email(self, email: str, perfil: str):
        doc = self.collection.document(f"{perfil}_{email}").get()
        if doc.exists:
            return doc.to_dict()
        return None

    def get_by_uid(self, uid: str, perfil: str = None):
        if not uid:
            return None
        query = self.collection.where("uid", "==", uid)
        if perfil:
            query = query.where("perfil", "==", perfil)
        for doc in query.limit(1).stream():
            return doc.to_dict()
        return None

    def save(self, user_dict: dict):
        email = (user_dict.get("email") or "").strip().lower()
        perfil = user_dict.get("perfil")
        dados = dict(user_dict)
        dados["email"] = email
        agora = _agora_iso()
        dados.setdefault("created_at", agora)
        dados["updated_at"] = agora
        if dados.get("foto") and not dados.get("foto_thumbnail"):
            dados["foto_thumbnail"] = gerar_thumbnail_imagem(dados["foto"], 200, 200)
        doc_ref = self.collection.document(f"{perfil}_{email}")
        doc_ref.set(dados, merge=True)
        return dados


class ProjectRepository:
    def __init__(self):
        self.collection = get_db().collection("projects")

    def get_all_available(self):
        docs = self.collection.where("status", "==", "Disponível").stream()
        return [sincronizar_midias_projeto(doc.to_dict()) for doc in docs]

    def get_by_owner(self, owner_email: str, owner_uid: str = None):
        docs = self.collection.where("owner_email", "==", owner_email).stream()
        projetos = {doc.id: sincronizar_midias_projeto(doc.to_dict()) for doc in docs}
        if owner_uid:
            for doc in self.collection.where("owner_uid", "==", owner_uid).stream():
                projetos.setdefault(doc.id, sincronizar_midias_projeto(doc.to_dict()))
        return list(projetos.values())

    def get_by_id(self, project_id: str):
        doc = self.collection.document(project_id).get()
        if doc.exists:
            return sincronizar_midias_projeto(doc.to_dict())
        return None

    def save(self, project_dict: dict):
        dados = sincronizar_midias_projeto(dict(project_dict))
        agora = _agora_iso()
        dados.setdefault("created_at", agora)
        dados["updated_at"] = agora
        doc_ref = self.collection.document(dados["id"])
        doc_ref.set(dados, merge=True)
        return dados

    def delete(self, project_id: str):
        self.collection.document(project_id).delete()

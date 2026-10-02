import uuid
import re
from app.repositories.firebase_repository import ProjectRepository

class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepository()

    def create_or_update_project(self, project_data: dict, is_new: bool, is_submit: bool) -> tuple[dict, dict]:
        erros = {}
        
        # Validações de negócio
        if not project_data.get("titulo"):
            erros["titulo"] = "Informe o nome do projeto."
            
        contato_email = project_data.get("contato_email")
        if contato_email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", contato_email):
            erros["contato_email"] = "E-mail inválido."
            
        # Adicione aqui mais validações do negócio (ex: número máximo de integrantes, etc.)

        if not erros:
            # Regras de Negócio de Status e ID
            project_data["status"] = "Disponível" if is_submit else "Rascunho"
            
            if is_new:
                project_data["id"] = uuid.uuid4().hex
                
            self.project_repo.save(project_data)
            
        return project_data, erros

    def delete_project(self, project_id: str, owner_email: str) -> bool:
        p = self.project_repo.get_by_id(project_id)
        if p and p.get("owner_email", p.get("owner")) == owner_email:
            self.project_repo.delete(project_id)
            return True
        return False
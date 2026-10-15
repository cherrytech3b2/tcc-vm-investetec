import uuid
import re
from app.repositories.firebase_repository import ProjectRepository

class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepository()

    def create_or_update_project(self, project_data: dict, is_new: bool, is_submit: bool) -> tuple[dict, dict]:
        erros = {}
        cursos = ["Informática para Internet", "Mecatrônica", "Administração"]
        niveis = ["Em desenvolvimento", "Protótipo", "Concluído"]

        if not project_data.get("titulo"):
            erros["titulo"] = "Informe o nome do projeto."

        contato_email = project_data.get("contato_email")
        if contato_email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", contato_email):
            erros["contato_email"] = "E-mail inválido."

        tel = re.sub(r"\D", "", project_data.get("contato_telefone", ""))
        if tel and len(tel) not in (10, 11):
            erros["contato_telefone"] = "Telefone inválido. Use DDD + número."

        if is_submit:
            obrigatorios = {
                "descricao": "Informe a descrição resumida.",
                "descricao_completa": "Informe a descrição completa.",
                "responsavel": "Informe o responsável.",
                "problema": "Informe o problema.",
                "solucao": "Informe a solução.",
                "diferencial": "Informe o diferencial.",
                "publico_alvo": "Informe o público-alvo.",
                "potencial": "Informe o potencial.",
            }
            for campo, msg in obrigatorios.items():
                if not project_data.get(campo):
                    erros[campo] = msg
            if project_data.get("categoria") not in cursos:
                erros["categoria"] = "Selecione o curso principal."
            if project_data.get("nivel") not in niveis:
                erros["nivel"] = "Selecione o estágio do projeto."
            if not project_data.get("tecnologias"):
                erros["tecnologias"] = "Informe ao menos uma tecnologia."
            for i in (1, 2, 3):
                if not project_data.get(f"foto_{i}"):
                    erros[f"foto{i}"] = f"Envie a foto {i}."
            if not project_data.get("video"):
                erros["video"] = "Envie o vídeo."
            if not project_data.get("contato_email") and not tel:
                erros["contato"] = "Informe ao menos um contato (e-mail ou telefone)."
            if not project_data.get("autoriza"):
                erros["autoriza"] = "Confirme a autorização para divulgar o contato."

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
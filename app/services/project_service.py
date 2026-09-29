from app.repositories.project_repository import ProjectRepository
from app.models.project import Project

class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepository()

    def get_all_projects(self):
        return self.project_repo.get_all_projects()

    def add_project(self, data: dict):
        project = Project(
            id=None,
            name=data.get('name'),
            description=data.get('description'),
            course=data.get('course'),
            status=data.get('status'),
            has_interest=data.get('has_interest', False),
            is_favorite=data.get('is_favorite', False),
            full_name=data.get('full_name'),
            email=data.get('email'),
            password=data.get('password'),
            account_type=data.get('account_type'),
            accepted_terms=data.get('accepted_terms', False)
        )
        return self.project_repo.add_project(project)

    def update_project(self, project_id: str, data: dict):
        project = Project(
            id=project_id,
            name=data.get('name'),
            description=data.get('description'),
            course=data.get('course'),
            status=data.get('status'),
            has_interest=data.get('has_interest', False),
            is_favorite=data.get('is_favorite', False),
            full_name=data.get('full_name'),
            email=data.get('email'),
            password=data.get('password'),
            account_type=data.get('account_type'),
            accepted_terms=data.get('accepted_terms', False)
        )
        return self.project_repo.update_project(project_id, project)
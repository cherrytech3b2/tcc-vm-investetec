import firebase_admin
from firebase_admin import firestore
from app.models.project import Project

class ProjectRepository:
    def get_all_projects(self) -> list[Project]:
        db = firestore.client()
        docs = db.collection('projects').stream()
        projects = []
        for doc in docs:
            data = doc.to_dict()
            projects.append(Project(id=doc.id,
                                    name=data.get('name'),
                                    description=data.get('description'),
                                    course=data.get('course'),
                                    status=data.get('status'),
                                    has_interest=data.get('has_interest'),
                                    is_favorite=data.get('is_favorite'),
                                    full_name=data.get('full_name'),
                                    email=data.get('email'),
                                    password=data.get('password'),
                                    account_type=data.get('account_type'),
                                    accepted_terms=data.get('accepted_terms')))
        return projects

    def get_project(self, project_id: str) -> Project:
        db = firestore.client()
        doc = db.collection('projects').document(project_id).get()
        if doc.exists:
            data = doc.to_dict()
            return Project(id=doc.id,
                           name=data.get('name'),
                           description=data.get('description'),
                           course=data.get('course'),
                           status=data.get('status'),
                           has_interest=data.get('has_interest'),
                           is_favorite=data.get('is_favorite'),
                           full_name=data.get('full_name'),
                           email=data.get('email'),
                           password=data.get('password'),
                           account_type=data.get('account_type'),
                           accepted_terms=data.get('accepted_terms'))
        return None

    def add_project(self, project: Project) -> str:
        db = firestore.client()
        doc = db.collection('projects').add({
            'name': project.name,
            'description': project.description,
            'course': project.course,
            'status': project.status,
            'has_interest': project.has_interest,
            'is_favorite': project.is_favorite,
            'full_name': project.full_name,
            'email': project.email,
            'password': project.password,
            'account_type': project.account_type,
            'accepted_terms': project.accepted_terms,
        })
        return doc[1].id

    def update_project(self, project_id: str, project: Project) -> bool:
        db = firestore.client()
        db.collection('projects').document(project_id).update({
            'name': project.name,
            'description': project.description,
            'course': project.course,
            'status': project.status,
            'has_interest': project.has_interest,
            'is_favorite': project.is_favorite,
            'full_name': project.full_name,
            'email': project.email,
            'password': project.password,
            'account_type': project.account_type,
            'accepted_terms': project.accepted_terms,
        })
        return True
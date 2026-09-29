from dataclasses import dataclass

@dataclass
class Project:
    id: str
    name: str
    description: str
    course: str
    status: str
    has_interest: bool
    is_favorite: bool
    full_name: str
    email: str
    password: str
    account_type: str
    accepted_terms: bool
        
  
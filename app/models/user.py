from dataclass import dataclass

@dataclass
class User:
    uid: str
    nome:str
    email:str
    created_at: str = None
    update_at: str = None
from dataclass import dataclass
from datatime import datetime

@dataclass
class User:
    uid: str
    nome:str
    email:str
    created_at: str = None
    update_at: str = None 
    datatime = field(default_factory=datatime.utcnow)

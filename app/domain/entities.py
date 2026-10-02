from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class User:
    email: str
    perfil: str 
    nome: str
    telefone: Optional[str] = None
    bio: Optional[str] = None
    foto: Optional[str] = None
    curso: Optional[str] = None
    turma: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    interesses: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class Project:
    id: str
    owner_email: str
    status: str
    titulo: str
    descricao: str
    categoria: str
    tipo: str
    nivel: str
    descricao_completa: Optional[str] = None
    responsavel: Optional[str] = None
    turma: Optional[str] = None
    integrantes: Optional[str] = None
    problema: Optional[str] = None
    solucao: Optional[str] = None
    diferencial: Optional[str] = None
    publico_alvo: Optional[str] = None
    potencial: Optional[str] = None
    contato_email: Optional[str] = None
    contato_telefone: Optional[str] = None
    tecnologias: List[str] = field(default_factory=list)
    fotos: List[str] = field(default_factory=list)
    video: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _agora_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class User:
    email: str
    perfil: str
    nome: str
    uid: Optional[str] = None
    provedor: str = "password"
    accepted_terms: bool = True
    telefone: Optional[str] = None
    bio: Optional[str] = None
    foto: Optional[str] = None
    foto_thumbnail: Optional[str] = None
    curso: Optional[str] = None
    turma: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    interesses: Optional[str] = None
    created_at: Optional[str] = field(default_factory=_agora_iso)
    updated_at: Optional[str] = field(default_factory=_agora_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        valid = {f.name for f in fields(cls)}
        filtrado = {k: v for k, v in (data or {}).items() if k in valid}
        return cls(**filtrado)


@dataclass
class Project:
    id: str
    owner_email: str
    status: str = "Rascunho"
    titulo: str = ""
    descricao: str = ""
    categoria: str = ""
    curso: str = ""
    tipo: str = "Individual"
    integrado: bool = False
    nivel: str = ""
    owner: Optional[str] = None
    owner_uid: Optional[str] = None
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
    autoriza: bool = False
    cursos_integrados: List[str] = field(default_factory=list)
    tecnologias: List[str] = field(default_factory=list)
    # Mídias hospedadas no Cloudinary (originais + thumbnails)
    foto_1: Optional[str] = None
    foto_2: Optional[str] = None
    foto_3: Optional[str] = None
    fotos: List[str] = field(default_factory=list)
    imagem: Optional[str] = None
    thumbnail: Optional[str] = None
    thumbnails: List[str] = field(default_factory=list)
    video: Optional[str] = None
    video_thumbnail: Optional[str] = None
    midias: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = field(default_factory=_agora_iso)
    updated_at: Optional[str] = field(default_factory=_agora_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        valid = {f.name for f in fields(cls)}
        filtrado = {k: v for k, v in (data or {}).items() if k in valid}
        return cls(**filtrado)

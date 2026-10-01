# Adicione ao seu models.py (ou importe este arquivo). Assume Flask-SQLAlchemy: db = SQLAlchemy()
from datetime import datetime
from extensions import db  # <- ajuste para onde está o seu "db"


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False, index=True)  # dono do projeto
    titulo = db.Column(db.String(80), default="")
    descricao = db.Column(db.String(200), default="")            # resumida (card)
    descricao_completa = db.Column(db.Text, default="")          # detalhes
    categoria = db.Column(db.String(40), default="")             # curso principal
    tipo = db.Column(db.String(20), default="Individual")        # Individual | Integrado
    status = db.Column(db.String(20), default="Rascunho")        # Rascunho|Enviado|Disponível|Arquivado
    problema = db.Column(db.Text, default="")
    solucao = db.Column(db.Text, default="")
    diferencial = db.Column(db.Text, default="")
    publico_alvo = db.Column(db.Text, default="")
    potencial = db.Column(db.Text, default="")
    responsavel = db.Column(db.String(80), default="")
    turma = db.Column(db.String(30), default="")
    cursos_envolvidos = db.Column(db.String(200), default="")    # "Mecatrônica,Administração"
    video = db.Column(db.String(200), default="")
    imagem_principal = db.Column(db.Integer, default=1)          # posição da foto (1-3)
    contato_email = db.Column(db.String(120), default="")
    contato_telefone = db.Column(db.String(30), default="")
    contato_autorizado = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fotos = db.relationship("Foto", backref="projeto", cascade="all, delete-orphan", order_by="Foto.posicao")
    integrantes = db.relationship("Integrante", backref="projeto", cascade="all, delete-orphan")

    def foto(self, pos):
        return next((f for f in self.fotos if f.posicao == pos), None)

    @property
    def capa(self):
        f = self.foto(self.imagem_principal or 1) or (self.fotos[0] if self.fotos else None)
        return f.arquivo if f else None


class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    posicao = db.Column(db.Integer, nullable=False)  # 1, 2 ou 3
    arquivo = db.Column(db.String(200), nullable=False)


class Integrante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    curso = db.Column(db.String(40), default="")
    funcao = db.Column(db.String(60), default="")
